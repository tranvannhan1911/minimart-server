import datetime
from email.policy import default
from enum import unique
from itertools import product
from pprint import pprint
from secrets import choice
from sqlite3 import IntegrityError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from vi_address.models import Ward

from management.utils.utils import end_of_date, start_of_date, to_datetime

def created_updated(obj, request):
    if obj.user_created is None:
        obj.user_created = request.user
    else:
        obj.date_updated = timezone.now()
        obj.user_updated = request.user
    obj.save()

def filter_date(queryset, start_of_date, end_of_date):
    # queryset = queryset.filter(
    #     Q(date_created__year__gt=start_of_date.year | 
    #         Q(date_created__year=start_of_date.year) & 
    #         Q(date_created__month__gt=start_of_date.month) |
    #             Q(date_created__month=start_of_date.month) & Q(date_created__day_gte=start_of_date.day)
    #         ))
    #     )
    # )
    
    queryset = queryset.filter(date_created__gte=start_of_date)
    queryset = queryset.filter(date_created__lt=end_of_date+datetime.timedelta(days=1))
    # queryset = queryset.filter(
    #     Q(date_created__year__lt=end_of_date.year | 
    #         (Q(date_created__year=end_of_date.year) & 
    #         (Q(date_created__month__lt=end_of_date.month) |
    #             Q(date_created__month=end_of_date.month) & 
    #             Q(date_created__day_lte=end_of_date.day)))
    #     )
    # )
    return queryset

def _filter_date_str(queryset, start_date, end_date):
    if start_date:
        start_date = to_datetime(start_date)
        start_date = start_of_date(start_date)
        queryset = queryset.filter(date_created__gte=start_date)
        
    if end_date:
        end_date = to_datetime(end_date)
        end_date = end_of_date(end_date)
        queryset = queryset.filter(date_created__lte=end_date)

    return queryset

def filter_product(queryset, product_id, product_group_id, product_category_id):
    if product_id:
        queryset = queryset.filter(product=product_id)
        
    if product_group_id:
        queryset = queryset.filter(product__product_groups=product_group_id)

    if product_category_id and HierarchyTree.objects.filter(pk = product_category_id).exists():
        product_category = HierarchyTree.objects.get(pk = product_category_id)
        childrens = product_category.get_all_children_id()
        queryset = queryset.filter(product__product_category__in=childrens)

    return queryset

def unique_rand():
    code = User.objects.make_random_password(length=8)
    return code

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Số điện thoại không được để trống')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)

class CustomerGroup(models.Model):
    name = models.CharField('Tên nhóm khách hàng', max_length=50)
    description = models.TextField('Mô tả nhóm khách hàng', blank=True)
    note = models.TextField('Ghi chú', null=True)
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="customer_group_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="customer_group_updated")
    
    class Meta:
        db_table = 'CustomerGroup'

    def delete(self, using=None, keep_parents=False):
        if CustomerGroup.objects.filter(customer_group_detail=self.pk).exists():
            raise IntegrityError
        super().delete(using, keep_parents)

class User(AbstractUser):
    code = models.CharField('Mã nhân viên', max_length=30, unique=True, default=unique_rand)
    phone = models.CharField('Số điện thoại', max_length=15, unique=True)
    fullname = models.CharField('Tên nhân viên', max_length=30, null=True)
    gender = models.CharField('Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    ))
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú', null=True)
    
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="users_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="users_updated")
    is_manager = models.BooleanField("Quản lý", default=False)
    is_staff = True

    email = None
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.format_code()
        super(User, self).save(*args, **kwargs)

    def format_code(self):
        while True:
            _code = "NV"+str(CounterIndex.increase("User")).zfill(5)
            if not User.objects.filter(code = _code).exists():
                self.code = _code
                break


    def __str__(self):
        return self.phone

    @staticmethod
    def check_exists(phone, is_active=None):
        if is_active == None:
            return User.objects.filter(phone=phone).exists()
        return User.objects.filter(phone=phone, is_active=is_active).exists()

    @staticmethod
    def format_phone(phone):
        if phone[:3] != "+84":
            if phone[0] == "0":
                phone = "+84"+phone[1:]
            else:
                phone = "+84"+phone
        return phone

    @staticmethod
    def convert_phone(phone):
        if phone[:3] == "+84":
            if phone[3] == "0":
                phone = phone[3:]
            else:
                phone = "0"+phone[3:]
        return phone

    @staticmethod
    def random_password():
        import string
        import random
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    class Meta:
        db_table = 'Staff'


class Customer(models.Model):
    phone = models.CharField('Số điện thoại', max_length=15, unique=True)
    customer_group = models.ManyToManyField(CustomerGroup, 
        db_table='CustomerGroupDetail', blank=True, 
        related_name='customer_group_detail')
    fullname = models.CharField('Tên khách hàng', max_length=30, null=True)
    gender = models.CharField('Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    ))
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú', null=True)
    password = models.CharField("Mật khẩu", max_length=128, blank=True)
    last_login = models.DateTimeField("Lần đăng nhập cuối cùng", blank=True, null=True)
    is_active = models.BooleanField("Hoạt động", default=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="customer_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey("management.User", on_delete=models.PROTECT, 
        null=True, related_name="customer_updated")

    def __str__(self):
        return self.phone

    @staticmethod
    def check_exists(phone, is_active=None):
        if is_active == None:
            return Customer.objects.filter(phone=phone).exists()
        return Customer.objects.filter(phone=phone, is_active=is_active).exists()
    
    def random_password(self):
        import string
        import random
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    
    def set_password(self, raw_password=None):
        if not raw_password:
            raw_password = self.random_password()
        self.password = make_password(raw_password)
        self._password = raw_password
        return raw_password

    def check_password(self, raw_password):
        salt = self.password.split("$")[2]
        password = make_password(raw_password, salt)
        if password == self.password:
            return True
        return False

    class Meta:
        db_table = 'Customer'

class ProductGroup(models.Model):
    product_group_code = models.CharField('Mã nhóm sản phẩm', max_length=15)
    name = models.CharField('Tên nhóm sản phẩm', max_length=255)
    description = models.TextField('Mô tả nhóm sản phẩm', 
        help_text='Mô tả của nhóm sản phẩm', null=True)
    note = models.TextField('Ghi chú', null=True)
    
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="product_group_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="product_group_updated")

    class Meta:
        db_table = 'ProductGroup'

class Supplier(models.Model):
    code = models.CharField('Mã code', max_length=30, unique=True)
    name = models.CharField('Tên nhà cung cấp', max_length=100)
    phone = models.CharField('Số điện thoại', max_length=15)
    email = models.CharField('Địa chỉ email', max_length=50, null=True)
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="suppliers_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="suppliers_updated")

    class Meta:
        db_table = 'Supplier'

class HierarchyTree(models.Model):
    code = models.CharField('Mã code', max_length=30, unique=True)
    name = models.CharField('Tên cấp', max_length=50)
    level = models.IntegerField('Cấp', default=0)
    type = models.CharField('Loại', max_length=15, choices=(
        ("product", "Sản phẩm"),
    ))
    parent = models.ForeignKey("management.HierarchyTree", 
        on_delete=models.CASCADE, null=True, related_name='children')
    note = models.TextField('Ghi chú', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="hierarchy_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="hierarchy_updated")

    class Meta:
        db_table = 'HierarchyTree'


    def get_all_children_id(self):
        ret = []
        queue = []
        queue.append(self)
        while(len(queue) > 0):
            cur = queue.pop(0)
            ret.append(cur.id)
            for child in cur.children.all():
                queue.append(child)
        return ret




class CalculationUnit(models.Model):
    # unit_id = models.AutoField('Mã đơn vị tính', primary_key=True)
    code = models.CharField('Mã code', max_length=30, unique=True)
    name = models.CharField('Tên đơn vị tính', max_length=50, unique=True)
    note = models.TextField('Ghi chú', help_text='Ghi chú nội bộ', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="units_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="units_updated")
    class Meta:
        db_table = 'CalculationUnit'


class Product(models.Model):
    product_code = models.CharField('Mã sản phẩm', max_length=15)
    name = models.CharField('Tên sản phẩm', max_length=255)
    description = models.TextField('Mô tả sản phẩm', null=True)
    image = models.CharField('Hình ảnh sản phẩm', max_length=255, null=True)
    barcode = models.CharField('Mã vạch', max_length=15)
    barcode_image = models.CharField('Ảnh mã vạch', max_length=255)
    product_groups = models.ManyToManyField(ProductGroup, related_name='products', 
        db_table='ProductGroupDetail', blank=True)
    product_category = models.ForeignKey(HierarchyTree, on_delete=models.PROTECT, 
        related_name='products', null=True)
    # base_unit = models.ForeignKey(CalculationUnit, on_delete=models.CASCADE, verbose_name='Đơn vị cơ bản',
    #     help_text='Đơn vị cơ bản', related_name='products', )
    units = models.ManyToManyField(CalculationUnit, through='management.UnitExchange',
        blank=True)
    status = models.BooleanField('Trạng thái', default=False)
    note = models.TextField('Ghi chú', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="products_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="products_updated")

    def stock(self):
        transactions = WarehouseTransaction.objects.filter(product=self)
        # print(transactions)
        ammount = 0
        for tran in transactions:
            ammount += tran.change
        return ammount

    def get_base_unit(self):
        return self.units.filter(
            unitexchanges__product=self, 
            unitexchanges__is_base_unit=True,
            unitexchanges__is_active=True
            ).first()

    def get_unit_exchange(self, unit=None):
        if unit == None:
            unit = self.get_base_unit()
        return UnitExchange.objects.filter(
            product=self, 
            unit=unit,
            is_active=True
            ).first()

    def get_price_detail(self, unit_exchange=None):
        if unit_exchange == None:
            unit_exchange = self.get_unit_exchange(self.get_base_unit())
        
        return self.pricedetails.filter(
            unit_exchange=unit_exchange,
            pricelist__start_date__lte=timezone.now(),
            pricelist__end_date__gte=timezone.now(),
            pricelist__status = True
        ).order_by("-id").first()

    def get_price_detail_by_unit(self, unit=None):
        if unit == None:
            unit = self.get_base_unit()
        unit_exchange = self.get_unit_exchange(unit)
        return self.get_price_detail(unit_exchange)

    def _have_price(self):
        if self.get_price_detail() == None:
            return False
        return True
    
    def remain(self):
        return str(self.stock())+" "+self.get_base_unit().name


    class Meta:
        db_table = 'Product'

class UnitExchange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
        related_name='unitexchanges')
    unit = models.ForeignKey(CalculationUnit, on_delete=models.CASCADE,
        related_name='unitexchanges')
    value = models.PositiveIntegerField('Giá trị quy đổi',
        help_text='Đơn vị này bằng bao nhiêu đơn vị mặc định?', default=1)
    allow_sale = models.BooleanField('Đơn vị được phép bán hàng',
        help_text='Cho phép bán hàng bằng đơn vị này không?', default=False)
    is_base_unit = models.BooleanField('Đơn vị cơ bản', default=False)
    is_active = models.BooleanField('Hoạt động', default=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="unit_exchange_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="unit_exchange_updated")

    def get_number_of(self, ammount):
        return self.value*ammount

    @property
    def price(self):
        print(self)
        print(self.product.get_price_detail(self))
        return self.product.get_price_detail(self).price

    class Meta:
        db_table = 'UnitExchange'
    
class PriceList(models.Model):
    price_list_id = models.AutoField('Mã bảng giá', primary_key=True)
    name = models.CharField('Tên bảng giá', max_length=50, default="")    
    start_date = models.DateTimeField('Thời gian bắt đầu',
        help_text='Thời gian bắt đâu áp dụng bảng giá', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc',
        help_text='Thời gian kết thúc áp dụng bảng giá', default=timezone.now)
    status = models.BooleanField('Trạng thái', default=False)
    note = models.TextField('Ghi chú', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="pricelists_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="pricelists_updated")
    
    class Meta:
        db_table = 'PriceList'

class PriceDetail(models.Model):
    pricelist = models.ForeignKey(PriceList, on_delete=models.CASCADE, 
        related_name='pricedetails')
    product = models.ForeignKey(Product, verbose_name='Sản phẩm', on_delete=models.CASCADE,
        related_name='pricedetails')
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        related_name='pricedetails', null=True)
    price = models.FloatField('Giá bán', default=0)
    # start_date = models.DateTimeField('Thời gian bắt đầu', default=timezone.now)
    # end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'PriceDetail'

    @staticmethod
    def check_overlapse(product, start_date, end_date, exclude=None):
        queryset = PriceDetail.objects.filter(
            product=product,
            pricelist__status=True)

        if exclude:
            queryset = queryset.exclude(pricelist__price_list_id = exclude.price_list_id)
        queryset = queryset.exclude(pricelist__start_date__gt=end_date)
        queryset = queryset.exclude(pricelist__end_date__lt=start_date)
        return queryset

class Order(models.Model):
    # order_id = models.AutoField('Mã đơn hàng', primary_key=True)
    note = models.TextField('Ghi chú', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,
        related_name='orders', null=True)
    total = models.FloatField('Tổng tiền', default=0)
    final_total = models.FloatField('Thành tiền', default=0)
    status = models.CharField('Trạng thái', max_length=15, default="complete", choices=(
        ('complete', 'Hoàn tất'),
        ('cancel', 'Đã hủy đơn'),
        ('refund', 'Đã trả đơn')
    ))

    date_created = models.DateTimeField('Ngày lập hóa đơn', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="orders_created")
    date_updated = models.DateTimeField('Ngày cập nhật hóa đơn', default=timezone.now)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="orders_updated")

    class Meta:
        db_table = 'Order'

    @staticmethod
    def _filter(queryset, start_date, end_date, staff_id):
        queryset = _filter_date_str(queryset, start_date, end_date)
        if staff_id:
            queryset = queryset.filter(user_created__id=staff_id)

        return queryset


    @staticmethod
    def _filter_date(queryset, start_date, end_date):
        return _filter_date_str(queryset, start_date, end_date)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
        related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', on_delete=models.CASCADE)
    price = models.ForeignKey(PriceDetail, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveIntegerField('Số lượng')
    total = models.FloatField('Thành tiền', default=0)
    note = models.TextField('Ghi chú', null=True)

    def get_quantity_dvtcb(self):
        return self.quantity*self.unit_exchange.value
    class Meta:
        db_table = 'OrderDetail'

class OrderRefund(models.Model):
    # refund_id = models.AutoField('Mã trả hàng', primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT,
        related_name='refund')
    note = models.TextField('Ghi chú', null=True)
    status = models.CharField('Trạng thái', max_length=15, default="pending", choices=(
        ('complete', 'Hoàn tất'),
        ('cancel', 'Hủy')
    ))

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="orders_refund_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="orders_refund_updated")
    
    class Meta:
        db_table = 'OrderRefund'

    @staticmethod
    def _filter_date(queryset, start_date, end_date):
        return _filter_date_str(queryset, start_date, end_date)

class OrderRefundDetail(models.Model):
    order_refund = models.ForeignKey(OrderRefund, on_delete=models.CASCADE,
        related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', 
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Số lượng')
    note = models.TextField('Ghi chú', null=True)

    def get_quantity_dvtcb(self):
        return self.quantity*self.unit_exchange.value

    class Meta:
        db_table = 'OrderRefundDetail'

class InventoryReceivingVoucher(models.Model):
    # voucher_id = models.AutoField('Mã phiếu nhập hàng', primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)
    status = models.CharField('Trạng thái', max_length=15, choices=(
        ("pending", "Chờ xác nhận"),
        ("complete", "Hoàn thành"),
        ("cancel", "Hủy"),
    ))
    note = models.TextField('Ghi chú', null=True)
    total = models.FloatField('Thành tiền', default=0)
    
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="inventory_receiving_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="inventory_receiving_updated")
    
    class Meta:
        db_table = 'InventoryReceivingVoucher'

class InventoryReceivingVoucherDetail(models.Model):
    receiving_voucher = models.ForeignKey(InventoryReceivingVoucher, on_delete=models.CASCADE,
        related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', 
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Số lượng')
    quantity_base_unit = models.PositiveIntegerField('Số lượng trên đơn vị cơ bản', default=1)
    price = models.FloatField('Giá nhập')
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'InventoryReceivingVoucherDetail'

    @staticmethod
    def filter_date(queryset, start_date, end_date):
        if start_date:
            start_date = to_datetime(start_date)
            start_date = start_of_date(start_date)
            queryset = queryset.filter(receiving_voucher__date_created_gte=start_date)
            
        if end_date:
            end_date = to_datetime(end_date)
            end_date = end_of_date(end_date)
            queryset = queryset.filter(receiving_voucher__date_created_lte=end_date)

        return queryset

class InventoryVoucher(models.Model):
    # voucher_id = models.AutoField('Mã phiếu kiểm kê', primary_key=True)
    # status = models.CharField('Trạng thái', max_length=15)
    note = models.TextField('Ghi chú', null=True)
    status = models.CharField('Trạng thái', max_length=15, choices=(
        ("pending", "Chờ xác nhận"),
        ("complete", "Hoàn thành"),
        ("cancel", "Hủy"),
    ))
    
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="inventory_created")
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="inventory_updated")
    
    class Meta:
        db_table = 'InventoryVoucher'

class InventoryVoucherDetail(models.Model):
    inventory_voucher = models.ForeignKey(InventoryVoucher, on_delete=models.CASCADE,
        related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity_before = models.PositiveIntegerField('Số lượng trước', null=True)
    quantity_after = models.PositiveIntegerField('Số lượng sau')
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'InventoryVoucherDetail'

class WarehouseTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    reference = models.CharField("Hóa đơn hoặc mã phiếu", max_length=30, null=True)

    change = models.IntegerField('Thay đổi')
    type = models.CharField("Loại biến động", max_length=30, choices=(
        ('order', 'Bán hàng'),
        ('order_cancel', 'Hủy hóa đơn'),
        ('promotion', 'Khuyến mãi'),
        ('inventory', 'Kiểm kê'),
        ('inventory_cancel', 'Hủy kiểm kê'),
        ('inventory_receiving', 'Nhập hàng'),
        ('inventory_receiving_cancel', 'Hủy nhập hàng'),
        ('refund', 'Trả hàng'),
    ))
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'WarehouseTransaction'

class Promotion(models.Model):
    title = models.CharField('Tiêu đề của chương trình khuyến mãi', max_length=255)
    description = models.TextField('Mô tả chương trình khuyến mãi', default="")
    image = models.CharField('Hình ảnh', max_length=255, null=True)
    
    applicable_customer_groups = models.ManyToManyField(CustomerGroup, 
        db_table='ApplicableCustomerGroup', blank=True)

    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)

    status = models.BooleanField('Trạng thái', default=False)
    note = models.TextField('Ghi chú', null=True)

    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, related_name="promotions_created", 
        null=True)
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="promotions_updated")
    
    class Meta:
        db_table = 'Promotion'

class PromotionLine(models.Model):
    title = models.CharField('Tiêu đề của khuyến mãi', max_length=255, default="")
    description = models.TextField('Mô tả khuyến mãi', default="")
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15, null=True, unique=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='lines')
    type = models.CharField('Loại khuyến mãi', max_length=15, choices=(
        ('Product', 'Khuyến mãi sản phẩm'),
        ('Percent', 'Khuyến mãi theo phần trăm hóa đơn'),
        ('Fixed', 'Khuyến mãi số tiền nhất định'),
    ))
    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)
    status = models.BooleanField('Trạng thái')
    # None: Không giới hạn
    max_quantity = models.IntegerField('Số lần áp dụng tối đa', null=True) 
    max_quantity_per_customer = models.IntegerField('Số lần áp dụng tối đa trên khách hàng', null=True)
    max_quantity_per_customer_per_day = models.IntegerField('Số lần áp dụng tối đa trên khách hàng trên 1 ngày', null=True)
    note = models.TextField('Ghi chú', null=True)
    
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, related_name="promotion_lines_created", 
        null=True)
    date_updated = models.DateTimeField('Ngày cập nhật', null=True)
    user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
        null=True, related_name="promotion_lines_updated")
    
    def get_used(self):
        count = 0
        for history in self.histories.all():
            count += history.quantity
        return count

    def get_remain(self):
        if self.max_quantity == None or self.max_quantity == 0:
            return -1 # unlimited
        return self.max_quantity - self.get_used()

    __remain_today = -1

    @property
    def remain_today(self):
        return self.__remain_today

    def get_remain_today(self, customer):
        remain = self.get_remain()
        self.__remain_today = remain
        if self.max_quantity_per_customer_per_day == None or self.max_quantity_per_customer_per_day <= 0:
            return remain

        queryset = self.histories.filter(
            order__customer=customer,
            )
        queryset = filter_date(queryset, timezone.now().date(), timezone.now().date())
        remain_today = min(remain, self.max_quantity_per_customer_per_day - queryset.count())
        self.__remain_today = remain_today
        return remain_today

    __remain_customer = -1
    @property
    def remain_customer(self):
        return self.__remain_customer

    def get_remain_customer(self, customer):
        remain = self.get_remain()
        self.__remain_customer = remain
        # print(self.__remain_customer)
        if self.max_quantity_per_customer == None or self.max_quantity_per_customer <= 0:
            return remain

        queryset = self.histories.filter(
            order__customer=customer,
            )
        remain_customer = min(remain, self.max_quantity_per_customer - queryset.count())
        self.__remain_customer = remain_customer
        return remain_customer

    __benefit = 0
    @property
    def benefit(self):
        return self.__benefit

    __actual_received = 0
    @property
    def actual_received(self):
        return self.__actual_received

    def quantity_base_actual_received(self, product, quantity_base_unit, customer, quantity_in_use_of_product=0):
        remain_today = self.get_remain_today(customer)
        if remain_today == -1:
            remain_today = 99999999999
        
        quantity_buy_p1 = self.detail.quantity_buy
        quantity_received_p1 = self.detail.quantity_received
        
        product_remain = self.detail.product_received.stock()
        product_remain -= quantity_in_use_of_product

        number_of_voucher_use = min(remain_today, quantity_base_unit // quantity_buy_p1)
        number_of_voucher_use = min(number_of_voucher_use, product_remain//quantity_received_p1)
        quantity_base_actual_received = number_of_voucher_use*quantity_received_p1
        self.__actual_received = quantity_base_actual_received
        return quantity_base_actual_received

    def benefit_product(self, product, quantity_base_unit, customer, quantity_in_use_of_product=0):
        quantity_base_actual_received = self.quantity_base_actual_received(
            product, quantity_base_unit, 
            customer, quantity_in_use_of_product)

        price = product.get_price_detail().price
        benefit = quantity_base_actual_received*price
        self.__benefit = benefit
        print("benefit", product, quantity_base_unit, customer, benefit)
        return benefit

    @staticmethod
    def get_best_benefit_product(promotion_lines, product, quantity_base_unit, customer,
            quantity_in_use_of_product=0):
        promotion_line = None
        benefit = 0
        for pl in promotion_lines:
            b = pl.benefit_product(product, quantity_base_unit, customer, quantity_in_use_of_product)
            if benefit < b:
                benefit = b
                promotion_line = pl
        return promotion_line, benefit

    @staticmethod
    def sort_benefit_product(promotion_lines, product, quantity, customer,
            quantity_in_use_of_product=0):
        promotion_lines = sorted(promotion_lines, 
            key=lambda t: -t.benefit_product(product, quantity, customer,
                quantity_in_use_of_product))
        return promotion_lines

    def benefit_order(self, amount):
        benefit = 0
        if amount < self.detail.minimum_total:
            benefit = 0
        elif self.type == "Percent":
            if self.detail.maximum_reduction_amount:
                benefit = min(self.detail.maximum_reduction_amount,
                    self.detail.percent*amount/100)
            else:
                benefit = self.detail.percent*amount/100
        elif self.type == "Fixed":
            benefit = self.detail.reduction_amount
            
        self.__benefit = benefit
        return benefit

    @staticmethod
    def sort_benefit_order(promotion_lines, amount):
        promotion_lines = sorted(promotion_lines, 
            key=lambda t: -t.benefit_order(amount))
        return promotion_lines
        
    
    @staticmethod
    def get_best_benefit_order(promotion_lines, amount):
        promotion_line = None
        benefit = 0
        for pl in promotion_lines:
            b = pl.benefit_order(amount)
            if benefit < b:
                benefit = b
                promotion_line = pl
        return promotion_line, benefit

    @staticmethod
    def filter_customer(promotion_lines, customer):
        # trả về các khuyến mãi không tồn tại nhóm khách hàng áp dụng
        # hoặc khách hàng thuộc nhóm khách hàng được áp dụng
        # print(customer.customer_group.all())
        promotion_lines = promotion_lines.filter(
            Q(promotion__applicable_customer_groups__in = customer.customer_group.all()) |
            Q(promotion__applicable_customer_groups = None)
        )
        return promotion_lines

    @staticmethod
    def get_by_order(amount, status=True):
        # trả về các khuyến mãi theo số tiền hóa đơn
        promotion_lines = PromotionLine.objects.filter(
            promotion__status=status,
            status=status,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            detail__minimum_total__lte=amount
        )
        promotion_lines = promotion_lines.filter(
            Q(type="Percent") | Q(type="Fixed")
        )
        return promotion_lines

    @staticmethod
    def get_by_product(product, status=True):
        promotion_line = PromotionLine.objects.filter(
            promotion__status=status,
            status=status,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            type="Product"
        )
        promotion_line = promotion_line.filter(
            Q(detail__applicable_products = product) |
            Q(detail__applicable_product_groups__products = product)
        )
        return promotion_line

    @staticmethod
    def get_by_type(type, status=True):
        if type:
            if type == "Order":
                return PromotionLine.objects.filter(
                    promotion__status=status,
                    status=status,
                    start_date__lte=timezone.now(),
                    end_date__gte=timezone.now(),
                ).exclude(type="Product")
            return PromotionLine.objects.filter(
                promotion__status=status,
                status=status,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
                type=type
            )
        return PromotionLine.objects.filter(
            promotion__status=status,
            status=status,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )


    class Meta:
        db_table = 'PromotionLine'

class PromotionDetail(models.Model):
    promotion_line = models.OneToOneField(PromotionLine, on_delete=models.CASCADE, null=True, related_name='detail')
    # Product
    applicable_products = models.ManyToManyField(Product, db_table='ApplicableProduct', blank=True)
    applicable_product_groups = models.ManyToManyField(ProductGroup, db_table='ApplicableProductGroup', blank=True)
    product_received = models.ForeignKey(Product, null=True,
        on_delete=models.CASCADE, related_name="promotion_receive")

    quantity_buy = models.PositiveIntegerField('Số lượng sản phẩm cần mua', null=True)
    quantity_received = models.PositiveIntegerField('Số lượng sản phẩm được nhận', null=True)
    # Percent & fixed
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn', null=True)
    # Percent
    percent = models.FloatField('Phần trăm giảm giá', null=True)
    maximum_reduction_amount = models.FloatField('Số tiền được giảm tối đa', null=True)
    # Fixed
    reduction_amount = models.FloatField('Số tiền được giảm', null=True)

    class Meta:
        db_table = 'PromotionDetail'

class PromotionHistory(models.Model):
    promotion_line = models.ForeignKey(PromotionLine, 
        on_delete=models.PROTECT, null=True, related_name="histories")
    type = models.CharField("Loại", max_length=15,choices=(
        ("Order", "Hóa đơn"),
        ("Product", "Sản phẩm"),
    ))
    # order & product
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    # product
    buy_order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, null=True,
        related_name="buy_order_detail")
    received_order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, null=True,
        related_name="received_order_detail")
    ###
    quantity = models.PositiveIntegerField('Số lượng khuyến mãi', default=0, null=True)
    amount = models.FloatField('Số tiền được giảm', null=True)
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'PromotionHistory'

    @staticmethod
    def filter_type(queryset, type):
        if type:
            return queryset.filter(type=type)
        return queryset

class History(models.Model):
    object_name = models.CharField('Tên đối tượng', max_length=50)
    object_id = models.CharField('Mã đối tượng', max_length=50)
    action = models.CharField('Hành động', max_length=15, choices=(
        ('CREATE', "Tạo mới"),
        ('UPDATE', "Cập nhật"),
        ('DELETE', "Xóa"),
    ))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Người thực hiện")
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    note = models.TextField('Ghi chú', null=True)

    class Meta:
        db_table = 'History'

class CounterIndex(models.Model):
    value = models.IntegerField("Giá trị")
    table = models.CharField("Bảng", max_length=30)

    class Meta:
        db_table = 'CounterIndex'

    @staticmethod
    def increase(table):
        try:
            counter = CounterIndex.objects.get(table=table)
            counter.value += 1
            counter.save()
            return counter.value
        except:
            CounterIndex.objects.create(table=table, value = 1)
            return 1
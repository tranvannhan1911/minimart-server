from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

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

class User(AbstractUser):
    phone = models.CharField('Số điện thoại', max_length=15, unique=True)

    email = None
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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
        db_table = 'Account'

class CustomerGroup(models.Model):
    name = models.CharField('Tên nhóm khách hàng', max_length=50)
    description = models.TextField('Mô tả nhóm khách hàng')
    note = models.TextField('Ghi chú', blank=True)
    
    class Meta:
        db_table = 'CustomerGroup'


class Customer(models.Model):
    customer_id = models.AutoField('Mã khách hàng', primary_key=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(CustomerGroup, on_delete=models.PROTECT, null=True)
    fullname = models.CharField('Tên khách hàng', max_length=30)
    gender = models.CharField('Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    ))
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    note = models.TextField('Ghi chú', blank=True)

    class Meta:
        db_table = 'Customer'
    
    @property
    def get_gender(self):
        return self.get_gender_display()

class Staff(models.Model):
    staff_id = models.AutoField('Mã nhân viên', primary_key=True)
    fullname = models.CharField('Tên nhân viên', max_length=30)
    phone = models.CharField('Số điện thoại', max_length=15, unique=True)
    cccd = models.CharField('Số căn cước công dân', max_length=15)
    address = models.CharField('Địa chỉ', max_length=255)
    gender = models.CharField(verbose_name='Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    ))
    day_of_birth = models.DateField('Ngày sinh', default='1900-01-01')
    email = models.CharField('Địa chỉ email', max_length=50)
    status = models.BooleanField('Trạng thái', default=True)

    class Meta:
        db_table = 'Staff'

    @property
    def get_gender(self):
        return self.get_gender_display()

class ProductGroup(models.Model):
    product_type_id = models.AutoField('Mã loại sản phẩm', primary_key=True)
    product_type_name = models.CharField('Tên loại sản phẩm', max_length=255)
    description = models.TextField('Mô tả loại sản phẩm', 
        help_text='Mô tả của loại sản phẩm')
    note = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'ProductGroup'

class Supplier(models.Model):
    supplier_id =  models.AutoField('Mã nhà cung cấp', primary_key=True)
    supplier_name = models.CharField('Tên nhà cung cấp', max_length=100)
    phone = models.CharField('Số điện thoại', max_length=15)
    email = models.CharField('Địa chỉ email', max_length=50)
    address = models.CharField('Địa chỉ', max_length=255)
    note = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'Supplier'

class HierarchyTree(models.Model):
    name = models.CharField('Tên cấp', max_length=50)
    level = models.IntegerField('Cấp', default=0)
    type = models.CharField('Loại', max_length=15, choices=(
        ("product", "Sản phẩm"),
    ))
    parent = models.ForeignKey("management.HierarchyTree", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'HierarchyTree'

class Product(models.Model):
    product_id = models.AutoField('Mã sản phẩm', primary_key=True)
    product_name = models.CharField('Tên sản phẩm', max_length=255)
    description = models.TextField('Mô tả sản phẩm')
    image = models.CharField('Hình ảnh sản phẩm', max_length=255, blank=True)
    barcode = models.CharField('Mã vạch', max_length=15)
    barcode_image = models.CharField('Ảnh mã vạch', max_length=255)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.PROTECT, 
        related_name='products', null=True)
    product_type = models.ForeignKey(HierarchyTree, on_delete=models.PROTECT, 
        related_name='products', null=True)

    class Meta:
        db_table = 'Product'


class Unit(models.Model):
    unit_id = models.AutoField('Mã đơn vị tính', primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
        related_name='units')
    unit_name = models.CharField('Tên đơn vị tính', max_length=30)
    value = models.PositiveIntegerField('Giá trị quy đổi',
        help_text='Đơn vị này bằng bao nhiêu đơn vị mặc định?')
    allow_sale = models.BooleanField('Đơn vị được phép bán hàng',
        help_text='Cho phép bán hàng bằng đơn vị này không?')
    is_base_unit = models.BooleanField('Đơn vị cơ bản',
        help_text='Có phải là đơn vị cơ bản hay không (đơn vị nhỏ nhất)')

    class Meta:
        db_table = 'Unit'
    
class PriceList(models.Model):
    price_list_id = models.AutoField('Mã bảng giá', primary_key=True)
    
    start_date = models.DateTimeField('Thời gian bắt đầu',
        help_text='Thời gian bắt đâu áp dụng bảng giá', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc',
        help_text='Thời gian kết thúc áp dụng bảng giá', default=timezone.now)
    status = models.BooleanField('Trạng thái', default=True)

    class Meta:
        db_table = 'PriceList'

class PriceDetail(models.Model):
    pricelist = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Sản phẩm', on_delete=models.CASCADE,
        related_name='pricedetails', null=True)
    unit = models.ForeignKey(Unit, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        related_name='pricedetails', null=True)
    price = models.FloatField('Giá bán', default=0)

    class Meta:
        db_table = 'PriceDetail'

class Order(models.Model):
    order_id = models.AutoField('Mã đơn hàng', primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,
        related_name='orders', null=True)
    date_created = models.DateTimeField('Ngày lập hóa đơn', default=timezone.now)
    total = models.FloatField('Thành tiền', default=0)
    status = models.CharField('Trạng thái', max_length=15, default="pending", choices=(
        ('pending', 'Đang chờ'),
        ('complete', 'Hoàn tất'),
        ('cancel', 'Đã hủy đơn / hoàn trả')
    ))

    class Meta:
        db_table = 'Order'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        null=True)
    price = models.ForeignKey(PriceDetail, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Số lượng')
    total = models.FloatField('Thành tiền', default=0)
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'OrderDetail'

class Refund(models.Model):
    refund_id = models.AutoField('Mã trả hàng', primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú')
    date_created = models.DateTimeField('Ngày trả hàng', default=timezone.now)

    class Meta:
        db_table = 'Refund'

class InventoryReceivingVoucher(models.Model):
    voucher_id = models.AutoField('Mã phiếu nhập hàng', primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)
    status = models.CharField('Trạng thái', max_length=15, choices=(
        ("pending", "Chờ xác nhận"),
        ("complete", "Hoàn thành"),
    ))
    note = models.TextField('Ghi chú')
    total = models.FloatField('Thành tiền')
    date_created = models.DateTimeField('Ngày nhập hàng', default=timezone.now)
    
    class Meta:
        db_table = 'InventoryReceivingVoucher'

class InventoryReceivingVoucherDetail(models.Model):
    receiving_voucher = models.ForeignKey(InventoryReceivingVoucher, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Số lượng')
    price = models.FloatField('Giá nhập')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'InventoryReceivingVoucherDetail'

class InventoryVoucher(models.Model):
    voucher_id = models.AutoField('Mã phiếu kiểm kê', primary_key=True)
    # status = models.CharField('Trạng thái', max_length=15)
    note = models.TextField('Ghi chú')
    date_created = models.DateTimeField('Ngày tạo phiếu kiểm kê', default=timezone.now)

    class Meta:
        db_table = 'InventoryVoucher'

class InventoryVoucherDetail(models.Model):
    inventory_voucher = models.ForeignKey(InventoryVoucher, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    quantity_before = models.PositiveIntegerField('Số lượng trước')
    quantity_after = models.PositiveIntegerField('Số lượng sau')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'InventoryVoucherDetail'

class WarehouseTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, null=True)
    inventory_receiving_detail = models.ForeignKey(InventoryReceivingVoucherDetail, on_delete=models.PROTECT, null=True)
    inventory_detail = models.ForeignKey(InventoryVoucherDetail, on_delete=models.PROTECT, null=True)
    change = models.IntegerField('Thay đổi')
    type = models.CharField("Loại biến động", max_length=30, choices=(
        ('order', 'Bán hàng'),
        ('inventory', 'Kiểm kê'),
        ('inventory_receiving', 'Nhập hàng'),
        ('refund', 'Trả hàng'),
    ))
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)

    class Meta:
        db_table = 'WarehouseTransaction'

class Promotion(models.Model):
    title = models.CharField('Tiêu đề của chương trình khuyến mãi', max_length=255)
    image = models.CharField('Hình ảnh', max_length=255)
    
    applicable_customer_groups = models.ManyToManyField(CustomerGroup, db_table='ApplicableCustomerGroup')

    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)

    status = models.BooleanField('Trạng thái')
    max_quantity = models.IntegerField('Số lần áp dụng tối đa')
    max_quantity_per_customer = models.IntegerField('Số lần áp dụng tối đa trên khách hàng')
    max_quantity_per_customer_per_day = models.IntegerField('Số lần áp dụng tối đa trên khách hàng trên 1 ngày')

    class Meta:
        db_table = 'Promotion'

class PromotionProductVoucher(models.Model):
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15, null=True)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    applicable_products = models.ManyToManyField(Product, db_table='ApplicableProduct')
    applicable_product_groups = models.ManyToManyField(ProductGroup, db_table='ApplicableProductGroup')
    quantity_buy = models.PositiveIntegerField('Số lượng sản phẩm cần mua')
    quantity_received = models.PositiveIntegerField('Số lượng sản phẩm được nhận')

    class Meta:
        db_table = 'PromotionProductVoucher'

class PromotionPercentVoucher(models.Model):
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15, null=True)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn')
    percent = models.FloatField('Phần trăm giảm giá')
    maximum_reduction_amount = models.FloatField('Số tiền được giảm tối đa')

    class Meta:
        db_table = 'PromotionPercentVoucher'

class PromotionFixedVoucher(models.Model):
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15, null=True)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn')
    reduction_amount = models.FloatField('Số tiền được giảm')

    class Meta:
        db_table = 'PromotionFixedVoucher'

class PromotionHistory(models.Model):
    product_voucher = models.ForeignKey(PromotionProductVoucher, on_delete=models.PROTECT, null=True)
    percent_voucher = models.ForeignKey(PromotionPercentVoucher, on_delete=models.PROTECT, null=True)
    fixed_voucher = models.ForeignKey(PromotionFixedVoucher, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, null=True)
    type = models.CharField('Loại khuyến mãi', max_length=15, choices=(
        ('Product', 'Tặng sản phẩm'),
        ('Percent', 'Giảm số tiền theo % hóa đơn'),
        ('Fixed', 'Giảm số tiền được định trước'),
    ))
    reduction_quantity = models.PositiveIntegerField('Số lượng sản phẩm được nhận', default=0)
    reduction_amount = models.FloatField('Số tiền được giảm', null=True)
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)

    class Meta:
        db_table = 'PromotionHistory'

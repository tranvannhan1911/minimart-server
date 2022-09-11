from sqlite3 import IntegrityError
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

class CustomerGroup(models.Model):
    name = models.CharField('Tên nhóm khách hàng', max_length=50)
    description = models.TextField('Mô tả nhóm khách hàng', blank=True)
    note = models.TextField('Ghi chú', blank=True)
    
    class Meta:
        db_table = 'CustomerGroup'

    def delete(self, using=None, keep_parents=False):
        if CustomerGroup.objects.filter(customer_group_detail=self.pk).exists():
            raise IntegrityError
        super().delete(using, keep_parents)

class User(AbstractUser):
    phone = models.CharField('Số điện thoại', max_length=15, unique=True)
    customer_group = models.ManyToManyField(CustomerGroup, db_table='CustomerGroupDetail', blank=True, related_name='customer_group_detail')
    fullname = models.CharField('Tên khách hàng', max_length=30, null=True)
    gender = models.CharField('Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    ))
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    note = models.TextField('Ghi chú', blank=True)
    
    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey("management.User", on_delete=models.PROTECT, 
    #     null=True, related_name="users_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey("management.User", on_delete=models.PROTECT, 
    #     null=True, related_name="users_updated")

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
        db_table = 'User'


class ProductGroup(models.Model):
    product_group_code = models.CharField('Mã nhóm sản phẩm', max_length=15)
    name = models.CharField('Tên nhóm sản phẩm', max_length=255)
    description = models.TextField('Mô tả nhóm sản phẩm', 
        help_text='Mô tả của nhóm sản phẩm', null=True)
    note = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ', null=True)
    
    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="product_group_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="product_group_updated")

    class Meta:
        db_table = 'ProductGroup'

class Supplier(models.Model):
    # supplier_id =  models.AutoField('Mã nhà cung cấp', primary_key=True)
    name = models.CharField('Tên nhà cung cấp', max_length=100)
    phone = models.CharField('Số điện thoại', max_length=15)
    email = models.CharField('Địa chỉ email', max_length=50, null=True)
    address = models.CharField('Địa chỉ', max_length=255, null=True)
    note = models.TextField('Ghi chú', help_text='Ghi chú nội bộ', null=True)

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="suppliers_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="suppliers_updated")

    class Meta:
        db_table = 'Supplier'

class HierarchyTree(models.Model):
    name = models.CharField('Tên cấp', max_length=50)
    level = models.IntegerField('Cấp', default=0)
    type = models.CharField('Loại', max_length=15, choices=(
        ("product", "Sản phẩm"),
    ))
    parent = models.ForeignKey("management.HierarchyTree", on_delete=models.CASCADE, null=True)

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="hierarchy_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="hierarchy_updated")

    class Meta:
        db_table = 'HierarchyTree'


class CalculationUnit(models.Model):
    # unit_id = models.AutoField('Mã đơn vị tính', primary_key=True)
    name = models.CharField('Tên đơn vị tính', max_length=50)

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="units_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="units_updated")
    class Meta:
        db_table = 'CalculationUnit'


class Product(models.Model):
    product_code = models.CharField('Mã sản phẩm', max_length=15, unique=True)
    name = models.CharField('Tên sản phẩm', max_length=255)
    description = models.TextField('Mô tả sản phẩm')
    image = models.CharField('Hình ảnh sản phẩm', max_length=255, blank=True)
    barcode = models.CharField('Mã vạch', max_length=15)
    barcode_image = models.CharField('Ảnh mã vạch', max_length=255)
    product_groups = models.ManyToManyField(ProductGroup, related_name='products', 
        db_table='ProductGroupDetail')
    product_category = models.ForeignKey(HierarchyTree, on_delete=models.PROTECT, 
        related_name='products', null=True)
    base_unit = models.ForeignKey(CalculationUnit, on_delete=models.CASCADE, verbose_name='Đơn vị cơ bản',
        help_text='Đơn vị cơ bản', null=True)

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="products_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="products_updated")
    
    class Meta:
        db_table = 'Product'

class UnitExchange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
        related_name='unitexchanges')
    unit = models.ForeignKey(CalculationUnit, on_delete=models.CASCADE,
        related_name='unitexchanges')
    value = models.PositiveIntegerField('Giá trị quy đổi',
        help_text='Đơn vị này bằng bao nhiêu đơn vị mặc định?')
    allow_sale = models.BooleanField('Đơn vị được phép bán hàng',
        help_text='Cho phép bán hàng bằng đơn vị này không?')

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="unit_exchange_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="unit_exchange_updated")

    class Meta:
        db_table = 'UnitExchange'
    
class PriceList(models.Model):
    name = models.CharField('Tên bảng giá', max_length=50, default="")    
    price_list_id = models.AutoField('Mã bảng giá', primary_key=True)
    start_date = models.DateTimeField('Thời gian bắt đầu',
        help_text='Thời gian bắt đâu áp dụng bảng giá', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc',
        help_text='Thời gian kết thúc áp dụng bảng giá', default=timezone.now)
    status = models.BooleanField('Trạng thái', default=True)

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="pricelists_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="pricelists_updated")
    
    class Meta:
        db_table = 'PriceList'

class PriceDetail(models.Model):
    pricelist = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Sản phẩm', on_delete=models.CASCADE,
        related_name='pricedetails', null=True)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        related_name='pricedetails', null=True)
    price = models.FloatField('Giá bán', default=0)
    start_date = models.DateTimeField('Thời gian bắt đầu', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)

    class Meta:
        db_table = 'PriceDetail'

class Order(models.Model):
    # order_id = models.AutoField('Mã đơn hàng', primary_key=True)
    note = models.TextField('Ghi chú')
    customer = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='orders', null=True)
    total = models.FloatField('Thành tiền', default=0)
    status = models.CharField('Trạng thái', max_length=15, default="pending", choices=(
        ('pending', 'Đang chờ'),
        ('complete', 'Hoàn tất'),
        ('cancel', 'Đã hủy đơn / hoàn trả')
    ))

    # date_created = models.DateTimeField('Ngày lập hóa đơn', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="orders_created")
    # date_updated = models.DateTimeField('Ngày cập nhật hóa đơn', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="orders_updated")

    class Meta:
        db_table = 'Order'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        null=True)
    price = models.ForeignKey(PriceDetail, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Số lượng')
    total = models.FloatField('Thành tiền', default=0)
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'OrderDetail'

class OrderRefund(models.Model):
    # refund_id = models.AutoField('Mã trả hàng', primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    staff = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú')

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="orders_refund_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="orders_refund_updated")
    
    class Meta:
        db_table = 'OrderRefund'

class OrderRefundDetail(models.Model):
    order_refund = models.ForeignKey(OrderRefund, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        null=True)
    quantity = models.PositiveIntegerField('Số lượng')
    note = models.TextField('Ghi chú')

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
    note = models.TextField('Ghi chú')
    total = models.FloatField('Thành tiền')
    
    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="inventory_receiving_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="inventory_receiving_updated")
    
    class Meta:
        db_table = 'InventoryReceivingVoucher'

class InventoryReceivingVoucherDetail(models.Model):
    receiving_voucher = models.ForeignKey(InventoryReceivingVoucher, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveIntegerField('Số lượng')
    price = models.FloatField('Giá nhập')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'InventoryReceivingVoucherDetail'

class InventoryVoucher(models.Model):
    # voucher_id = models.AutoField('Mã phiếu kiểm kê', primary_key=True)
    # status = models.CharField('Trạng thái', max_length=15)
    note = models.TextField('Ghi chú')
    status = models.CharField('Trạng thái', max_length=15, choices=(
        ("pending", "Chờ xác nhận"),
        ("complete", "Hoàn thành"),
        ("cancel", "Hủy"),
    ))
    
    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="inventory_created")
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="inventory_updated")
    
    class Meta:
        db_table = 'InventoryVoucher'

class InventoryVoucherDetail(models.Model):
    inventory_voucher = models.ForeignKey(InventoryVoucher, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, on_delete=models.PROTECT, null=True)
    quantity_before = models.PositiveIntegerField('Số lượng trước')
    quantity_after = models.PositiveIntegerField('Số lượng sau')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'InventoryVoucherDetail'

class WarehouseTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_exchange = models.ForeignKey(UnitExchange, on_delete=models.PROTECT, null=True)
    reference = models.CharField("Hóa đơn hoặc mã phiếu", max_length=30, null=True)

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
    description = models.TextField('Mô tả chương trình khuyến mãi', default="")
    image = models.CharField('Hình ảnh', max_length=255)
    
    applicable_customer_groups = models.ManyToManyField(CustomerGroup, db_table='ApplicableCustomerGroup')

    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)

    status = models.BooleanField('Trạng thái')

    # date_created = models.DateTimeField('Ngày tạo', default=timezone.now)
    # user_created = models.ForeignKey(User, on_delete=models.PROTECT, related_name="promotions_created", 
    #     null=True)
    # date_updated = models.DateTimeField('Ngày cập nhật', default=timezone.now)
    # user_updated = models.ForeignKey(User, on_delete=models.PROTECT, 
    #     null=True, related_name="promotions_updated")
    
    class Meta:
        db_table = 'Promotion'

class PromotionDetail(models.Model):
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15, null=True, unique=True)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    type = models.CharField('Loại khuyến mãi', max_length=15, choices=(
        ('Product', 'Khuyến mãi sản phẩm'),
        ('Percent', 'Khuyến mãi theo phần trăm hóa đơn'),
        ('Fixed', 'Khuyến mãi số tiền nhất định'),
    ))
    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng', default=timezone.now)
    end_date = models.DateTimeField('Thời gian kết thúc', default=timezone.now)
    status = models.BooleanField('Trạng thái')
    max_quantity = models.IntegerField('Số lần áp dụng tối đa', null=True)
    max_quantity_per_customer = models.IntegerField('Số lần áp dụng tối đa trên khách hàng', null=True)
    max_quantity_per_customer_per_day = models.IntegerField('Số lần áp dụng tối đa trên khách hàng trên 1 ngày', null=True)
    # Product
    applicable_products = models.ManyToManyField(Product, db_table='ApplicableProduct')
    applicable_product_groups = models.ManyToManyField(ProductGroup, db_table='ApplicableProductGroup')
    quantity_buy = models.PositiveIntegerField('Số lượng sản phẩm cần mua', null=True)
    quantity_received = models.PositiveIntegerField('Số lượng sản phẩm được nhận', null=True)
    # Percent
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn', null=True)
    percent = models.FloatField('Phần trăm giảm giá', null=True)
    maximum_reduction_amount = models.FloatField('Số tiền được giảm tối đa', null=True)
    # Fixed
    reduction_amount = models.FloatField('Số tiền được giảm', null=True)

    class Meta:
        db_table = 'PromotionDetail'

class PromotionHistory(models.Model):
    promotion_detail = models.ForeignKey(PromotionDetail, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, null=True)

    reduction_quantity = models.PositiveIntegerField('Số lượng sản phẩm được nhận', default=0, null=True)
    reduction_amount = models.FloatField('Số tiền được giảm', null=True)
    date_created = models.DateTimeField('Ngày tạo', default=timezone.now)

    class Meta:
        db_table = 'PromotionHistory'

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

    class Meta:
        db_table = 'History'

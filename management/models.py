from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
        db_table = 'TaiKhoan'

class CustomerType(models.Model):
    name = models.CharField('Tên nhóm khách hàng', max_length=50)
    description = models.TextField('Mô tả nhóm khách hàng')
    note = models.TextField('Ghi chú', blank=True)
    
    class Meta:
        db_table = 'CustomerType'


class Customer(models.Model):
    customer_id = models.CharField('Mã khách hàng', primary_key=True, 
        max_length=15)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(CustomerType, on_delete=models.PROTECT, null=True)
    fullname = models.CharField('Tên khách hàng', max_length=30)
    gender = models.CharField(verbose_name='Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    )),
    note = models.TextField('Ghi chú', blank=True)

    class Meta:
        db_table = 'Customer'

class Staff(models.Model):
    staff_id = models.CharField('Mã nhân viên', primary_key=True
        , max_length=15)
    fullname = models.CharField('Tên nhân viên', max_length=30)
    phone = models.CharField('Số điện thoại', max_length=15)
    cccd = models.CharField('Số căn cước công dân', max_length=15)
    address = models.CharField('Địa chỉ', max_length=255)
    gender = models.CharField(verbose_name='Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    )),
    day_of_birth = models.DateField('Ngày sinh', default='1900-01-01')
    email = models.CharField('Địa chỉ email', max_length=50)
    status = models.BooleanField('Trạng thái')

    class Meta:
        db_table = 'Staff'


class ProductType(models.Model):
    product_type_id = models.CharField('Mã loại sản phẩm', primary_key=True
        , max_length=15)
    product_type_name = models.CharField('Tên loại sản phẩm', max_length=255)
    description = models.TextField('Mô tả loại sản phẩm', 
        help_text='Mô tả của loại sản phẩm')
    note = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'ProductType'

class Supplier(models.Model):
    supplier_id =  models.CharField('Mã nhà cung cấp', primary_key=True
        , max_length=15)
    supplier_name = models.CharField('Tên nhà cung cấp', max_length=100)
    phone = models.CharField('Số điện thoại', max_length=15)
    email = models.CharField('Địa chỉ email', max_length=50)
    address = models.CharField('Địa chỉ', max_length=255)
    note = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'Supplier'


class Product(models.Model):
    product_id = models.CharField('Mã sản phẩm', primary_key=True
        , max_length=15)
    product_name = models.CharField('Tên sản phẩm', max_length=255)
    description = models.TextField('Mô tả sản phẩm')
    image = models.CharField('Hình ảnh sản phẩm', max_length=255, blank=True)
    barcode = models.CharField('Mã vạch', max_length=15)
    barcode_image = models.CharField('Ảnh mã vạch', max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, 
        related_name='products', null=True)

    class Meta:
        db_table = 'Product'


class Unit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
        related_name='units')
    unit_id = models.AutoField('Mã đơn vị tính', primary_key=True)
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
    product = models.ForeignKey(Product, verbose_name='Sản phẩm', on_delete=models.CASCADE,
        related_name='pricelists')
    unit = models.ForeignKey(Unit, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        related_name='pricelists')
    price = models.FloatField('Giá bán')
    start_date = models.DateTimeField('Thời gian bắt đầu',
        help_text='Thời gian bắt đâu áp dụng bảng giá')
    end_date = models.DateTimeField('Thời gian kết thúc',
        help_text='Thời gian kết thúc áp dụng bảng giá')

    class Meta:
        db_table = 'PriceList'


class Order(models.Model):
    order_id = models.CharField('Mã đơn hàng', primary_key=True, 
        max_length=15)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True)
    note = models.TextField('Ghi chú')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,
        related_name='orders', null=True)

    class Meta:
        db_table = 'Order'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.ForeignKey(PriceList, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Số lượng')
    total = models.FloatField('Thành tiền')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'OrderDetail'

class InventoryReceivingVoucher(models.Model):
    voucher_id = models.CharField('Mã phiếu nhập hàng', primary_key=True, 
        max_length=15)
    date_created = models.DateTimeField('Thời gian tạo')
    status = models.CharField('Trạng thái', max_length=15)
    note = models.TextField('Ghi chú')
    total = models.FloatField('Thành tiền')
    
    class Meta:
        db_table = 'InventoryReceivingVoucher'

class InventoryReceivingVoucherDetail(models.Model):
    receiving_voucher = models.ForeignKey(InventoryReceivingVoucher, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Số lượng')
    price = models.FloatField('Giá nhập')
    note = models.TextField('Ghi chú')

    class Meta:
        db_table = 'InventoryReceivingVoucherDetail'

class InventoryVoucher(models.Model):
    voucher_id = models.CharField('Mã phiếu kiểm kê', primary_key=True
        , max_length=15)
    date_created = models.DateTimeField('Thời gian tạo')
    status = models.CharField('Trạng thái', max_length=15)
    note = models.TextField('Ghi chú')

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


class Promotion(models.Model):
    promotion_code = models.CharField('Mã khuyến mãi', max_length=15)
    title = models.CharField('Tiêu đề của chương trình khuyến mãi', max_length=255)
    image = models.CharField('Hình ảnh', max_length=255)
    
    applicable_customer_types = models.ManyToManyField(CustomerType, db_table='ApplicableCustomerType')

    start_date = models.DateTimeField('Thời gian bắt đầu áp dụng')
    end_date = models.DateTimeField('Thời gian kết thúc')

    type = models.CharField('Loại khuyến mãi', max_length=15, choices=(
        ('Product', 'Tặng sản phẩm'),
        ('Percent', 'Giảm số tiền theo % hóa đơn'),
        ('Fixed', 'Giảm số tiền được định trước'),
    ))

    status = models.CharField('Trạng thái', max_length=15)
    max_quantity = models.IntegerField('Số lần áp dụng tối đa')
    max_quantity_per_customer = models.IntegerField('Số lần áp dụng tối đa trên khách hàng')
    max_quantity_per_customer_per_day = models.IntegerField('Số lần áp dụng tối đa trên khách hàng trên 1 ngày')

    class Meta:
        db_table = 'Promotion'

class PromotionProductVoucher(models.Model):
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    applicable_products = models.ManyToManyField(Product, db_table='ApplicableProduct')
    applicable_product_types = models.ManyToManyField(ProductType, db_table='ApplicableProductType')
    quantity_buy = models.PositiveIntegerField('Số lượng sản phẩm cần mua')
    quantity_received = models.PositiveIntegerField('Số lượng sản phẩm được nhận')

    class Meta:
        db_table = 'PromotionProductVoucher'

class PromotionPercentVoucher(models.Model):
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn')
    percent = models.FloatField('Phần trăm giảm giá')
    maximum_reduction_amount = models.FloatField('Số tiền được giảm tối đa')

    class Meta:
        db_table = 'PromotionPercentVoucher'

class PromotionFixedVoucher(models.Model):
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    minimum_total = models.FloatField('Số tiền tối thiểu trên hóa đơn')
    reduction_amount = models.FloatField('Số tiền được giảm')

    class Meta:
        db_table = 'PromotionFixedVoucher'
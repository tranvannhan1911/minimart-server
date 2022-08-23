from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, so_dien_thoai, password, **extra_fields):
        if not so_dien_thoai:
            raise ValueError('Số điện thoại không được để trống')
        user = self.model(so_dien_thoai=so_dien_thoai, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, so_dien_thoai, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(so_dien_thoai, password, **extra_fields)

class User(AbstractUser):
    so_dien_thoai = models.CharField('Số điện thoại', max_length=15, unique=True)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'so_dien_thoai'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.so_dien_thoai

    @staticmethod
    def check_exists(so_dien_thoai, is_active=None):
        if is_active == None:
            return User.objects.filter(so_dien_thoai=so_dien_thoai).exists()
        return User.objects.filter(so_dien_thoai=so_dien_thoai, is_active=is_active).exists()

    @staticmethod
    def format_phone(so_dien_thoai):
        if so_dien_thoai[:3] != "+84":
            if so_dien_thoai[0] == "0":
                so_dien_thoai = "+84"+so_dien_thoai[1:]
            else:
                so_dien_thoai = "+84"+so_dien_thoai
        return so_dien_thoai

    def convert_phone(so_dien_thoai):
        if so_dien_thoai[:3] == "+84":
            if so_dien_thoai[3] == "0":
                so_dien_thoai = so_dien_thoai[3:]
            else:
                so_dien_thoai = "0"+so_dien_thoai[3:]
        return so_dien_thoai

    @staticmethod
    def random_password():
        import string
        import random
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    class Meta:
        db_table = 'TaiKhoan'

class KhachHang(models.Model):
    ma_khach_hang = models.CharField('Mã khách hàng', primary_key=True, 
        max_length=15)
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE)
    ten_khach_hang = models.CharField('Tên khách hàng', max_length=30)
    gioi_tinh = models.CharField(verbose_name='Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    )),
    ghi_chu = models.TextField('Tên khách hàng', blank=True)

    class Meta:
        db_table = 'KhachHang'

class NhanVien(models.Model):
    ma_nhan_vien = models.CharField('Tên nhân viên', primary_key=True
        , max_length=15)
    ten_nhan_vien = models.CharField('Tên nhân viên', max_length=30)
    so_dien_thoai = models.CharField('Số điện thoại', max_length=15)
    so_cccd = models.CharField('Số căn cước công dân', max_length=15)
    dia_chi = models.CharField('Địa chỉ', max_length=255)
    gioi_tinh = models.CharField(verbose_name='Giới tính', max_length=1, default='U', choices=(
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không xác định'),
    )),
    ngay_sinh = models.DateField('Ngày sinh', default='1900-01-01')
    email = models.CharField('Địa chỉ email', max_length=50)
    trang_thai = models.BooleanField('Trạng thái')

    class Meta:
        db_table = 'NhanVien'

class DonHang(models.Model):
    ma_don_hang = models.CharField('Mã đơn hàng', primary_key=True, 
        max_length=15)
    ghi_chu = models.TextField('Ghi chú')
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.PROTECT)

    class Meta:
        db_table = 'DonHang'

class LoaiSanPham(models.Model):
    ma_loai_san_pham = models.CharField('Mã loại sản phẩm', primary_key=True
        , max_length=15)
    ten_loai_san_pham = models.CharField('Tên loại sản phẩm', max_length=255)
    mo_ta = models.TextField('Mô tả loại sản phẩm', 
        help_text='Mô tả của loại sản phẩm')
    ghi_chu = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'LoaiSanPham'

class NhaCungCap(models.Model):
    ma_ncc =  models.CharField('Mã nhà cung cấp', primary_key=True
        , max_length=15)
    ten_ncc = models.CharField('Tên nhà cung cấp', max_length=100)
    so_dien_thoai = models.CharField('Số điện thoại', max_length=15)
    email = models.CharField('Địa chỉ email', max_length=50)
    ma_so_thue = models.CharField('Địa chỉMã số thuế', max_length=20)
    dia_chi = models.CharField('Địa chỉ', max_length=255)
    ghi_chu = models.TextField('Ghi chú', 
        help_text='Ghi chú nội bộ')

    class Meta:
        db_table = 'NhaCungCap'


class SanPham(models.Model):
    ma_san_pham = models.CharField('Mã sản phẩm', primary_key=True
        , max_length=15)
    ten_san_pham = models.CharField('Tên sản phẩm', max_length=255)
    mo_ta = models.TextField('Mô tả sản phẩm')
    hinh_anh = models.CharField('Hình ảnh sản phẩm', max_length=255, blank=True)
    so_luong = models.PositiveIntegerField('Số lượng')
    ma_vach = models.CharField('Mã vạch', max_length=15)
    anh_ma_vach = models.CharField('Ảnh mã vạch', max_length=255)
    loai_san_pham = models.ForeignKey(LoaiSanPham, on_delete=models.PROTECT,
        related_name='ds_san_pham')
    nha_cung_cap = models.ForeignKey(NhaCungCap, on_delete=models.PROTECT,
        related_name='ds_san_pham')

    class Meta:
        db_table = 'SanPham'


class DonViTinh(models.Model):
    ma_don_vi = models.AutoField('Mã đơn vị tính', primary_key=True)
    don_vi = models.CharField('Tên đơn vị tính', max_length=30)
    gia_tri_quy_doi = models.PositiveIntegerField('Giá trị quy đổi',
        help_text='Đơn vị này bằng bao nhiêu đơn vị mặc định?')
    don_vi_mac_dinh_ban_hang = models.BooleanField('Đơn vị mặc định bán hàng',
        help_text='Là đơn vị mặc định để bán hàng hay không?')
    don_vi_mac_dinh = models.BooleanField('Đơn vị mặc định',
        help_text='Là đơn vị mặc định hay không (thường là đơn vị nhỏ nhất)')
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE,
        related_name='ds_don_vi_tinh')

    class Meta:
        db_table = 'DonViTinh'

class BienThe(models.Model):
    ma_bien_the = models.AutoField('Mã biến thể', primary_key=True)
    ten_bien_the = models.CharField('Tên biến thể', max_length=30)
    ma_vach = models.CharField('Mã vạch', max_length=15)
    anh_ma_vach = models.CharField('Ảnh mã vạch', max_length=255)
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE,
        related_name='ds_bien_the')

    class Meta:
        db_table = 'BienThe'

# class PhieuNhapHang(models.Model):
#     ma_phieu_nhap_hang = models.CharField('Mã phiếu nhập hàng', primary_key=True
#         , max_length=15)
    
class BangGia(models.Model):
    ma_bang_gia = models.AutoField('Mã bảng giá', primary_key=True)
    san_pham = models.ForeignKey(SanPham, verbose_name='Sản phẩm', on_delete=models.CASCADE,
        related_name='ds_bang_gia')
    bien_the = models.ForeignKey(BienThe, verbose_name='Biến thể', on_delete=models.CASCADE,
        related_name='ds_bang_gia')
    don_vi_tinh = models.ForeignKey(DonViTinh, verbose_name='Đơn vị tính', on_delete=models.CASCADE,
        related_name='ds_bang_gia')
    gia = models.FloatField('Giá bán')
    bat_dau = models.DateTimeField('Thời gian bắt đầu',
        help_text='Thời gian bắt đâu áp dụng bảng giá')
    ket_thuc = models.DateTimeField('Thời gian kết thúc',
        help_text='Thời gian kết thúc áp dụng bảng giá')


from django.db import models
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 10

    @property
    def stock_status(self):
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock <= 10:
            return 'low_stock'
        return 'available'

    @property
    def stock_label(self):
        s = self.stock_status
        if s == 'out_of_stock':
            return 'Out of Stock'
        elif s == 'low_stock':
            return 'Low Stock'
        return 'Available'


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    label = models.CharField(max_length=100)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.label}"


class ProductPerfectFor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='perfect_for_items')
    item = models.CharField(max_length=300)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.item}"


class Order(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    DELIVERY_PICKUP = 'pickup'
    DELIVERY_SEND = 'delivery'
    DELIVERY_CHOICES = [
        (DELIVERY_PICKUP, 'Ambil di Store'),
        (DELIVERY_SEND, 'Diantar'),
    ]

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    request_notes = models.TextField(blank=True)
    greeting_card = models.CharField(max_length=500, blank=True, default='-')
    paper_bags = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=200)
    customer_whatsapp = models.CharField(max_length=30)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default=DELIVERY_PICKUP)
    delivery_address = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pickup_date', 'pickup_time']

    def __str__(self):
        return f"{self.product_name} - {self.customer_name}"

    @property
    def due_datetime(self):
        if self.pickup_date and self.pickup_time:
            return datetime.combine(self.pickup_date, self.pickup_time)
        return None

    def get_time_until_due(self):
        if not self.pickup_date or not self.pickup_time:
            return ""
        from django.utils import timezone as tz
        import pytz
        try:
            now = datetime.now()
            due = self.due_datetime
            diff = due - now
            total_seconds = diff.total_seconds()
            if total_seconds < 0:
                return "Overdue"
            hours = int(total_seconds / 3600)
            minutes = int((total_seconds % 3600) / 60)
            if hours >= 24:
                days = int(hours / 24)
                return f"in {days} day{'s' if days > 1 else ''}"
            elif hours > 0:
                return f"in {hours} hr{'s' if hours > 1 else ''}"
            else:
                return f"in {minutes} min"
        except Exception:
            return ""

    @property
    def total_price(self):
        paper_bag_cost = self.paper_bags * 2000
        return self.price * self.quantity + paper_bag_cost


class Review(models.Model):
    reviewer_name = models.CharField(max_length=200)
    is_anonymous = models.BooleanField(default=False)
    content = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name = 'Anonymous' if self.is_anonymous else self.reviewer_name
        return f"Review by {name}"

    @property
    def display_name(self):
        return 'Anonymous' if self.is_anonymous else self.reviewer_name

    def get_time_ago(self):
        now = timezone.now()
        diff = now - self.created_at
        seconds = int(diff.total_seconds())
        if seconds < 60:
            return "just now"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} min ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hr{'s' if hours > 1 else ''} ago"
        days = hours // 24
        if days < 30:
            return f"{days} day{'s' if days > 1 else ''} ago"
        return self.created_at.strftime('%d %b %Y')


class SocialStats(models.Model):
    total_followers = models.IntegerField(default=0)
    prev_followers = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Social Stats'

    def __str__(self):
        return f"Social Stats ({self.total_followers} followers)"

    @property
    def followers_change_pct(self):
        if self.prev_followers == 0:
            return 0
        return round((self.total_followers - self.prev_followers) / self.prev_followers * 100)


class SOPSection(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class SOPItem(models.Model):
    section = models.ForeignKey(SOPSection, on_delete=models.CASCADE, related_name='items')
    content = models.TextField()
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} - item {self.order}"


class TermsSection(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TermsItem(models.Model):
    section = models.ForeignKey(TermsSection, on_delete=models.CASCADE, related_name='items')
    subtitle = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} - {self.subtitle}"


class AboutContent(models.Model):
    hero_image = models.ImageField(upload_to='about/', null=True, blank=True)
    content = models.TextField(default='')

    class Meta:
        verbose_name = 'About Content'

    def __str__(self):
        return "About Us Content"


class SiteSettings(models.Model):
    whatsapp_number = models.CharField(max_length=20, default='6287863912739')
    instagram_handle = models.CharField(max_length=100, default='@asari.bouquetflowerbdg')
    tiktok_handle = models.CharField(max_length=100, default='@asari.bouquetflowerbdg')
    address = models.TextField(default='Antapani, Bandung City')
    low_stock_threshold = models.IntegerField(default=10)
    order_template = models.TextField(
        default="""🌼 FORMAT PEMESANAN ASARI FLORIST 🌼
Haiii Kaaak! Silakan isi format di bawah ini yaaa 🤗
(Catatan: Mohon tidak mengubah teks yang dicetak tebal agar pesanan cepat terproses sistem)

📋 DETAIL PESANAN
*Nama Produk:* {product_name}
*Jumlah Produk:*
*Request:*
*Isi Kartu Ucapan (isi "-" jika kosongan):*
*Jumlah Paper Bag (+2000) (isi "0" jika tidak pakai):*

👤 INFORMASI PEMESAN
*Nama Pemesan:*
*No WhatsApp:*

🚚 JADWAL & PENGIRIMAN
*Tanggal Pengambilan (Contoh: Sabtu, 30 Mei 2026):*
*Jam Pengambilan (Contoh: 12.30 WIB):*
*Metode Penyerahan (Ketik: Ambil di Store / Diantar):*
*Alamat Pengiriman (Kosongkan jika diambil di store):*"""
    )

    class Meta:
        verbose_name = 'Site Settings'

    def __str__(self):
        return "Site Settings"

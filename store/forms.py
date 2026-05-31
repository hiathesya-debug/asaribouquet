from django import forms
from .models import (
    Product, ProductDetail, ProductPerfectFor,
    Order, Review, AboutContent, SiteSettings,
    SOPSection, SOPItem, TermsSection, TermsItem, SocialStats
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description', 'image', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Produk'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi produk...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = ['label', 'content', 'order']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Label (e.g. Main Flowers)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProductPerfectForForm(forms.ModelForm):
    class Meta:
        model = ProductPerfectFor
        fields = ['item', 'order']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfect for...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'product', 'product_name', 'quantity', 'request_notes',
            'greeting_card', 'paper_bags', 'customer_name', 'customer_whatsapp',
            'pickup_date', 'pickup_time', 'delivery_method', 'delivery_address',
            'price', 'status'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Produk'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'request_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Request khusus...'}),
            'greeting_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Isi kartu ucapan (atau "-")'}),
            'paper_bags': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pemesan'}),
            'customer_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. WhatsApp'}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Alamat pengiriman (kosongkan jika pickup)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False
        self.fields['product'].empty_label = "-- Pilih Produk (opsional) --"
        self.fields['request_notes'].required = False
        self.fields['delivery_address'].required = False


class OrderPriceForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['hero_image', 'content']
        widgets = {
            'hero_image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['whatsapp_number', 'instagram_handle', 'tiktok_handle', 'address', 'order_template']
        widgets = {
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_handle': forms.TextInput(attrs={'class': 'form-control'}),
            'tiktok_handle': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'order_template': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
        }


class SOPSectionForm(forms.ModelForm):
    class Meta:
        model = SOPSection
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SOPItemForm(forms.ModelForm):
    class Meta:
        model = SOPItem
        fields = ['section', 'content', 'link_text', 'link_url', 'order']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'link_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teks link (opsional)'}),
            'link_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL (opsional)'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TermsSectionForm(forms.ModelForm):
    class Meta:
        model = TermsSection
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TermsItemForm(forms.ModelForm):
    class Meta:
        model = TermsItem
        fields = ['section', 'subtitle', 'content', 'order']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SocialStatsForm(forms.ModelForm):
    class Meta:
        model = SocialStats
        fields = ['total_followers']
        widgets = {
            'total_followers': forms.NumberInput(attrs={'class': 'form-control'}),
        }

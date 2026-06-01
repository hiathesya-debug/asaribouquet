"""
seed_data.py — Asari Bouquet & Flower
Jalankan: python manage.py seed_data

Membuat:
  - 4 Kategori (Freshest Series, Flower Bouquet, Hand Bouquet, Flower Vase)
  - 4 Produk per kategori (16 total), nama "Bunga Mawar", harga Rp 1.000.000
  - 1 produk per kategori di-set out of stock (stock=0) untuk testing overlay
  - 1 AboutContent default
  - 1 SiteSettings default
  - Gambar produk diambil dari static/images/flower X.jpeg
"""

import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from store.models import Category, Product, AboutContent, SiteSettings


# ── Mapping: kategori → [indeks flower image (1-based)] ──────────────────────
CATEGORIES = [
    {
        'name': 'Freshest Series',
        'order': 1,
        'flower_indices': [1, 2, 3, 4],   # static/images/flower 1.jpeg, dll.
    },
    {
        'name': 'Flower Bouquet',
        'order': 2,
        'flower_indices': [5, 6, 7, 8],
    },
    {
        'name': 'Hand Bouquet',
        'order': 3,
        'flower_indices': [9, 10, 11, 12],
    },
    {
        'name': 'Flower Vase',
        'order': 4,
        'flower_indices': [13, 14, 15, 16],
    },
]

PRODUCT_NAME   = 'Bunga Mawar'
PRODUCT_PRICE  = 1_000_000
PRODUCT_STOCK  = 10          # stok normal
OOS_STOCK      = 0           # stok 0 → is_out_of_stock = True


class Command(BaseCommand):
    help = 'Seed data awal: kategori, produk, about, site settings'

    def handle(self, *args, **kwargs):
        self._seed_settings()
        self._seed_about()
        self._seed_products()
        self.stdout.write(self.style.SUCCESS('\n✅  Seed selesai!'))

    # ──────────────────────────────────────────────────────
    def _seed_settings(self):
        """SiteSettings — 1 baris singleton."""
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            obj.whatsapp_number    = '6287863912739'
            obj.instagram_handle   = '@asari.bouquetflowerbdg'
            obj.tiktok_handle      = '@asari.bouquetflowerbdg'
            obj.address            = 'Antapani, Bandung City'
            obj.save()
            self.stdout.write('  ✔  SiteSettings dibuat')
        else:
            self.stdout.write('  –  SiteSettings sudah ada, skip')

    # ──────────────────────────────────────────────────────
    def _seed_about(self):
        """AboutContent — 1 baris singleton."""
        obj, created = AboutContent.objects.get_or_create(pk=1)
        if created:
            obj.content = (
                "Asari Bouquet & Flower adalah florist rumahan yang berlokasi di "
                "Antapani, Kota Bandung. Kami menghadirkan rangkaian bunga segar dan "
                "elegan dengan sentuhan personal untuk setiap momen spesial Anda. "
                "Kami menawarkan berbagai produk bunga mulai dari hand bouquet, "
                "wedding bouquet, flower vase, hingga custom order dengan kualitas "
                "premium dan layanan yang penuh ketulusan.\n\n"
                "Setiap pesanan kami kerjakan dengan penuh perhatian dan cinta, "
                "karena kami percaya setiap bunga membawa cerita indah tersendiri. "
                "Jadikan momen Anda lebih berkesan bersama Asari Bouquet & Flower."
            )
            obj.save()
            self.stdout.write('  ✔  AboutContent dibuat')
        else:
            self.stdout.write('  –  AboutContent sudah ada, skip')

    # ──────────────────────────────────────────────────────
    def _seed_products(self):
        """Kategori + produk + gambar dari static/images."""
        static_images = Path(settings.BASE_DIR) / 'static' / 'images'
        media_products = Path(settings.MEDIA_ROOT) / 'products'
        media_products.mkdir(parents=True, exist_ok=True)

        for cat_data in CATEGORIES:
            # ── Buat/ambil kategori ──
            cat, cat_created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug':  slugify(cat_data['name']),
                    'order': cat_data['order'],
                }
            )
            label = '✔  Dibuat' if cat_created else '–  Sudah ada'
            self.stdout.write(f'\n  {label}: Kategori "{cat.name}"')

            # ── Buat 4 produk per kategori ──
            for i, flower_idx in enumerate(cat_data['flower_indices'], start=1):
                # Produk ke-1 per kategori → out of stock untuk testing
                stock = OOS_STOCK if i == 1 else PRODUCT_STOCK

                product_name = f'{PRODUCT_NAME} {flower_idx}'

                product, prod_created = Product.objects.get_or_create(
                    name=product_name,
                    category=cat,
                    defaults={
                        'price':       PRODUCT_PRICE,
                        'stock':       stock,
                        'description': (
                            f'Rangkaian bunga segar {cat_data["name"]} '
                            f'yang elegan dan tahan lama.'
                        ),
                        'is_featured': True,
                    }
                )

                if not prod_created:
                    self.stdout.write(f'    –  Produk "{product_name}" sudah ada, skip')
                    continue

                # ── Salin gambar dari static ke media ──
                src = static_images / f'flower {flower_idx}.jpeg'
                if src.exists():
                    dest_name = f'bunga-mawar-{flower_idx}.jpeg'
                    dest      = media_products / dest_name
                    shutil.copy2(src, dest)
                    product.image = f'products/{dest_name}'
                    product.save()
                    oos = ' [OUT OF STOCK]' if stock == 0 else ''
                    self.stdout.write(f'    ✔  "{product_name}"{oos} + gambar flower {flower_idx}')
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'    ⚠  "{product_name}" dibuat tanpa gambar '
                            f'(static/images/flower {flower_idx}.jpeg tidak ada)'
                        )
                    )
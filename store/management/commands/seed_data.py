import csv
import os
import urllib.request
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.core.files.base import ContentFile
from store.models import Product, Order, Category

class Command(BaseCommand):
    help = 'Load data dari file CSV (Products dan Orders) ke database'

    def handle(self, *args, **kwargs):
        # 1. IMPORT PRODUCT
        product_csv_path = os.path.join(settings.BASE_DIR, 'products_seed.csv')
        
        if os.path.exists(product_csv_path):
            with open(product_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Buat atau ambil objek Category terlebih dahulu
                    category_name = row['category']
                    category_obj, created = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'slug': slugify(category_name)}
                    )

                    # Simpan data produknya dulu (tanpa gambar)
                    product, prod_created = Product.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'category': category_obj,
                            'description': row['description'],
                            'price': row['price'],
                            'stock': 100,
                            'is_featured': True
                        }
                    )

                    # ==========================================
                    # PROSES AUTODOWNLOAD GAMBAR DARI URL (INTERNET)
                    # ==========================================
                    image_url = row['image_url']
                    
                    # Cek apakah kolom di CSV berisi link HTTP/HTTPS
                    if image_url.startswith('http'):
                        try:
                            # Request ke internet pura-pura jadi browser (Mozilla)
                            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req) as response:
                                # Kasih nama file berdasarkan nama produk, contoh: classic-red-rose-bouquet.jpg
                                file_name = f"{slugify(row['name'])}.jpg"
                                
                                # Simpan otomatis ke folder media/products lu
                                product.image.save(file_name, ContentFile(response.read()), save=True)
                                
                            self.stdout.write(f"  -> Sukses download gambar untuk: {product.name}")
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"  -> Gagal download gambar {product.name}: {e}"))
                    elif image_url:
                        # Kalau di CSV cuma nulis 'products/gambar.jpg' (File lokal)
                        product.image = image_url
                        product.save()

            self.stdout.write(self.style.SUCCESS('Berhasil import data Product!'))
        else:
            self.stdout.write(self.style.ERROR('File products_seed.csv tidak ditemukan.'))

        # 2. IMPORT ORDER (Sudah termasuk fix error " WIB" sebelumnya)
        order_csv_path = os.path.join(settings.BASE_DIR, 'orders_seed.csv')
        
        if os.path.exists(order_csv_path):
            with open(order_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = Product.objects.filter(name=row['product_name']).first()
                    
                    if product:
                        delivery_val = Order.DELIVERY_SEND if row['delivery_method'] == 'Diantar' else Order.DELIVERY_PICKUP
                        
                        status_val = Order.STATUS_IN_PROGRESS
                        if row['status'] == 'Done': 
                            status_val = Order.STATUS_DONE
                        elif row['status'] == 'Cancelled': 
                            status_val = Order.STATUS_CANCELLED

                        clean_time = row['pickup_time'].replace(' WIB', '').replace(' wib', '').strip()

                        Order.objects.create(
                            product=product,
                            product_name=row['product_name'], 
                            customer_name=row['customer_name'],
                            customer_whatsapp=row['whatsapp'], 
                            quantity=int(row['quantity']),
                            request_notes=row['request'], 
                            greeting_card=row['greeting_card'],
                            paper_bags=int(row['paper_bag']), 
                            pickup_date=row['pickup_date'],
                            pickup_time=clean_time,  
                            delivery_method=delivery_val,
                            delivery_address=row['address'], 
                            price=product.price, 
                            status=status_val
                        )
            self.stdout.write(self.style.SUCCESS('Berhasil import data Order!'))
        else:
            self.stdout.write(self.style.ERROR('File orders_seed.csv tidak ditemukan.'))
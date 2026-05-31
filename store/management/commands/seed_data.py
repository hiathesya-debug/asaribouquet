from django.core.management.base import BaseCommand
from store.models import (
    Category, SiteSettings, SocialStats,
    SOPSection, SOPItem, TermsSection, TermsItem, AboutContent
)


class Command(BaseCommand):
    help = 'Seed initial data for Asari Florist'

    def handle(self, *args, **options):
        self.stdout.write('🌸 Seeding initial data...')

        # ── Site Settings ──
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write('  ✓ SiteSettings created')
        else:
            self.stdout.write('  – SiteSettings already exists')

        # ── Social Stats ──
        SocialStats.objects.get_or_create(pk=1, defaults={'total_followers': 2205, 'prev_followers': 2000})
        self.stdout.write('  ✓ SocialStats ready')

        # ── Categories ──
        categories = [
            ('Flower Bouquet', 'flower-bouquet', 0),
            ('Hand Bouquet / Wedding Bouquet', 'hand-bouquet', 1),
            ('Flower Vase', 'flower-vase', 2),
            ('Custom Order', 'custom-order', 3),
        ]
        for name, slug, order in categories:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'order': order}
            )
            if created:
                self.stdout.write(f'  ✓ Category: {name}')

        # ── About Content ──
        about, created = AboutContent.objects.get_or_create(
            pk=1,
            defaults={
                'content': (
                    'Asari Bouquet & Flower adalah florist rumahan yang berlokasi di Antapani, '
                    'Kota Bandung. Kami menghadirkan rangkaian bunga segar dan elegan dengan '
                    'sentuhan personal untuk setiap momen spesial Anda.\n\n'
                    'Kami menawarkan berbagai produk bunga mulai dari hand bouquet, wedding bouquet, '
                    'flower vase, hingga custom order dengan kualitas premium dan layanan yang penuh '
                    'ketulusan. Setiap pesanan kami kerjakan dengan penuh perhatian dan cinta, '
                    'karena kami percaya setiap bunga membawa cerita indah tersendiri.'
                )
            }
        )
        if created:
            self.stdout.write('  ✓ AboutContent created')

        # ── SOP ──
        if not SOPSection.objects.exists():
            sop_data = [
                ('Order Taking', [
                    ('Pencatatan detail pesanan menggunakan format', 'copy here',
                     'https://wa.me/6287863912739'),
                    ('Pesanan baru akan diproses atau masuk antrean produksi setelah pembayaran awal '
                     '(DP) atau full payment diterima dan diverifikasi.', '', ''),
                ]),
                ('Production', [
                    ('Pastikan proporsi dan kombinasi warna sesuai dengan request pelanggan.', '', ''),
                    ('Gunakan teknik spiral untuk buket agar tangkai rapi dan kokoh.', '', ''),
                    ('Pasang water tube atau kapas basah pada ujung tangkai buket agar bunga tetap '
                     'segar selama pengiriman.', '', ''),
                    ('Sebelum di-lapisi kertas wrapping, cek kembali kesegaran bunga dan kesesuaian '
                     'dengan pesanan.', '', ''),
                    ('Sisipkan kartu ucapan di tempat yang mudah terlihat namun aman.', '', ''),
                ]),
                ('Hand Over', [
                    ('Foto produk yang sudah jadi sebagai arsip dan untuk dikirimkan kepada pelanggan '
                     'sebelum dikirim.', '', ''),
                    ('Kirimkan bukti pengiriman (foto tanda terima) kepada pelanggan.', '', ''),
                ]),
            ]
            for i, (section_title, items) in enumerate(sop_data):
                section = SOPSection.objects.create(title=section_title, order=i)
                for j, (content, link_text, link_url) in enumerate(items):
                    SOPItem.objects.create(
                        section=section,
                        content=content,
                        link_text=link_text,
                        link_url=link_url,
                        order=j
                    )
            self.stdout.write('  ✓ SOP sections and items created')

        # ── Terms & Conditions ──
        if not TermsSection.objects.exists():
            terms_data = [
                ('Order Rules', [
                    ('Order Placement',
                     'Please place your orders at least two days in advance (D-2) or as specified '
                     'in our Open Order announcements.'),
                    ('Availability',
                     'Last-minute orders are only accepted for ready-stock flowers.'),
                    ('Custom Orders',
                     'We highly recommend placing custom orders well in advance.'),
                    ('Purchasing Channels',
                     'Orders are exclusively processed via Instagram Direct Message (DM) or WhatsApp.'),
                    ('Location & Operations',
                     'We are based in Antapani, Bandung City. Please note that we operate exclusively '
                     'online and do not have a physical storefront.'),
                    ('Customer Service',
                     'Kindly expect delayed responses to messages sent outside of business hours or '
                     'on holidays.'),
                    ('Updates',
                     'Please refer to our Instagram Story for the latest information and updates.'),
                ]),
                ('Payment', [
                    ('Order Processing',
                     'Orders will only be added to our queue upon receipt of full payment or a down '
                     'payment (DP).'),
                    ('Down Payment',
                     'A minimum down payment of 50% is required to confirm your order. The remaining '
                     'balance must be settled before or on the day of delivery/pickup.'),
                    ('Payment Methods',
                     'We accept transfer via bank or e-wallet (BCA, Mandiri, GoPay, OVO, DANA).'),
                ]),
                ('Pickup & Delivery Rules', [
                    ('Schedule Changes',
                     'If you need to change your pickup day or time, please notify our admin '
                     'immediately via chat.'),
                    ('Delivery Area',
                     'Delivery is available within Bandung City and surrounding areas. Delivery '
                     'fees depend on the destination.'),
                    ('Packaging',
                     'All bouquets are carefully packaged to ensure freshness during delivery.'),
                ]),
                ('Disclaimer', [
                    ('Order Forms',
                     'Customers are requested to fill out the order form clearly and completely. '
                     'If there are any revisions, please notify us immediately.'),
                    ('Natural Products',
                     'Flowers are natural products. Slight color variations may occur between the '
                     'product photos and the actual product.'),
                    ('Cancellation',
                     'Cancellations after payment confirmation are not accepted. We will do our '
                     'best to accommodate reasonable requests.'),
                ]),
            ]
            for i, (section_title, items) in enumerate(terms_data):
                section = TermsSection.objects.create(title=section_title, order=i)
                for j, (subtitle, content) in enumerate(items):
                    TermsItem.objects.create(
                        section=section,
                        subtitle=subtitle,
                        content=content,
                        order=j
                    )
            self.stdout.write('  ✓ Terms & Conditions created')

        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete! Run: python manage.py runserver'))

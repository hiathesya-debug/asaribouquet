import json
import calendar
from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    Category, Product, ProductDetail, ProductPerfectFor,
    Order, Review, SocialStats, SOPSection, SOPItem,
    TermsSection, TermsItem, AboutContent, SiteSettings
)
from .forms import (
    ProductForm, ProductDetailForm, ProductPerfectForForm,
    OrderForm, OrderPriceForm, AboutContentForm, SiteSettingsForm,
    SOPSectionForm, SOPItemForm, TermsSectionForm, TermsItemForm,
    SocialStatsForm
)


# ─────────────────────────────────────────
# PUBLIC VIEWS
# ─────────────────────────────────────────

def home(request):
    categories = Category.objects.prefetch_related('products').all()
    about = AboutContent.objects.first()
    featured_products = Product.objects.filter(is_featured=True)[:6]

    cat_sections = []
    for cat in categories:
        products = cat.products.all()[:6]
        if products:
            cat_sections.append({'category': cat, 'products': products})

    context = {
        'cat_sections': cat_sections,
        'featured_products': featured_products,
        'about': about,
    }
    return render(request, 'public/home.html', context)


def product_categories(request):
    categories = Category.objects.all()
    return render(request, 'public/product_categories.html', {'categories': categories})


def product_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
        'total': products.count(),
    }
    return render(request, 'public/product_list.html', context)


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    context = {
        'query': query,
        'products': products,
        'total': products.count(),
    }
    return render(request, 'public/product_search.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    details = product.details.all()
    perfect_for = product.perfect_for_items.all()
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)

    # Build WhatsApp message
    wa_message = settings_obj.order_template.replace('{product_name}', product.name)

    context = {
        'product': product,
        'details': details,
        'perfect_for': perfect_for,
        'wa_message': wa_message,
        'wa_number': settings_obj.whatsapp_number,
    }
    return render(request, 'public/product_detail.html', context)


def about_us(request):
    about = AboutContent.objects.first()
    return render(request, 'public/about.html', {'about': about})


def terms_and_conditions(request):
    sections = TermsSection.objects.prefetch_related('items').all()
    return render(request, 'public/terms.html', {'sections': sections})


# ─────────────────────────────────────────
# ADMIN AUTH
# ─────────────────────────────────────────

def admin_login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Username atau password salah, atau tidak memiliki akses admin.')
    return render(request, 'admin_panel/login.html')


@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


# ─────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────

@login_required
def admin_dashboard(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Period filter
    period_month = int(request.GET.get('month', current_month))
    period_year = int(request.GET.get('year', current_year))

    month_name = datetime(period_year, period_month, 1).strftime('%B %Y')

    # Stats
    social_stats, _ = SocialStats.objects.get_or_create(pk=1)

    total_orders_this_month = Order.objects.filter(
        created_at__year=period_year,
        created_at__month=period_month
    ).count()

    total_orders_last_month = Order.objects.filter(
        created_at__year=period_year if period_month > 1 else period_year - 1,
        created_at__month=period_month - 1 if period_month > 1 else 12
    ).count()

    order_change_pct = 0
    if total_orders_last_month > 0:
        order_change_pct = round((total_orders_this_month - total_orders_last_month) / total_orders_last_month * 100)

    # Recent reviews (latest 5)
    recent_reviews = Review.objects.all()[:5]

    context = {
        'social_stats': social_stats,
        'total_orders': total_orders_this_month,
        'order_change_pct': order_change_pct,
        'recent_reviews': recent_reviews,
        'period_month': period_month,
        'period_year': period_year,
        'month_name': month_name,
        'all_months': [(i, datetime(2024, i, 1).strftime('%B')) for i in range(1, 13)],
        'followers_form': SocialStatsForm(instance=social_stats),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def get_sales_data(request):
    period_month = int(request.GET.get('month', timezone.now().month))
    period_year = int(request.GET.get('year', timezone.now().year))

    days_in_month = calendar.monthrange(period_year, period_month)[1]
    labels = list(range(1, days_in_month + 1))
    data = []

    for day in range(1, days_in_month + 1):
        total = Order.objects.filter(
            created_at__year=period_year,
            created_at__month=period_month,
            created_at__day=day,
            status=Order.STATUS_DONE
        ).aggregate(total=Sum('price'))['total'] or 0
        data.append(float(total))

    return JsonResponse({'labels': labels, 'data': data})


@login_required
def update_followers(request):
    if request.method == 'POST':
        stats, _ = SocialStats.objects.get_or_create(pk=1)
        new_val = request.POST.get('total_followers')
        if new_val:
            stats.prev_followers = stats.total_followers
            stats.total_followers = int(new_val)
            stats.save()
            messages.success(request, 'Followers berhasil diperbarui.')
    return redirect('admin_dashboard')


@login_required
def all_reviews(request):
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year', timezone.now().year)

    reviews = Review.objects.all()
    if month_filter:
        reviews = reviews.filter(
            created_at__month=int(month_filter),
            created_at__year=int(year_filter)
        )

    months = [(i, datetime(2024, i, 1).strftime('%B')) for i in range(1, 13)]
    context = {
        'reviews': reviews,
        'months': months,
        'selected_month': int(month_filter) if month_filter else None,
        'selected_year': int(year_filter),
    }
    return render(request, 'admin_panel/all_reviews.html', context)


# ─────────────────────────────────────────
# ADMIN PRODUCT MANAGEMENT
# ─────────────────────────────────────────

@login_required
def management_product(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    threshold = settings_obj.low_stock_threshold
    products = Product.objects.select_related('category').all()

    low_stock_products = [p for p in products if 0 < p.stock <= threshold]
    out_of_stock_products = [p for p in products if p.stock == 0]
    reminders = low_stock_products + out_of_stock_products

    context = {
        'products': products,
        'reminders': reminders,
    }
    return render(request, 'admin_panel/management_product.html', context)


@login_required
def product_add(request):
    form = ProductForm()
    detail_forms = [ProductDetailForm(prefix=f'detail_{i}') for i in range(3)]
    pf_forms = [ProductPerfectForForm(prefix=f'pf_{i}') for i in range(3)]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            # Save details
            idx = 0
            while f'detail_{idx}-label' in request.POST:
                label = request.POST.get(f'detail_{idx}-label', '').strip()
                content = request.POST.get(f'detail_{idx}-content', '').strip()
                if label and content:
                    ProductDetail.objects.create(product=product, label=label, content=content, order=idx)
                idx += 1

            # Save perfect-for
            idx = 0
            while f'pf_{idx}-item' in request.POST:
                item = request.POST.get(f'pf_{idx}-item', '').strip()
                if item:
                    ProductPerfectFor.objects.create(product=product, item=item, order=idx)
                idx += 1

            messages.success(request, f'Produk "{product.name}" berhasil ditambahkan.')
            return redirect('management_product')
        else:
            messages.error(request, 'Terdapat kesalahan pada form. Periksa kembali.')

    context = {'form': form, 'detail_forms': detail_forms, 'pf_forms': pf_forms, 'action': 'Tambah'}
    return render(request, 'admin_panel/product_form.html', context)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    existing_details = list(product.details.all())
    existing_pf = list(product.perfect_for_items.all())

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()

            # Clear and re-create details
            product.details.all().delete()
            idx = 0
            while f'detail_{idx}-label' in request.POST:
                label = request.POST.get(f'detail_{idx}-label', '').strip()
                content = request.POST.get(f'detail_{idx}-content', '').strip()
                if label and content:
                    ProductDetail.objects.create(product=product, label=label, content=content, order=idx)
                idx += 1

            product.perfect_for_items.all().delete()
            idx = 0
            while f'pf_{idx}-item' in request.POST:
                item = request.POST.get(f'pf_{idx}-item', '').strip()
                if item:
                    ProductPerfectFor.objects.create(product=product, item=item, order=idx)
                idx += 1

            messages.success(request, f'Produk "{product.name}" berhasil diperbarui.')
            return redirect('management_product')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')

    context = {
        'form': form,
        'product': product,
        'existing_details': existing_details,
        'existing_pf': existing_pf,
        'action': 'Edit',
    }
    return render(request, 'admin_panel/product_form.html', context)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Produk "{name}" berhasil dihapus.')
    return redirect('management_product')


# ─────────────────────────────────────────
# ADMIN ORDER MANAGEMENT
# ─────────────────────────────────────────

@login_required
def orders_view(request):
    status_filter = request.GET.get('status', 'in_progress')
    orders = Order.objects.filter(status=status_filter).select_related('product')

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
        'in_progress_count': Order.objects.filter(status='in_progress').count(),
        'done_count': Order.objects.filter(status='done').count(),
        'cancelled_count': Order.objects.filter(status='cancelled').count(),
    }
    return render(request, 'admin_panel/orders.html', context)


@login_required
def order_add(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Order "{order.product_name}" berhasil ditambahkan.')
            return redirect('orders')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    return render(request, 'admin_panel/order_form.html', {'form': form, 'action': 'Tambah'})


@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order berhasil diperbarui.')
            return redirect('orders')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    return render(request, 'admin_panel/order_form.html', {'form': form, 'order': order, 'action': 'Edit'})


@login_required
def order_update_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'status': new_status})
            messages.success(request, f'Status order diperbarui menjadi {order.get_status_display()}.')
    return redirect('orders')


@login_required
def order_update_price(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderPriceForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'price': str(order.price)})
            messages.success(request, 'Harga order berhasil diperbarui.')
            return redirect('orders')
    return redirect('orders')


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order berhasil dihapus.')
    return redirect('orders')


# ─────────────────────────────────────────
# ADMIN SOP
# ─────────────────────────────────────────

@login_required
def sop_view(request):
    sections = SOPSection.objects.prefetch_related('items').all()
    return render(request, 'admin_panel/sop.html', {'sections': sections})


@login_required
def sop_section_add(request):
    form = SOPSectionForm()
    if request.method == 'POST':
        form = SOPSectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seksi SOP berhasil ditambahkan.')
            return redirect('sop')
    return render(request, 'admin_panel/sop_form.html', {'form': form, 'title': 'Tambah Seksi SOP'})


@login_required
def sop_item_add(request):
    form = SOPItemForm()
    if request.method == 'POST':
        form = SOPItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item SOP berhasil ditambahkan.')
            return redirect('sop')
    return render(request, 'admin_panel/sop_form.html', {'form': form, 'title': 'Tambah Item SOP'})


@login_required
def sop_item_edit(request, pk):
    item = get_object_or_404(SOPItem, pk=pk)
    form = SOPItemForm(instance=item)
    if request.method == 'POST':
        form = SOPItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item SOP berhasil diperbarui.')
            return redirect('sop')
    return render(request, 'admin_panel/sop_form.html', {'form': form, 'title': 'Edit Item SOP'})


@login_required
def sop_item_delete(request, pk):
    item = get_object_or_404(SOPItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item SOP berhasil dihapus.')
    return redirect('sop')


# ─────────────────────────────────────────
# ADMIN MANAGEMENT WEBSITE
# ─────────────────────────────────────────

@login_required
def management_website(request):
    about = AboutContent.objects.first()
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    terms_sections = TermsSection.objects.prefetch_related('items').all()

    about_form = AboutContentForm(instance=about)
    settings_form = SiteSettingsForm(instance=settings_obj)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save_about':
            if about:
                about_form = AboutContentForm(request.POST, request.FILES, instance=about)
            else:
                about_form = AboutContentForm(request.POST, request.FILES)
            if about_form.is_valid():
                about_form.save()
                messages.success(request, 'Konten About Us berhasil diperbarui.')
                return redirect('management_website')

        elif action == 'save_settings':
            settings_form = SiteSettingsForm(request.POST, instance=settings_obj)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'Pengaturan situs berhasil diperbarui.')
                return redirect('management_website')

    context = {
        'about': about,
        'about_form': about_form,
        'settings_form': settings_form,
        'terms_sections': terms_sections,
    }
    return render(request, 'admin_panel/management_website.html', context)


@login_required
def terms_section_add(request):
    form = TermsSectionForm()
    if request.method == 'POST':
        form = TermsSectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seksi T&C berhasil ditambahkan.')
            return redirect('management_website')
    return render(request, 'admin_panel/terms_form.html', {'form': form, 'title': 'Tambah Seksi Terms'})


@login_required
def terms_item_add(request):
    form = TermsItemForm()
    if request.method == 'POST':
        form = TermsItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item T&C berhasil ditambahkan.')
            return redirect('management_website')
    return render(request, 'admin_panel/terms_form.html', {'form': form, 'title': 'Tambah Item Terms'})


@login_required
def terms_item_edit(request, pk):
    item = get_object_or_404(TermsItem, pk=pk)
    form = TermsItemForm(instance=item)
    if request.method == 'POST':
        form = TermsItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item T&C berhasil diperbarui.')
            return redirect('management_website')
    return render(request, 'admin_panel/terms_form.html', {'form': form, 'title': 'Edit Item Terms'})


@login_required
def terms_item_delete(request, pk):
    item = get_object_or_404(TermsItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item T&C berhasil dihapus.')
    return redirect('management_website')

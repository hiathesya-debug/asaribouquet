from django.urls import path
from . import views

urlpatterns = [
    # ─── Public ───
    path('', views.home, name='home'),
    path('products/', views.product_categories, name='product_categories'),
    path('products/<slug:slug>/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='product_search'),
    path('about/', views.about_us, name='about_us'),
    path('terms/', views.terms_and_conditions, name='terms'),

    # ─── Admin Auth ───
    path('admin-panel/login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),

    # ─── Admin Dashboard ───
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/dashboard/sales-data/', views.get_sales_data, name='get_sales_data'),
    path('admin-panel/dashboard/update-followers/', views.update_followers, name='update_followers'),
    path('admin-panel/dashboard/reviews/', views.all_reviews, name='all_reviews'),

    # ─── Admin Products ───
    path('admin-panel/products/', views.management_product, name='management_product'),
    path('admin-panel/products/add/', views.product_add, name='product_add'),
    path('admin-panel/products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-panel/products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # ─── Admin Orders ───
    path('admin-panel/orders/', views.orders_view, name='orders'),
    path('admin-panel/orders/add/', views.order_add, name='order_add'),
    path('admin-panel/orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('admin-panel/orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('admin-panel/orders/<int:pk>/price/', views.order_update_price, name='order_update_price'),
    path('admin-panel/orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # ─── Admin SOP ───
    path('admin-panel/sop/', views.sop_view, name='sop'),
    path('admin-panel/sop/section/add/', views.sop_section_add, name='sop_section_add'),
    path('admin-panel/sop/item/add/', views.sop_item_add, name='sop_item_add'),
    path('admin-panel/sop/item/<int:pk>/edit/', views.sop_item_edit, name='sop_item_edit'),
    path('admin-panel/sop/item/<int:pk>/delete/', views.sop_item_delete, name='sop_item_delete'),

    # ─── Admin Website Management ───
    path('admin-panel/website/', views.management_website, name='management_website'),
    path('admin-panel/website/terms/section/add/', views.terms_section_add, name='terms_section_add'),
    path('admin-panel/website/terms/item/add/', views.terms_item_add, name='terms_item_add'),
    path('admin-panel/website/terms/item/<int:pk>/edit/', views.terms_item_edit, name='terms_item_edit'),
    path('admin-panel/website/terms/item/<int:pk>/delete/', views.terms_item_delete, name='terms_item_delete'),
]

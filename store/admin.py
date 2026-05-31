from django.contrib import admin
from .models import (
    Category, Product, ProductDetail, ProductPerfectFor,
    Order, Review, SocialStats, SOPSection, SOPItem,
    TermsSection, TermsItem, AboutContent, SiteSettings
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductPerfectFor)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(SocialStats)
admin.site.register(SOPSection)
admin.site.register(SOPItem)
admin.site.register(TermsSection)
admin.site.register(TermsItem)
admin.site.register(AboutContent)
admin.site.register(SiteSettings)

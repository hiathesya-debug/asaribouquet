from .models import SiteSettings, Category


def global_context(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    categories = Category.objects.all()
    return {
        'site_settings': settings_obj,
        'nav_categories': categories,
    }

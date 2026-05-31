from django import template

register = template.Library()


@register.filter
def rupiah(value):
    """Format number as Indonesian Rupiah without prefix (prefix added in template)"""
    try:
        val = int(float(value))
        # Format with dot as thousands separator (Indonesian style)
        formatted = f"{val:,}".replace(',', '.')
        return formatted
    except (ValueError, TypeError):
        return value


@register.filter
def time_ago(review):
    """Get relative time for a review"""
    return review.get_time_ago()


@register.filter
def due_time(order):
    """Get relative due time for an order"""
    return order.get_time_until_due()


@register.filter
def abs_val(value):
    """Return absolute value"""
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value


@register.filter
def intcomma(value):
    """Format integer with thousands separators (dot for Indonesian)"""
    try:
        val = int(float(value))
        return f"{val:,}".replace(',', '.')
    except (ValueError, TypeError):
        return value


@register.filter
def split(value, delimiter=' '):
    """Split a string by delimiter"""
    return value.split(delimiter)

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def format_rupiah(value):
    try:
        value = float(value)
        return f"Rp {value:,.2f}".replace(",", ".")
    except (ValueError, TypeError):
        return value

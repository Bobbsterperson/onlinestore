from django import template

register = template.Library()

@register.filter
def discount_price(price, discount):
    if discount:
        return round(price - (price * discount / 100), 2)
    return price

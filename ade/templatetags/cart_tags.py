from django import template

register = template.Library()

@register.filter(name='cart_item_count')
def cart_item_count(cart):
    if not cart:
        return 0
    return sum(item.get('quantity', 0) for item in cart.values())

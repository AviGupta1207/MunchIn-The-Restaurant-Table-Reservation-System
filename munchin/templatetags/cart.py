from django import template
from munchin.models import FoodItem


register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(FoodItem,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == FoodItem.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(FoodItem, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == FoodItem.id:
            return cart.get(id)
    return 0;

@register.filter(name='price_total')
def price_total(FoodItem,cart):
    return FoodItem.price * cart_quantity(FoodItem,cart)


@register.filter(name='total_cart_price')
def total_cart_price(fooditems, cart):
    sum = 0;
    for p in fooditems:
        sum += price_total(p,cart)
    return sum
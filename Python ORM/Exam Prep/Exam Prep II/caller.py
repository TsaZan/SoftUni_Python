import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Sum, F

from main_app.models import Profile, Product, Order


# Create queries within functions
def get_profiles(search_string=None):
    if search_string is None:
        return ""

    new_string = (Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string))

    profiles = Profile.objects.filter(new_string).annotate(order_count=Count('order_profile'))

    if not profiles:
        return ""
    result = []

    for p in profiles.order_by('full_name'):
        result.append(
            f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_count}')

    return '\n'.join(result)


def get_loyal_profiles():
    loyal_profiles = Profile.objects.annotate(order_count=Count('order_profile')).filter(order_count__gt=2)

    if not loyal_profiles:
        return ""
    result = []

    for p in loyal_profiles.order_by('-order_count'):
        result.append(
            f'Profile: {p.full_name}, orders: {p.order_count}')

    return '\n'.join(result)


# print(get_loyal_profiles())

def get_last_sold_products():
    if not Order.objects.all().exists():
        return ""

    last_order = Order.objects.all().last()

    products = []

    for p in last_order.products.all().order_by('name'):
        products.append(p.name)

    return f"Last sold products: {', '.join(products)}"


# print(get_last_sold_products())

def get_top_products():
    products = Product.objects.annotate(qty_sold=Count('order_products')).filter(qty_sold__gt=0).order_by('-qty_sold', 'name')[:5]

    if not Order.objects.all():
        return ""

    result = ['Top products:']

    for p in products.all():
        result.append(f'{p.name}, sold {p.qty_sold} times')
    return '\n'.join(result)

#
# print(get_top_products())

def apply_discounts():
    orders = Order.objects.annotate(count=Count('products')).filter(is_completed=False, count__gt=2)
    order_count = orders.count()
    orders.update(total_price = F('total_price') * 0.9)

    return f"Discount applied to {order_count if order_count > 0 else 0} orders."

# print(apply_discounts())

def complete_order():
    if not Order.objects.all():
        return ""

    oldest_order = Order.objects.filter(is_completed=False).first()

    if not oldest_order:
        return ""

    for p in oldest_order.products.all():
        p.in_stock -= 1
        p.save()
        if p.in_stock == 0:
            p.is_available = False
            p.save()
    oldest_order.is_completed = True
    oldest_order.save()
    return "Order has been completed!"

# print(complete_order())

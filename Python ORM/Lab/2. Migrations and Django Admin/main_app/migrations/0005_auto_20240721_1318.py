import random

from django.db import migrations, models


def add_barcode(apps, schema_editor):
    Product = apps.get_model('main_app', 'Product')
    all_products = Product.objects.all()
    barcodes = random.sample(
        range(100000000, 999999999),
        len(all_products)
    )

    for i in range(len(all_products)):
        product = all_products[i]
        product.barcode = barcodes[i]
        product.save()


def reverse_barcode(apps, schema_editor):
    Product = apps.get_model('main_app', 'Product')
    for product in Product.objects.all():
        product.barcode = 0
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0004_remove_product_count_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RunPython(add_barcode,
                             reverse_code=reverse_barcode)]

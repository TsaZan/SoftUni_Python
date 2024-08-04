from django.core.exceptions import ValidationError


def category_validator(value):
    valid_categories = ["Appetizers", "Main Course", "Desserts"]

    for c in valid_categories:
        if c.lower() not in value.lower():
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
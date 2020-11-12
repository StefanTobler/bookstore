from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value) is not a positive number.')
        )
def validate_rating(value):
    if not 0 <= value <= 5:
        raise ValidationError(
            _(f'{value} is not in the range [0,5].')
        )

def validate_isbn(value):
    if len(value) < 10:
        raise ValidationError(
            _('%(value) is not a valid ISBN number.')
        )
    elif len(value) == 14 and value.count('-') != 1:
        raise ValidationError(
            _('%(value) is not a valid ISBN number.')
        )

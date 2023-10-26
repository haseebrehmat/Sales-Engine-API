from django.core.validators import RegexValidator

source_validator = RegexValidator(
    regex='^[a-zA-Z0-9]+$',
    message='Source should contain only alphabetic or numeric characters (no spaces or special characters).'
)

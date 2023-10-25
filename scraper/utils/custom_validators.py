from django.core.validators import RegexValidator

source_validator = RegexValidator(
    regex='^[a-zA-Z]+$',
    message='Source should contain only alphabetic characters (no spaces or special characters).'
)

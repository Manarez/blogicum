from django.utils import timezone
from django.contrib.auth import get_user_model

CHAR_LENGTH = 256

PAGINATE_BY = 10

TODAY = timezone.now()

USER = get_user_model()

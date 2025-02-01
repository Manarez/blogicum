from datetime import datetime

from django.contrib.auth import get_user_model

CHAR_LENGTH = 256

PAGINATE_BY = 10

TODAY = datetime.today()

USER = get_user_model()

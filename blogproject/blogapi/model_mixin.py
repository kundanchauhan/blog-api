from django.db import models
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import lazy
from django.utils.regex_helper import _lazy_re_compile


class CreateAndUpdateTimeStampMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True




from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
import uuid
from djchoices import DjangoChoices, ChoiceItem

from .model_mixin import CreateAndUpdateTimeStampMixin



class StateChoices(DjangoChoices):
    """Choices for blog state"""
    Published = ChoiceItem('Published','Published')
    Draft = ChoiceItem('Draft', 'Draft')
    Archived = ChoiceItem('Archived','Archived')

class ActionChoices(DjangoChoices):
    """Choices for blog state"""
    Created = ChoiceItem('Created', 'Created')
    Edited = ChoiceItem('Edited', 'Edited')
    Deleted = ChoiceItem('Deleted', 'Deleted')



class BlogUser(CreateAndUpdateTimeStampMixin):
    # id = models.IntegerField(primary_key=True, blank=True, null=False)
    username = models.CharField(unique=True, max_length=60, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=75, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Blog User')
        verbose_name_plural = _('Blog Users')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_authenticated(self):
        return True


class CreatePost(CreateAndUpdateTimeStampMixin):
    user = models.ForeignKey(BlogUser, related_name='user_details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=50, choices=StateChoices, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f'{self.user.username} {self.state}'

    @property
    def is_authenticated(self):
        return True


class Logger(CreateAndUpdateTimeStampMixin):
    log = models.ForeignKey(CreatePost, related_name='logger_blog_details', on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ActionChoices, null=True)

    class Meta:
        verbose_name = _('Logger')
        verbose_name_plural = _('Loggers')




class CountHistory(CreateAndUpdateTimeStampMixin):
    hit_count = models.IntegerField(null=True)
    user = models.ForeignKey(BlogUser, related_name='user_hit_details', on_delete=models.CASCADE)


    class Meta:
        verbose_name = _('CountHistory')
        verbose_name_plural = _('CountHistorys')

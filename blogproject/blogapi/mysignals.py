from django.db.models.signals import post_save, pre_save, post_delete,pre_delete,m2m_changed
from .models import BlogUser, CreatePost, Logger
from django.dispatch import receiver







@receiver(post_save, sender=CreatePost)
def blog_saved(sender, instance, created, **kwargs):
    if created:
        Logger.objects.create(log=instance, action='Created')
    else:
        Logger.objects.create(log=instance, action='Edited')



@receiver(pre_delete, sender=CreatePost)
def blog_deleted(sender, instance, **kwargs):

    Logger.objects.create(log=instance, action='Deleted')




from django.contrib import admin
# Register your models here.

from .models import BlogUser, CreatePost, Logger, CountHistory


class BlogUserAdmin(admin.ModelAdmin):

    list_display = ('id','username', 'email', 'first_name', 'last_name')
    list_filter = ('email',)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs.update({
                'exclude': getattr(kwargs, 'exclude', tuple()) + ('password',),
            })
        return super(BlogUserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(BlogUser, BlogUserAdmin)


class PostAdmin(admin.ModelAdmin):

    list_display = ('id','user', 'title', 'description', 'state')
    list_filter = ('user',)


admin.site.register(CreatePost, PostAdmin)


class LoggerAdmin(admin.ModelAdmin):

    list_display = ('log', 'action')
    list_filter = ('log',)


admin.site.register(Logger, LoggerAdmin)



class CountHistoryAdmin(admin.ModelAdmin):

    list_display = ('hit_count','user')
    list_filter = ('hit_count','user')


admin.site.register(CountHistory, CountHistoryAdmin)
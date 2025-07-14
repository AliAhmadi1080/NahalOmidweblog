from django.contrib import admin
from .models import *


class AdminBlog(admin.ModelAdmin):
    list_display = ('id', 'titel', 'date', 'author', 'like_count')
    list_filter = ('author', 'titel')
    list_display_links = ('id',)
    readonly_fields = ('date', 'like_count')

    fieldsets = [
        (
            ('اطلاعات'),
            {
                "fields": ['titel', 'author'],
            },

        ),
        (
            ('بدنه'),
            {
                'fields': ['sub_titel', 'categorys', 'text', 'image']
            }
        ),
        (
            ('کاربر'),
            {
                'fields': ['like_count', 'date']
            }
        ),
    ]

    add_fieldsets = (
        (
            ('اطلاعات'),
            {
                "fields": ['titel', 'author'],
            },
        ),
        (
            ('بدنه'),
            {
                'fields': ['sub_titel', 'categorys', 'text', 'image']
            }
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class AdminComment(admin.ModelAdmin):
    list_display = ('id', 'blog', 'status')
    list_display_links = ('id',)
    list_filter = ('status',)


class AdminConsultation(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status')
    list_display_links = ('id',)
    list_filter = ('status',)


class AdminSubscriber(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email')
    list_display_links = ('id',)


admin.site.register(Blog, AdminBlog)
admin.site.register(Categorys)
admin.site.register(Comment, AdminComment)
admin.site.register(Like)
admin.site.register(Consultation, AdminConsultation)
admin.site.register(Subscriber, AdminSubscriber)

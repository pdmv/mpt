from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from .models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.db.models import Count


class CourseAdminSite(admin.AdminSite):
    site_header = "yourCourse"

    def get_urls(self):
        return [
                   path('course-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()
        stats = Course.objects.annotate(lesson_count=Count('lesson__id')).values('id', 'subject', 'lesson_count')
        return TemplateResponse(request,
                                'admin/stats.html', {
                                    'course_count': count,
                                    'course_stats': stats
                                })


admin_site = CourseAdminSite(name="site")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class CourseForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    readonly_fields = ['img']
    form = CourseForm

    def img(self, course):
        if course:
            return mark_safe('<img src="/static/{url}" width="120" />'.format(url=course.image.name))


# Register your models here.
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Tag)

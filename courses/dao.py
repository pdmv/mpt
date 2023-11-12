from .models import Category, Course
from django.db.models import Count


def load_course(param={}):
    q = Course.objects.filter(active=True)

    kw = param.get('kw')
    if kw:
        q = q.filter(subject__icontains=kw)

    cate_id = param.get('cate_id')
    if cate_id:
        q = q.filter(category_id=cate_id)

    return q


def count_courses_by_cate():
    return Category.objects.annotate(count=Count('course__id')).value("id", "name", "count").order_by("count")

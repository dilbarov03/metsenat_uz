from random import choices
from django_filters import rest_framework as filters
from api.models import Sponsor, University


class SponsorFilter(filters.FilterSet):
    STATUS_CHOICES = (
        ("Yangi", "Yangi"),
        ("Moderiyatsada", "Moderiyatsada"),
        ("Tasdiqlangan", "Tasdiqlangan"),
        ("Bekor qilingan", "Bekor qilingan")
    )

    summa = filters.NumberFilter(field_name="summa")
    status = filters.ChoiceFilter(field_name="status", choices=STATUS_CHOICES)
    date_created = filters.DateFromToRangeFilter(field_name="date_created")


    class Meta:
        model = Sponsor
        fields = ['summa', 'status', 'date_created']

class StudentFilter(filters.FilterSet):
    STUDENT_TYPES = (
        ("Bakalavr", "Bakalavr"),
        ("Magistr", "Magistr")
    )

    student_type = filters.ChoiceFilter(field_name="student_type", choices=STUDENT_TYPES)
    university = filters.ModelChoiceFilter(field_name="university", queryset=University.objects.all())
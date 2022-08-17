from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

class Sponsor(models.Model):
    PERSON_CHOICES = (
        ("Jismoniy shaxs", "Jismoniy shaxs"),
        ("Yuridik shaxs", "Yuridik shaxs")
    )

    STATUS_CHOICES = (
        ("Yangi", "Yangi"),
        ("Moderiyatsada", "Moderiyatsada"),
        ("Tasdiqlangan", "Tasdiqlangan"),
        ("Bekor qilingan", "Bekor qilingan")
    )

    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=56)
    summa = models.IntegerField()
    person_type = models.CharField(max_length=128, choices=PERSON_CHOICES)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default="Yangi")
    company_name = models.CharField(max_length=128, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class University(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Student(models.Model):
    STUDENT_TYPES = (
        ("Bakalavr", "Bakalavr"),
        ("Magistr", "Magistr")
    )

    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=56)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="students")
    student_type = models.CharField(max_length=56, choices=STUDENT_TYPES)
    contract_amount = models.IntegerField()  #kontrakt narxi
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name

class Funding(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="funding")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="funding")
    amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

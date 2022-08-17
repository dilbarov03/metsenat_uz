from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Sponsor, Student, Funding, University
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count
from rest_framework.generics import get_object_or_404

class SponsorSerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ["id", "full_name", "phone", "summa", "spent_money", "date_created", "status"]

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.funding.aggregate(money_sum=Coalesce(Sum('amount'), 0))['money_sum']
        return spent_money

class SponsorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["name"]

class StudentSerializer(serializers.ModelSerializer):
    gained_money = serializers.SerializerMethodField()
    university = UniversitySerializer(read_only=True)
    class Meta:
        model = Student
        fields = ["id", "full_name", "student_type", "university", "gained_money", "contract_amount"]

    @staticmethod
    def get_gained_money(student):
        gained_money = student.funding.aggregate(money_sum=Coalesce(Sum('amount'), 0))['money_sum']
        return gained_money

class StudentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class FundingSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    
    class Meta:
        model = Funding
        fields = ["student", "student_id", "sponsor", "sponsor_id", "amount"]

    def create(self, validated_data):
        sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))
        student = get_object_or_404(Student, id=validated_data.get('student_id'))
        amount = validated_data.get('amount')

        sponsor_spent_money = sponsor.funding.aggregate(money_sum=Coalesce(Sum('amount'), 0))['money_sum']
        student_gained_money = student.funding.aggregate(money_sum=Coalesce(Sum('amount'), 0))['money_sum']
        sponsor_balance = sponsor.summa - sponsor_spent_money

        if amount <= sponsor_balance:
            if student_gained_money + amount <= student.contract_amount:
                sponsorship = Funding.objects.create(**validated_data)
                return sponsorship
            else:
                raise ValidationError({'error': 'Homiylik puli kontrakt miqdoridan ochib ketdi'})
        else:
            raise ValidationError({'error': 'Homiyda yetarli pul mavjud emas.'})

    def update(self, instance, validated_data):
        sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))
        student = instance.student
        amount = validated_data["amount"]

        sponsor_spent_money = \
            sponsor.funding.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        student_gained_money = \
            student.funding.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        sponsor_balance = sponsor.money - sponsor_spent_money

        if amount <= sponsor_balance:
            if student_gained_money + amount <= student.contract_amount:
                instance.amount = amount
                instance.sponsor = sponsor
                instance.save()
                return instance
            else:
                raise ValidationError({'error': 'Homiylik puli kontrakt miqdoridan oshib ketdi'})
        else:
            raise ValidationError({"error": "Homiyda yetarli mablag' mavjud emas"})



class FundingSponsorSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Funding
        fields = ['id', 'student', 'amount']

    @staticmethod
    def get_student(funding):
        data = {
            'id': funding.student.id,
            'full_name': funding.student.full_name
        }
        return data

class FundingStudentSerializer(serializers.ModelSerializer):
    sponsor = serializers.SerializerMethodField()

    class Meta:
        model = Funding
        fields = ['id', 'sponsor', 'amount']

    @staticmethod
    def get_sponsor(funding):
        data = {
            'id': funding.sponsor.id,
            'full_name': funding.sponsor.full_name
        }
        return data

class DashboardMoneySerializer:
    def __init__(self):
        self.total_sponsored_money = Funding.objects.aggregate(Sum('amount'))['amount__sum']
        self.total_contract_money = Student.objects.aggregate(Sum('contract_amount'))['contract_amount__sum']
        self.total_needed_money = self.total_contract_money - self.total_sponsored_money

    @property
    def data(self):
        return self.__dict__


class DashboardGraphSerializer:
    def __init__(self):
        self.sponsors_stats = Sponsor.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')
        self.students_stats = Student.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')

    @property
    def data(self):
        return self.__dict__
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .filters import *
from .models import Sponsor, Student, Funding


class SponsorListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'company_name']
    filterset_class = SponsorFilter


class SponsorCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorPostSerializer

class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer



class StudentListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'university__name']
    filterset_class = StudentFilter

class StudentCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentPostSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentPostSerializer



class FundingListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer

class FundingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer

class FundingSponsorView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FundingSponsorSerializer
    
    def get_queryset(self):
        sponsor = get_object_or_404(Sponsor, id=self.kwargs['pk'])
        queryset = sponsor.funding.all()
        return queryset

class FundingStudentView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FundingStudentSerializer
    
    def get_queryset(self):
        student = get_object_or_404(Student, id=self.kwargs['pk'])
        queryset = student.funding.all()
        return queryset

class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        dashboard_money_serializer = DashboardMoneySerializer()
        dashboard_graph_serializer = DashboardGraphSerializer()
        return Response(data={
            'money_stats': dashboard_money_serializer.data,
            'graph_stats': dashboard_graph_serializer.data
        })
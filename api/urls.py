from django.urls import include, path
from .views import *

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),

    path("sponsors/", SponsorListView.as_view()),
    path("sponsors/add/", SponsorCreateView.as_view()),
    path("sponsors/<int:pk>/", SponsorDetailView.as_view()),
    path("sponsors/<int:pk>/funding/", FundingSponsorView.as_view()),

    path("students/", StudentListView.as_view()),
    path("students/add/", StudentCreateView.as_view()),
    path("students/<int:pk>/", StudentDetailView.as_view()),
    path("students/<int:pk>/funding/", FundingStudentView.as_view()),

    path("fundings/", FundingListView.as_view()),
    path("fundings/<int:pk>/", FundingDetailView.as_view()),
]
from django.urls import path
from .views import DomainStatusView, DomainDetailView, DomainSuggestionView

urlpatterns = [
    path('status/', DomainStatusView.as_view(), name='domain_status'),
    path('details/', DomainDetailView.as_view(), name='domain_details'),
    path('recommend/', DomainSuggestionView.as_view(), name='domain_recommendation'),

]

from django.urls import path
from .views import DomainStatusView, DomainDetailView

urlpatterns = [
    path('status/', DomainStatusView.as_view(), name='domain_status'),
    path('details/', DomainDetailView.as_view(), name='domain_details'),

]

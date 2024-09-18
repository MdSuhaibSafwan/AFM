from django.urls import path
from faqs import views

app_name = 'faqs'

urlpatterns = [
     path('', views.list_faq, name='list-faq'),
     path('create/', views.create_faq, name='faq-create'),
     path('faq_detail/<int:pk>/', views.FaqDetailView.as_view(), name='faq-detail'),
     path('edit/<int:pk>/', views.edit_faq, name='faq-update'),
     path('faq_delete/<int:pk>', views.FaqDeleteView.as_view(), name='faq-delete'),
]

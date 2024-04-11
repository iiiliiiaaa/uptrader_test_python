from django.urls import path
from .views import MenuPageView, PendantPageView

urlpatterns = [
    # Для именованных URL:
    path('pendant/', PendantPageView.as_view(), name='pendant-view'),  # test for named url

    # Для обычных URL:
    path('<str:menu_name>/', MenuPageView.as_view(), name='menu-view'),
    path('', MenuPageView.as_view(), name='default-menu-view'),
]

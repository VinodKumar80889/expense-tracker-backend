from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, summary
router=DefaultRouter()
router.register("expenses",ExpenseViewSet,basename="expense")
urlpatterns=[path("",include(router.urls)),path("summary/",summary)]

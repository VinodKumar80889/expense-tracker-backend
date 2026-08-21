from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    def get_queryset(self):
        qs=super().get_queryset()
        q=self.request.query_params.get("q")
        category=self.request.query_params.get("category")
        if q: qs=qs.filter(description__icontains=q) | qs.filter(category__icontains=q)
        if category: qs=qs.filter(category__iexact=category)
        return qs.distinct()

@api_view(["GET"])
def summary(request):
    total=Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    by_category=list(Expense.objects.values("category").annotate(total=Sum("amount")).order_by("-total"))
    by_month=list(Expense.objects.annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).order_by("month"))
    return Response({"total":total,"count":Expense.objects.count(),"by_category":by_category,"by_month":by_month})

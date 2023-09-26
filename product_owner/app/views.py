from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import LessonSerializer
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField


class ProductLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(products__user_access=user)


class ProductLessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()


class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        return Product.objects.annotate(
            total_viewed_lessons=Count('lessons__lessonstatus'),
            total_view_time_sec=Sum('lessons__lessonstatus__view_time_sec'),
            total_students=Count('user_access', distinct=True),
            purchase_percentage=ExpressionWrapper(
                Count('user_access', distinct=True) * 100.0 / F('owner__count'),
                output_field=FloatField()
            )
        )
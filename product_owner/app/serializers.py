from rest_framework import serializers
from .models import Lesson, LessonStatus


class LessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStatus
        fields = ('view_time_sec', 'view_or_notview')


class LessonSerializer(serializers.ModelSerializer):
    status = LessonStatusSerializer(source='lessonstatus_set', many=True)

    class Meta:
        model = Lesson
        fields = ('name', 'link_video', 'duration_sec', 'status')


class LessonDetailSerializer(serializers.ModelSerializer):
    last_viewed = serializers.SerializerMethodField()

    def get_last_viewed(self, obj):
        request = self.context.get('request')
        lesson_status = LessonStatus.objects.filter(lesson=obj, user=request.user).order_by('-view_time_sec').first()
        if lesson_status:
            return lesson_status.view_time_sec
        return None

    class Meta:
        model = Lesson
        fields = ('name', 'link_video', 'duration_sec', 'status', 'last_viewed')


class ProductStatsSerializer(serializers.ModelSerializer):
    total_viewed_lessons = serializers.IntegerField()
    total_view_time_sec = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = ('name', 'total_viewed_lessons', 'total_view_time_sec', 'total_students', 'purchase_percentage')

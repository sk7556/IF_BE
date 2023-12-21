from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnlySchedule, IsOwnerOrReadOnlyPeriodEvent, IsOwnerOrReadOnlyDateEvent
from .models import Planners, PeriodEvents, DateEvents, DateEventPlaces
from .serializers import (
    PlannerSerializer, PeriodEventSerializer, DateEventSerializer,
    DateEventPlaceSerializer
)

# 최상위 Planner에 대한 CRUD 뷰
class PlannerViewSet(viewsets.ModelViewSet):
    queryset = Planners.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [AllowAny]

# PeriodEvent에 대한 CRUD 뷰
class PeriodEventViewSet(viewsets.ModelViewSet):
    queryset = PeriodEvents.objects.all()
    serializer_class = PeriodEventSerializer
    permission_classes = [AllowAny]

# DateEvent에 대한 CRUD 뷰
class DateEventViewSet(viewsets.ModelViewSet):
    queryset = DateEvents.objects.all()
    serializer_class = DateEventSerializer
    permission_classes = [AllowAny]

# DateEventPlace에 대한 CRUD 뷰
class DateEventPlaceViewSet(viewsets.ModelViewSet):
    queryset = DateEventPlaces.objects.all()
    serializer_class = DateEventPlaceSerializer
    permission_classes = [AllowAny]  # DateEventPlace에 대한 특별한 권한 체크가 필요하다면 추가

# 나머지 일반적인 기능을 수행하는 view들
class PlannerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Planners.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [AllowAny]

class PlannerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Planners.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [AllowAny]


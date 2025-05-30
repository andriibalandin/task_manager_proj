from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabelViewSet, CardViewSet, BoardViewSet, ListViewSet, CommentViewSet, IndexView

app_name = 'boards'

router = DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'cards', CardViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'lists', ListViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', IndexView.as_view(), name='index'),
]
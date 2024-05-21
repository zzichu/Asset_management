from django.urls import include, path
from rest_framework import routers
from .views import ItemViewSet, RentalStatistics, ReturnStatistics, RegisterStatistics, PDFConversionView

app_name = 'myapp'

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)
# router.register(r'qrcode', QRCodeViewSet, basename='qrcode')

urlpatterns = [
    path('', include(router.urls)),
    path('item/<str:pk>/return/', ItemViewSet.as_view({'put': 'return_update'}), name='item-return'),
    path('rental_statistics', RentalStatistics.as_view(), name='rental_statistics'),
    path('return_statistics', ReturnStatistics.as_view(), name='return_statistics'),
    path('register_statistics', RegisterStatistics.as_view(), name='register_statistics'),
    # path('myapp/items/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('convertPDF', PDFConversionView.as_view(), name='convertPDF'),
]

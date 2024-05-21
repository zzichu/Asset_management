from rest_framework import serializers, viewsets
from .models import item


class ItemSerializer(serializers.ModelSerializer):
   class Meta:
       model = item
       fields = ('id', 'itemName', 'name', 'team', 'status', 'register_date', 'rental_date', 'return_date')

class PDFSerializer(serializers.Serializer):
    html_content = serializers.CharField()

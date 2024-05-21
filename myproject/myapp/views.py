from datetime import date
from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import item
from .serializers import ItemSerializer
from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from xhtml2pdf import pisa
from rest_framework.pagination import PageNumberPagination
from io import BytesIO
from .serializers import PDFSerializer
# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

class ItemViewSet(viewsets.ModelViewSet):
    queryset = item.objects.all()
    serializer_class = ItemSerializer
    # pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #반환 업데이트
    @action(detail=True, methods=['PATCH'])
    def update_return_date(self, request, pk=None, *args, **kwargs):
        try:
            item_obj = item.objects.get(id=pk)  # ID가 pk인 정보를 DB에서 가져옴
        except item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        item_obj.status = '반환'
        item_obj.return_date = date.today()  # 반환일을 오늘 날짜로 업데이트
        item_obj.save()

        serializer = self.get_serializer(item_obj)
        response_data = serializer.data

        # 반환일 업데이트 후의 추가 로직을 manage.html에서 처리하도록 response_data에 추가 정보를 포함하여 반환
        response_data['dateType'] = 'return_date'

        return Response(response_data)

    #대여 업데이트
    @action(detail=True, methods=['PATCH'])
    def update_rental_date(self, request, pk=None, *args, **kwargs):
        try:
            item_obj = item.objects.get(id=pk)  # ID가 pk인 정보를 DB에서 가져옴
        except item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        item_obj.status = '대여'
        item_obj.return_date = date.today()  # 반환일을 오늘 날짜로 업데이트
        item_obj.save()

        serializer = self.get_serializer(item_obj)
        response_data = serializer.data

        # 반환일 업데이트 후의 추가 로직을 manage.html에서 처리하도록 response_data에 추가 정보를 포함하여 반환
        response_data['dateType'] = 'rental_date'

        return Response(response_data)

    #삭제
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


# 대여 통계
class RentalStatistics(APIView):
    def get(self, request):
        # 오늘 날짜 계산
        today = date.today()

        # 오늘 대여 건수 조회
        rental_today = item.objects.filter(rental_date=today).count()

        # 이번 주 대여 건수 조회
        rental_week = item.objects.filter(rental_date__week=today.isocalendar()[1]).count()

        statistics = {
            'rental_today': rental_today,
            'rental_week': rental_week,
        }

        return Response(statistics)

# 반환 통계
class ReturnStatistics(APIView):
    def get(self, request):
        # 오늘 날짜 계산
        today = date.today()

        # 오늘 반환 건수 조회
        return_today = item.objects.filter(return_date=today).count()

        # 이번 주 대여 건수 조회
        return_week = item.objects.filter(return_date__week=today.isocalendar()[1]).count()

        statistics = {
            'return_today': return_today,
            'return_week': return_week,
        }

        return Response(statistics)

class RegisterStatistics(APIView):
    def get(self, request):
        # 오늘 날짜 계산
        today = date.today()

        # 오늘 반환 건수 조회
        register_today = item.objects.filter(register_date=today).count() 

        # 이번 주 대여 건수 조회
        register_week = item.objects.filter(register_date__week=today.isocalendar()[1]).count() + 4

        statistics = {
            'register_today': register_today,
            'register_week': register_week,
        }

        return Response(statistics)

class PDFConversionView(APIView):
    def post(self, request):
        serializer = PDFSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        html_content = serializer.validated_data['html_content']
        pdf_file = self.convert_to_pdf(html_content)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
        response.write(pdf_file)
        return response

    def convert_to_pdf(self, html_content):
        result = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), result)
        if not pdf.err:
            return result.getvalue()
        else:
            raise Exception('PDF 변환에 실패했습니다.')



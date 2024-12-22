from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Bill
from ..serializers import BillSerializer

class BillDetail(APIView):
    @swagger_auto_schema(
        tags=['Bill'],
        responses={200: BillSerializer},
        operation_summary="Get Bill By ID",
        )
    def get(self, request, pk, format=None):
        try:
            bill = Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Bill'],
        request_body=BillSerializer,
        responses={200: BillSerializer},
        operation_summary="Update Bill",
        )
    def put(self, request, pk, format=None):
        try:
            bill = Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BillSerializer(bill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Bill'],
        request_body=BillSerializer,
        responses={200: BillSerializer},
        operation_summary="Partial Update Bill",
        )
    def patch(self, request, pk, format=None):
        try:
            bill = Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BillSerializer(bill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Bill'], 
        responses={204: 'No Content'},
        operation_summary="Delete Bill",
        )
    def delete(self, request, pk, format=None):
        try:
            bill = Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
        bill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BillCreate(APIView):
    @swagger_auto_schema(
        tags=['Bill'],
        request_body=BillSerializer,
        responses={201: BillSerializer, 400: "Invalid data"},
        operation_summary="Create Bill",
    )
    def post(self, request, format=None):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = BillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BillList(APIView):
    @swagger_auto_schema(
        tags=['Bill'], 
        responses={200: BillSerializer(many=True)},
        operation_summary="Get All Bills",
        )
    def get(self, request, format=None):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
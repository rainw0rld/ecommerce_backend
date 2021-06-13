from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, BrandSerializer, CategorySerializer
from .models import Product, Brand, Category
import random
import string


# Create your views here.

@api_view(['GET'])
def index(response):
    pass
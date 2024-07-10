from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, ProductLineSerializer
from .models import Category, Brand, Product

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all().isactive()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
        A simple Viewset for viewing all products
    """

    queryset = Product.objects.all().isactive()
    lookup_field = "slug"
    serializer_class = ProductSerializer

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(self.queryset.filter(slug=slug), many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    """
        Endpoint for getting the products by category
    """
    @action(methods=["get"], detail=False, url_path=r"category/(?P<category>\w+)/all")
    def list_product_by_category(self, request, category=None):
        serializer = ProductSerializer(self.queryset.filter(category__name__iexact=category), many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """.
    A simple Viewset for viewing all brands
    """

    queryset = Brand.objects.all().isactive()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
"""
Se podría optar por usar las clases CreateAPIView (para crear un Product) y 
ListAPIView (para listar los distintos Products) por separado de la siguiente forma:
    class ProductCreateAPIView(generics.CreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        def perform_create(self, serializer):
            content = serializer.validated_data.get('content') or "No description given"
            serializer.save(content=content)
            # También se puede optar por enviar una Signal.
    class ProductListAPIView(generics.ListAPIView):

        queryset = Product.objects.all()
        serializer_class = ProductSerializer
Pero usando ListCreateAPIView cumple el rol de ambas, 
para un mismo endpoint, un método GET devuelve la lista de Products y el metodo POST crea un Product.
"""
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or "No description given"
        serializer.save(content=content)
        # También se puede optar por enviar una Signal.

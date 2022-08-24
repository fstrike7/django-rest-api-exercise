from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # do something with the instance or just call perform_destroy from super()
        return super().perform_destroy(instance)

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.content = instance.content or "No description given"

"""
Se podría optar por usar las clases CreateAPIView (para crear un Product) y 
ListAPIView (para listar los distintos Products) por separado de la siguiente forma:
####
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
####
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

"""
Las clases de mixins permite combinar distintas consultas.
En sí las distintas subclases de generics (ListCreateAPIView, UpdateAPIView, etc) 
hacen uso de las subclases de mixins (CreateModelMixin, ListModelMixin, etc),
hacerlo de esta forma nos permite centralizar las consultas en una sola función y tener más control de que ocurre con cada una.
Ejemplo, para un mismo GET podemos determinar si se pide un elemento especifico dado su pk, o la lista de los elementos.
"""
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args,  **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args,  **kwargs):
        return self.create(request, *args,  **kwargs)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or "No description given"
        serializer.save(content=content)
        # También se puede optar por enviar una Signal.

"""
Este es un método alternativo, que con solo una función abarca todos los métodos, 
pero más confuso que el anterior. Usando clases derivadas de generics el código es más legible.
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == 'GET':
        if pk:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data.get('content') or "No description given"
            serializer.save(content=content)
            #instance = serializer.save() # Guarda la info en la DB y devuelve una instancia del objeto.
            return Response(serializer.data)
"""
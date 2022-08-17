import json
from django.forms.models import model_to_dict
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

"""
def api_home(request, *args, **kwargs):
    # request -> HttpRequest -> Django != requests
    params = request.GET # Url query params
    body = request.body # byte string of JSON data
    data = dict()
    try:
        data = json.loads(body)
    except:
        # Entra acá en el caso de que no se le pase ningún body
        pass
    data['params'] = dict(params)
    data['headers'] = request.headers # Previous versions used request.META
    data['content_type'] = request.content_type
    print(data)
    return JsonResponse({"message": f"Hi{' '+data['name'] if data.get('name') else ''}! This is Django API Response!"})
"""

"""
@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().order_by('?').first()
    data = {}
    if instance:
        # Serialization process:
            # model instance (model_data)
            # turn into a Python dict
            # return JSON to client

        ###
        #Tedious way:
        #data['id'] = model_data.id
        #data['title'] = model_data.title
        #data['content'] = model_data.content
        #data['price'] = model_data.price
        ###

        # Easy way :D
        #data = model_to_dict(model_data, fields=['id', 'title', 'content', 'price', 'sale_price'])
        # Using serializer
        data = ProductSerializer(instance).data
    return Response(data)
"""

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        #instance = serializer.save() # Guarda la info en la DB y devuelve una instancia del objeto.
        return Response(serializer.data)
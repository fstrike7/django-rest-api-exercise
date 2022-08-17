from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'discount' # Va a buscar el método get_discount de la clase ProductSerializer.
        ]

    def get_discount(self, obj):
        # Excepción donde el objeto no es una instancia del modelo. Útil cuando la información pasada como data no quiere ser guardada en la DB.
        if not isinstance(obj, Product):
            return None
        # Devuelve el método get_discount del obj pasado como argumento, en este caso, una instancia de Product.  
        return obj.get_discount()
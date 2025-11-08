from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Category, Warehouse, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    category_id = PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    warehouse_id = PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='warehouse', write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
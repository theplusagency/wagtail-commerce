from products.models import Product
import graphene
from graphene_django.types import DjangoObjectType


class ProductNode(DjangoObjectType):

    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        # interfaces = (Node, )
        # filter_fields = {
        #     'name': ['exact', 'icontains', 'istartswith'],
        #     'notes': ['exact', 'icontains'],
        #     'category': ['exact'],
        #     'category__name': ['exact'],
        # }


class Query(graphene.ObjectType):
    products = graphene.List(ProductNode)

    @graphene.resolve_only_args
    def resolve_products(self):
        return Product.objects.all()


schema = graphene.Schema(query=Query)

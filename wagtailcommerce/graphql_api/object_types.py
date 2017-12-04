import graphene


class CartLineNode(graphene.ObjectType):
    variant_id = graphene.Int()
    quantity = graphene.Int()

from django.contrib.contenttypes.models import ContentType

import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.carts.models import Cart, CartLine
from wagtailcommerce.graphql_api.object_types import WagtailImageType
from wagtailcommerce.products.object_types import ProductVariantType


class CartType(DjangoObjectType):

    class Meta:
        model = Cart


class CartLineType(DjangoObjectType):
    main_image = graphene.Field(WagtailImageType)
    variant = graphene.Field(ProductVariantType)

    def resolve_main_image(self, info, **kwargs):
        """
        Filter image sets and obtain cart line's variant's related image set.

        Returns the first image of the set.
        """
        filtering_fields = self.variant.product.specific.image_set_filtering_fields

        image_sets = self.variant.product.image_sets.all()

        for field in filtering_fields:
            # Filter image sets by generic foreign key, value comes from field on variant
            filtering_object = getattr(self.variant.specific, field)
            image_sets = image_sets.filter(
                content_type=ContentType.objects.get_for_model(filtering_object),
                object_id=filtering_object.pk
            )

        return image_sets[0].images.first().image

    class Meta:
        model = CartLine

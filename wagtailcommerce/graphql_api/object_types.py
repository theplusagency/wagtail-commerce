import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.utils.images import get_image_model
from wagtailcommerce.products.models import Image, ImageSet

from wagtail.images.models import Rendition


WagtailImage = get_image_model(require_ready=False)


class RenditionType(DjangoObjectType):
    class Meta:
        model = Rendition


class WagtailImageType(DjangoObjectType):
    renditions = graphene.List(RenditionType)

    def resolve_renditions(self, info, **kwargs):
        # @TODO: get only necessary renditions
        return self.renditions.all()

    class Meta:
        model = WagtailImage
        exclude_fields = ('tags', )

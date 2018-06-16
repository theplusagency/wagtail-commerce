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
    renditions = graphene.List(RenditionType, filter_specs=graphene.Argument(graphene.List(graphene.String)))

    def resolve_renditions(self, info, filter_specs=[]):
        params = {}

        if filter_specs:
            params['filter_spec__in'] = filter_specs

        rend = self.renditions.filter(**params)
        print(rend)
        return rend

    class Meta:
        model = WagtailImage
        exclude_fields = ('tags', )


class ImageType(DjangoObjectType):
    image = graphene.Field(WagtailImageType)

    def resolve_image(self, info):
        return self.image

    class Meta:
        model = Image


class ImageSetType(DjangoObjectType):
    images = graphene.List(ImageType)

    def resolve_images(self, info):
        return self.images.all().order_by()

    class Meta:
        model = ImageSet

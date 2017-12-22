from wagtailcommerce.stores.utils import get_store


def store(request):
    return {
        'store': request.store
    }

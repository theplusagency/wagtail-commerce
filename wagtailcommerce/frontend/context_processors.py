from wagtailcommerce.stores.utils import get_store


def store(request):
    return {
        'store': request.store,
        'store_currency': request.store.currency if request.store else ''
    }

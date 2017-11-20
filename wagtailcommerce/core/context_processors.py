from wagtailcommerce.carts.utils import get_cart_from_request


def wagtailcommerce_props(request):
    return {
        'props': {
            'cart': get_cart_from_request(request)
        }
    }

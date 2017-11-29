from wagtailcommerce.carts.utils import get_cart_from_request


def wagtailcommerce_props(request):
    return {
        'props': {
            'cart': {
                'lines': [
                    {
                        'pk': 1,
                        'variant_id': '31313',
                        'name': 'Peak Riser High',
                        'image': '/media/images/E44323AWHITE_2.max-165x165.png',
                        'price': 223,
                        'quantity': 2,
                    },
                    {
                        'pk': 2,
                        'variant_id': '31313',
                        'name': 'Peak Riser High',
                        'image': '/media/images/E44323AWHITE_2.max-165x165.png',
                        'price': 223,
                        'quantity': 2,
                    },
                ],
            }
        }
    }

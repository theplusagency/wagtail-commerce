from oca_shipping.models import OCAShippingMethod


def get_shipping_cost(cart, address=None):
    shipping_method = OCAShippingMethod.objects.get()

    return shipping_method.calculate_cost(cart, address)

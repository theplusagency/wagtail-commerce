from .models import Cart

COOKIE_NAME = 'cart'


def get_anonymous_cart_from_token(store, token):
    """
    Return an open anonymous cart for a given token
    """
    return Cart.objects.open().from_store(store).for_token(token=token).first()


def get_user_cart(store, user):
    """
    Fetch an open cart for user
    """
    return Cart.objects.open().from_store(store).for_user(user).first()


def get_cart_from_request(request):
    """
    Retrieve cart from DB or create a new one
    """
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        user = request.user
    else:
        token = request.get_signed_cookie(COOKIE_NAME, default=None)
        cart = get_anonymous_cart_from_token(request.store, token)
        user = None

    if cart is not None:
        return cart

    return Cart(user=user)

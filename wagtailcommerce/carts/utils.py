from datetime import timedelta

from wagtailcommerce.carts.exceptions import CartException

SESSION_KEY_NAME = 'cart_token'


def set_cart_cookie(cart, request):
    """
    Save a cart token in the session
    """
    # FIXME: check why session is not used in Saleor
    request.session[SESSION_KEY_NAME] = '{}'.format(cart.token)


def get_anonymous_cart_from_token(store, token):
    """
    Return an open anonymous cart for a given token
    """
    from wagtailcommerce.carts.models import Cart

    return Cart.objects.open().from_store(store).for_token(token=token).first()


def get_user_cart(store, user):
    """
    Fetch an open cart for user
    """
    from wagtailcommerce.carts.models import Cart

    return Cart.objects.open().from_store(store).for_user(user).first()


def get_cart_from_request(request):
    """
    Retrieve cart from DB or create a new one
    """
    from wagtailcommerce.carts.models import Cart

    if request.user.is_authenticated:
        cart = get_user_cart(request.store, request.user)
        user = request.user
    else:
        token = request.session.get(SESSION_KEY_NAME, None)
        cart = get_anonymous_cart_from_token(request.store, token)
        user = None

    if cart is not None:
        return cart

    return Cart(user=user, store=request.store)


def add_to_cart(request, variant):
    """
    Add one unit of variant to the request's cart
    """
    from wagtailcommerce.carts.models import CartLine

    cart = get_cart_from_request(request)

    if not getattr(cart, 'pk', None):
        cart.save()

    try:
        cart_line = cart.lines.get(variant=variant)
        cart_line.quantity = cart_line.quantity + 1
        cart_line.save()
    except CartLine.DoesNotExist:
        cart_line = CartLine.objects.create(cart=cart, variant=variant, quantity=1)

    if not request.user.is_authenticated:
        set_cart_cookie(cart, request)

    return cart_line


def modify_cart_line(request, variant, quantity):
    """
    Find a cart line matching the variant and modify its quantity
    """
    from wagtailcommerce.carts.models import CartLine

    cart = get_cart_from_request(request)

    if not getattr(cart, 'pk', None) or quantity < 0:
        # Generic error to be displayed on UI
        # Should't happen on any normal scenario
        raise CartException()

    try:
        cart_line = cart.lines.get(variant=variant)

        if quantity == 0:
            cart_line.delete()
            return None

        cart_line.quantity = quantity
        cart_line.save()
        return cart_line
    except CartLine.DoesNotExist:
        raise CartException()

COOKIE_NAME = 'cart'


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
        token = request.get_signed_cookie(COOKIE_NAME, default=None)
        cart = get_anonymous_cart_from_token(request.store, token)
        print(cart.pk)
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
        cart = cart.save()

    try:
        cart_line = cart.lines.get(variant=variant)
        cart_line.quantity = cart_line.quantity + 1
        cart_line.save()
    except CartLine.DoesNotExist:
        cart_line = CartLine.objects.create(cart=cart, variant=variant, quantity=1)

    return cart_line

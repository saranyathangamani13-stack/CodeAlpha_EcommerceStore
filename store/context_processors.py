def cart_count(request):
    cart = request.session.get('cart', {})
    total = 0

    if isinstance(cart, dict):
        for quantity in cart.values():
            try:
                total += int(quantity)
            except (TypeError, ValueError):
                continue

    return {'cart_count': total}
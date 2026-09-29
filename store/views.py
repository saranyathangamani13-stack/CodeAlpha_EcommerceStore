from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Order, OrderItem, Product


def _safe_int(value, default=0):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed


def _cart_products(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    valid_ids = [str(product_id) for product_id in cart.keys() if str(product_id).isdigit()]
    products = Product.objects.filter(id__in=valid_ids, is_active=True)

    lines = []
    total = Decimal('0.00')

    for product in products:
        quantity = _safe_int(cart.get(str(product.id), cart.get(product.id)), 0)
        if quantity <= 0:
            continue
        if product.stock <= 0:
            continue

        quantity = min(quantity, product.stock)
        line_total = product.price * quantity
        lines.append({'product': product, 'quantity': quantity, 'line_total': line_total})
        total += line_total

    return lines, total


def home(request):
    products = Product.objects.filter(is_active=True, stock__gt=0)
    category = request.GET.get('category', '')
    search = request.GET.get('q', '').strip()
    if category in dict(Product.CATEGORIES):
        products = products.filter(category=category)
    if search:
        products = products.filter(name__icontains=search)
    return render(request, 'store/home.html', {
        'products': products,
        'categories': Product.CATEGORIES,
        'selected_category': category,
        'search': search,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if request.method == 'POST':
        if product.stock < 1:
            messages.error(request, 'This piece is currently out of stock.')
        else:
            requested_quantity = _safe_int(request.POST.get('quantity', 1), 1)
            if requested_quantity <= 0:
                messages.error(request, 'Please choose a valid quantity.')
            else:
                cart = request.session.get('cart', {})
                if not isinstance(cart, dict):
                    cart = {}
                product_id = str(product.id)
                quantity = _safe_int(cart.get(product_id, 0), 0) + requested_quantity
                cart[product_id] = min(quantity, product.stock)
                request.session['cart'] = cart
                messages.success(request, f'{product.name} added to your bag.')
                return redirect('cart')
    return render(request, 'store/product_detail.html', {'product': product})


@require_POST
def cart(request):
    cart_data = request.session.get('cart', {})
    if not isinstance(cart_data, dict):
        cart_data = {}

    product_id = request.POST.get('product_id')
    action = request.POST.get('action')

    if not product_id:
        request.session['cart'] = cart_data
        if request.headers.get('Referer'):
            return redirect(request.headers['Referer'])
        return redirect('cart')

    if action == 'remove':
        cart_data.pop(product_id, None)
        messages.info(request, 'Item removed from your bag.')
    elif action == 'update':
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        quantity = _safe_int(request.POST.get('quantity', 1), 1)
        if quantity <= 0:
            cart_data.pop(product_id, None)
        else:
            cart_data[product_id] = min(quantity, product.stock)
    elif action == 'add':
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        current_quantity = _safe_int(cart_data.get(product_id, 0), 0)
        cart_data[product_id] = min(current_quantity + 1, product.stock)

    request.session['cart'] = cart_data
    if request.headers.get('Referer'):
        return redirect(request.headers['Referer'])
    return redirect('cart')


def cart_page(request):
    lines, total = _cart_products(request)
    return render(request, 'store/cart.html', {'lines': lines, 'total': total})


@login_required
def checkout(request):
    lines, total = _cart_products(request)
    if not lines:
        messages.info(request, 'Your bag is ready for something good.')
        return redirect('home')
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        if not all((full_name, email, address, city, postal_code)):
            messages.error(request, 'Please complete every delivery detail.')
        else:
            with transaction.atomic():
                locked_products = {
                    product.id: product
                    for product in Product.objects.select_for_update().filter(
                        id__in=[line['product'].id for line in lines], is_active=True
                    )
                }
                if any(
                    locked_products.get(line['product'].id) is None
                    or locked_products[line['product'].id].stock < line['quantity']
                    for line in lines
                ):
                    messages.error(request, 'A bag item has changed availability. Please review your bag.')
                    return redirect('cart')
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    email=email,
                    shipping_address=address,
                    city=city,
                    postal_code=postal_code,
                )
                for line in lines:
                    product = locked_products[line['product'].id]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        quantity=line['quantity'],
                        unit_price=product.price,
                    )
                    product.stock -= line['quantity']
                    product.save(update_fields=['stock'])
            request.session['cart'] = {}
            messages.success(request, 'Order placed. No payment was collected in this demo.')
            return redirect('order_detail', reference=order.reference)
    return render(request, 'store/checkout.html', {
        'lines': lines,
        'total': total,
        'initial_name': request.user.get_full_name() or request.user.username,
        'initial_email': request.user.email,
    })


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next') or 'home')
    return render(request, 'store/login.html', {'form': form})


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'store/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def orders(request):
    order_list = Order.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': order_list})


@login_required
def order_detail(request, reference):
    order = get_object_or_404(Order, reference=reference, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
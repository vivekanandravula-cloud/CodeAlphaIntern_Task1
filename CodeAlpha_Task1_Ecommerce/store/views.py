from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product

def _cart_data(request):
    cart = request.session.get("cart", {})
    items, total, count = [], Decimal("0.00"), 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = max(1, int(quantity))
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
        line_total = product.price * quantity
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
        count += quantity
    return items, total, count

def home(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query) | products.filter(category__icontains=query)
    _, _, cart_count = _cart_data(request)
    return render(request, "store/home.html", {"products": products, "query": query, "cart_count": cart_count})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    _, _, cart_count = _cart_data(request)
    return render(request, "store/product_detail.html", {"product": product, "cart_count": cart_count})

def cart(request):
    items, total, cart_count = _cart_data(request)
    return render(request, "store/cart.html", {"items": items, "total": total, "cart_count": cart_count})

def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, pk=product_id)
    cart_items = request.session.get("cart", {})
    current = int(cart_items.get(str(product_id), 0))
    if current >= product.stock:
        messages.warning(request, "You have reached the available stock for this product.")
    else:
        cart_items[str(product_id)] = current + 1
        request.session["cart"] = cart_items
        request.session.modified = True
        messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")

def update_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        try:
            quantity = int(request.POST.get("quantity", "1"))
        except ValueError:
            quantity = 1
        cart_items = request.session.get("cart", {})
        if quantity <= 0:
            cart_items.pop(str(product_id), None)
        elif quantity <= product.stock:
            cart_items[str(product_id)] = quantity
        else:
            messages.warning(request, f"Only {product.stock} units of {product.name} are available.")
        request.session["cart"] = cart_items
        request.session.modified = True
    return redirect("cart")

def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart_items = request.session.get("cart", {})
        cart_items.pop(str(product_id), None)
        request.session["cart"] = cart_items
        request.session.modified = True
        messages.info(request, "Item removed from your cart.")
    return redirect("cart")

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("home")
    _, _, cart_count = _cart_data(request)
    return render(request, "store/register.html", {"form": form, "cart_count": cart_count})

@login_required
def checkout(request):
    items, total, cart_count = _cart_data(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            # Recheck inventory before committing the order.
            for item in items:
                product = Product.objects.select_for_update().get(pk=item["product"].pk)
                if item["quantity"] > product.stock:
                    messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                    return redirect("cart")
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                total=total,
            )
            for item in items:
                product = Product.objects.select_for_update().get(pk=item["product"].pk)
                OrderItem.objects.create(
                    order=order, product=product, product_name=product.name,
                    unit_price=product.price, quantity=item["quantity"]
                )
                product.stock -= item["quantity"]
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} placed successfully.")
        return redirect("orders")
    return render(request, "store/checkout.html", {"form": form, "items": items, "total": total, "cart_count": cart_count})

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items")
    _, _, cart_count = _cart_data(request)
    return render(request, "store/orders.html", {"orders": user_orders, "cart_count": cart_count})

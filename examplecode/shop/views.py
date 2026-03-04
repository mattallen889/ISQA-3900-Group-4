from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart = Cart(request)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart': cart})

def product_detail(request, id):
    product = get_object_or_404(Product,
                                id=id,
                                available=True)
    #set choices for quantity available based on inventory and items in this session's cart
    cart = Cart(request)
    cartquantity = 0
    #if item in cart, subtract the items in the cart from the quantity available
    for item in cart:
        cartproduct = get_object_or_404(Product, id=item['product'].id)
        if product == cartproduct:
            cartquantity=item['quantity']
            break
    if product.quantity - cartquantity > 0:
        choices = [(i, str(i)) for i in range(1, product.quantity - cartquantity + 1)]
    else: #no items left in inventory for this session
        choices = [(1, 0)]

    cart_product_form = CartAddProductForm(my_choices=choices)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'cart': cart})


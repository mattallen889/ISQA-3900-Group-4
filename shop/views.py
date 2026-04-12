from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
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

def manage_customer_orders(request):
    if request.user.is_authenticated and request.user.is_staff:
        





        return redirect('/')
    else:
        return redirect('/')

#added code for base.html connection by Nate

def loginView(request):
    return render(request, 'registration/login.html', {'errorPresent': False})

def loginHandler(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return redirect('/registration/loginError/')
        else:
            login(request, user)
            return redirect('/catalog/profile/')
    else:
        return redirect('/registration/login/')

def loginErrorHandler(request):
    return render(request, 'registration/login.html', {'errorPresent': True, 'errorMsg': 'Username or password is not valid.'})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('shop:product_list')

def logged_out(request):
    return render(request, 'registration/logged_out.html')

def profile(request):
    return render(request, 'catalog/profile.html')
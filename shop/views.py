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

def edit_menu_items(request):
    if request.user.is_authenticated and request.user.is_staff:
        categories = Category.objects.all()
        products = Product.objects.all()
        return render(request, 'catalog/editMenuItems.html', {'categories': categories, 'products': products})
    else:
        return redirect('/')

def create_or_alter_menu_form(request, args):
    if request.user.is_authenticated and request.user.is_staff:
        categories = Category.objects.all()
        try:
            modeArgs = None
            if args == 'create':
                mode = args
            else:
                mode = args.split('-')[0]
                modeArgs = Product.objects.get(id=int(args.split('-')[1]))
            return render(request, 'catalog/createAlterMenuItemForm.html', {'unalteredArgs': args, 'mode': mode, 'args': modeArgs, 'categories': categories})
        except:
            return redirect('/')
    else:
        return redirect('/')

def execute_menu_alteration(request, args):
    if request.user.is_authenticated and request.user.is_staff:
        if (args == 'create'):
            mode = args

            # Default values
            price = 0.00
            quantity = 0
            description = ''


            name = request.POST['name']
            category = Category.objects.get(slug=request.POST['category'])
            image = request.POST['image']
            description = request.POST['description']
            price = float(request.POST['price']) if request.POST['price'] != '' else price
            quantity = int(request.POST['quantity']) if request.POST['quantity'] != '' else quantity

            product = Product(name=name, category=category, image=image, description=description, price=price, quantity=quantity)
            product.save()

        elif (args.startswith('delete')):
            modeArgs = args.split('-')[1]
            product = Product.objects.get(id=modeArgs)
            product.delete()

        elif (args.startswith('edit')):
            mode = args.split('-')[0]
            modeArgs = args.split('-')[1]

            name = request.POST['name']
            category = Category.objects.get(slug=request.POST['category'])
            image = request.POST['image']
            description = request.POST['description']
            price = request.POST['price']
            quantity = request.POST['quantity']

            print(f'{True if name == '' else False}\n{category}\n{image}\n{description}\n{price}\n{quantity}')

            product = Product.objects.get(id=int(modeArgs))
            product.name = name if request.POST['name'] != '' else product.name
            product.category = category
            product.image = image if request.POST['image'] != '' else product.image
            product.description = description if request.POST['description'] != '' else product.description
            product.price = float(price) if request.POST['price'] != '' else product.price
            product.quantity = int(quantity) if request.POST['quantity'] != '' else product.quantity

            product.save()

        return redirect('shop:edit_menu_items')
    else:
        return redirect('/')

def create_menu_category_form(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'catalog/createMenuCategoryForm.html')
    else:
        return redirect('/')

def execute_menu_category_alteration(request, args):
    if request.user.is_authenticated and request.user.is_staff:
        if (args.startswith('create')):
            mode = args
            name = request.POST['name']
            category = Category(name=name, slug=name)
            category.save()
        elif (args.startswith('delete')):
            modeArgs = args.split('-')[1]
            category = Category.objects.get(id=modeArgs)
            category.delete()
        else:
            pass
        return redirect('shop:edit_menu_items')
    else:
        return redirect('/')
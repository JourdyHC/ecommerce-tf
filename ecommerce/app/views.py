from decimal import Decimal
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Customer, OrderPlaced, Product
from .forms import CustomerProfileForm, CustomerRegitrationForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html", locals())

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category__slug = val)
        title = Product.objects.filter(category__slug=val).values('title')
        return render(request, "app/category.html", locals())
    
def login_success(request):
    user = request.user
    if(Customer.objects.filter(user=user).exists()):
        return redirect('home')
    else:
        return redirect('profile')

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())
    
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegitrationForm()
        return render(request, 'app/customerregistration.html',locals())
    
    def post(self, request):
        form = CustomerRegitrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Error! invalid imput data")
        return redirect("login")

class ProfileView(View):
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            # Si existe el perfil, llena el formulario con los datos del perfil
            form = CustomerProfileForm(instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm()
        return render( request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            print(user)
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            Customer.objects.update_or_create(
                user=user,
                defaults={
                    'name':name, 
                    'locality':locality, 
                    'mobile':mobile, 
                    'city':city, 
                    'state':state, 
                    'zipcode':zipcode
                }
            )

            # reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            # reg.save()

            messages.success(request, "Congratultions! profile Save Successfully")
            return redirect('home')
        else:
            messages.warning(request, "Invalid data input")
            return render(request, 'app/profile.html',locals())
    
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        add= Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profie Update Successcfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/updateAddress.html', locals())

def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product = product).save()
        return redirect("/cart")
    else:
        return redirect("login")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = getAmount(user)
        totalamount = (amount + 40)
        return render(request, 'app/checkout.html',locals())
    
    def post(self, request):
        user = request.user
        customer = Customer.objects.get(user=user)
        add = Customer.objects.filter(user=user)
        amount = getAmount(user)
        cart_items = Cart.objects.filter(user=user)
        totalamount = amount + 40
        if (customer.credits > totalamount):
            ##Crear orden
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=user, 
                    customer=Customer.objects.get(user=user), 
                    product=item.product,
                    quantity=item.quantity,
                    )
            #Eliminar objetos del carrito de compras
            cart_items.delete()
            customer.credits -= Decimal(totalamount)
            customer.save()
            return redirect('orders')
        else:
            messages.warning(request,"Créditos insuficientes")
            return render(request, 'app/checkout.html',locals())
    
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())

def plus_cart(request):
    if (request.method == 'GET'):
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        amount = getAmount(user)
        data = {
            'quantity': c.quantity,
            'amount': "S/. %.2f" % amount,
            'totalamount': "S/. %.2f" % (amount+40),
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if (request.method == 'GET'):
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity-=1
            c.save()
        user = request.user
        amount = getAmount(user)
        data = {
            'quantity': c.quantity,
            'amount': "S/. %.2f" % amount,
            'totalamount': "S/. %.2f" % (amount+40),
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        amount = getAmount(user)
        data = {
            'quantity': c.quantity,
            'totalamount': "S/. %.2f" % (amount+40),
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET['search']
    products = Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html',locals())

##Utils    
def getAmount(user):
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount + value
    return amount

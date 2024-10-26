from .models import Cart, Category, Customer


def navBarData(request):
    #categoris = 
    totalitem=0
    credits=0
    categories = Category.objects.all()
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        credits = Customer.objects.get(user=request.user).credits
    return {
        'totalitem':totalitem,
        'categories':categories,
        'credits':credits
        }
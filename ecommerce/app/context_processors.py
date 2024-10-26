from .models import Cart, Category


def navBarData(request):
    #categoris = 
    totalitem=0
    categories = Category.objects.all()
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return {
        'totalitem':totalitem,
        'categories':categories
        }
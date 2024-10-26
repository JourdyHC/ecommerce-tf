from .models import Cart


def navBarData(request):
    #categoris = 
    totalitem=0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return {'totalitem':totalitem}
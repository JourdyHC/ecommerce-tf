"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm

urlpatterns = [
    
    path("", views.home),
    path("about", views.about, name="about"),
    path("contact", views.contact, name='contact'),
    path("category/<slug:val>",views.CategoryView.as_view(), name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(), name="product-detail"),
    path("profile/",views.ProfileView.as_view(), name='profile'),
    path("address/",views.address, name='address'),
    path("updateAddress/<int:pk>",views.UpdateAddress.as_view(), name='updateAddress'),

    #Carrito
    path("add-to-cart/",views.add_to_cart, name='add-to-cart'),
    path("cart/",views.show_cart, name='showcart'),
    path("checkout/",views.show_cart, name='checkout'),

    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('passwword-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    ##Contadores de cantidad
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
         
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
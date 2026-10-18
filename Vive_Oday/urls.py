"""
URL configuration for Vive_Oday project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from Oday import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index),
    path("superuser/admincontrol/", views.Admin, name="admincontrol"),
    path("category/create/", views.CategoryCreate, name="CategoryCreate"),
    path("category/update/<int:catpk>/", views.CategoryUpdate, name="CategoryUpdate"),
    path("category/delete/<int:catpk>/", views.CategoryDelete, name="CategoryDelete"),
    path("Feature/create/", views.FeatureCreate, name="FeatureCreate"),
    path("Feature/update/<int:feapk>/", views.FeatureUpdate, name="FeatureUpdate"),
    path("Feature/delete/<int:feapk>/", views.FeatureDelete, name="FeatureDelete"),
    path("mainhero/create/", views.MainheroCreate, name="MainheroCreate"),
    path("mainhero/update/<int:mainpk>/", views.MainheroUpdate, name="MainheroUpdate"),
    path("mainhero/delete/<int:mainpk>/", views.MainheroDalete, name="MainheroDelete"),
    path("mainhero/activate/<int:mainactpk>/", views.MainheroActive),
    path("mainhero/deactivate/<int:maindepk>/", views.MainheroDeactive),
    path("about/", views.About),
    path("about/create/", views.AboutCreate, name="AboutCreate"),
    path("about/update/<int:aboutpk>/", views.AboutUpdate, name="AboutUpdate"),
    path("about/delete/<int:aboutpk>/", views.AboutDelete, name="AboutDelete"),
    path("brand/create/", views.BrandCreate, name="BrandCreate"),
    path("brand/update/<int:brandpk>/", views.BrandUpdate, name="BrandUpdate"),
    path("brand/delete/<int:Brandpk>/", views.BrandDelete, name="BrandDelete"),
    path("shop/", views.Shop, name="shop"),
    path("contact/", views.Contact),
    path("card/list/<int:cardpk>/", views.CardList, name="CardList"),
    path("Card/create/", views.CardCreate, name="CardCreate"),
    path("Card/update/<int:cardpk>/", views.CardUpdate, name="CardUpdate"),
    path("Card/delete/<int:cardpk>/", views.CardDelete, name="CardDelete"),
    path("login/", views.Login, name="login"),
    path("register/", views.Register),
    path("logout/", views.Logout, name="logout"),
    path("add-to-cart/<int:cardpk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_list, name="cart_list"),
    path("cart/delete/<int:item_id>/", views.remove_from_cart, name="cart_delete"),
    path("adminContact/view/", views.AdminContactView),
    path("adminContact/view/delete/<int:contactpk>/", views.AdminContactDelete),
    path("admincontrol/login/view/", views.AdminLoginHistory, name="login_history"),
    path(
        "admincontrol/login/view/delete/<int:logindetpk>/",
        views.AdminLoginHistoryDeltete,
        name="login_history",
    ),
    # USER
    path("cart/", views.cart_list, name="cart_list"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-single/<int:item_id>/", views.order_single, name="order_single"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("buy-now/<int:cardpk>/", views.buy_now, name="buy_now"),
    path("order/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    # ADMIN
    path("superuser/orders/", views.admin_orders, name="admin_orders"),
    path(
        "superuser/orders/approve/<int:order_id>/",
        views.approve_order,
        name="approve_order",
    ),
    path(
        "superuser/orders/reject/<int:order_id>/",
        views.reject_order,
        name="reject_order",
    ),
    # forgotten password
    # LOGIN / FORGOT PASSWORD FLOW
    path("login/", views.Login, name="login"),
    path("forgot-password/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

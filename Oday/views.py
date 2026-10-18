from django.shortcuts import render, redirect, get_object_or_404
from Oday.models import (
    CategoryModel,
    FeatureModel,
    MainheroModel,
    AboutModel,
    BrandModel,
    CardModel,
    AddToCardModel,
    Order,
    OrderItem,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from .models import ContactModel
from .models import PasswordResetOTP
from django.utils import timezone
from datetime import timedelta
from .models import LoginHistory
from django.contrib.admin.views.decorators import staff_member_required


# ================================================ for index page ======================================
def Index(request):
    categories = CategoryModel.objects.all()
    features = FeatureModel.objects.all()
    mainhero = MainheroModel.objects.filter(is_active=True)

    return render(
        request,
        "index.html",
        {
            "categories": categories,
            "features": features,
            "mainhero": mainhero,
        },
    )


def admin_only(user):
    return user.is_authenticated and user.is_staff


@staff_member_required
def Admin(request):
    categories = CategoryModel.objects.all()
    features = FeatureModel.objects.all()
    main_text = MainheroModel.objects.all()
    mainhero = MainheroModel.objects.all()
    about = AboutModel.objects.all()
    brand_image = BrandModel.objects.all()
    Card = CardModel.objects.all()

    return render(
        request,
        "superuser/admin.html",
        {
            "categories": categories,
            "features": features,
            "main_hero": main_text,
            "main": mainhero,
            "about": about,
            "brands": brand_image,
            "Cards": Card,
        },
    )


# ============== CATEGORY =====================


@user_passes_test(admin_only)
def CategoryCreate(request):
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get("image")

        if not name:
            return redirect("/superuser/admincontrol/")

        CategoryModel.objects.create(name=name, image=image)
        return redirect("/superuser/admincontrol/")

    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def CategoryUpdate(request, catpk):
    if request.method == "POST":
        category = get_object_or_404(CategoryModel, id=catpk)
        category.name = request.POST.get("name")

        image = request.FILES.get("image")
        if image:
            category.image.delete(save=False)
            category.image = image

        category.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def CategoryDelete(request, catpk):
    category = get_object_or_404(CategoryModel, id=catpk)
    category.delete()
    return redirect("/superuser/admincontrol/")


# ===================== FEATURE =====================


@user_passes_test(admin_only)
def FeatureCreate(request):
    if request.method == "POST":
        name = request.POST.get("feature_name")
        price = request.POST.get("feature_price")
        rating = int(request.POST.get("feature_rating", 0))  # default 0
        description = request.POST.get("feature_description")
        image = request.FILES.get("feature_image")
        category_id = request.POST.get("category_id")

        category = CategoryModel.objects.get(id=category_id)

        FeatureModel.objects.create(
            name=name,
            price=price,
            description=description,
            image=image,
            rating=rating,
            category=category,
        )
    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def FeatureUpdate(request, feapk):
    if request.method == "POST":
        feature = get_object_or_404(FeatureModel, id=feapk)
        feature.name = request.POST.get("feature_name")
        feature.price = request.POST.get("feature_price")
        feature.rating = int(request.POST.get("feature_rating", 0))
        feature.description = request.POST.get("feature_description")
        feature.category_id = request.POST.get("category_id")
        image = request.FILES.get("feature_image")
        if image:
            feature.image.delete(save=False)
            feature.image = image

        feature.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def FeatureDelete(request, feapk):
    feature = get_object_or_404(FeatureModel, id=feapk)
    feature.delete()
    return redirect("/superuser/admincontrol/")


# ================================================ For about page ===============================================


def About(request):
    about = AboutModel.objects.all()
    brand_image = BrandModel.objects.all()
    return render(
        request,
        "about.html",
        {
            "abouts": about,
            "brands": brand_image,
        },
    )


def Shop(request):
    search = request.GET.get("search", "").strip()
    selected_category = request.GET.get("category", "")
    sort = request.GET.get("sort", "featured")
    page_number = request.GET.get("page", 1)

    categories = CategoryModel.objects.filter(is_active=True)
    cards = CardModel.objects.all()
    brand_image = BrandModel.objects.all()

    # SEARCH
    if search:
        cards = cards.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )

    # CATEGORY FILTER
    if selected_category:
        cards = cards.filter(
            category__name=selected_category
        )

    # SORT
    if sort == "az":
        cards = cards.order_by("name", "id")
    elif sort == "item":
        cards = cards.order_by("id")
    else:
        sort = "featured"
        cards = cards.order_by("-created_at", "-id")

    # PAGINATION
    paginator = Paginator(cards, 9)
    Cards = paginator.get_page(page_number)

    # Keep search, category and sort in pagination links
    params = request.GET.copy()
    params.pop("page", None)
    query_params = params.urlencode()

    return render(
        request,
        "shop.html",
        {
            "Cards": Cards,
            "categories": categories,
            "selected_category": selected_category,
            "search": search,
            "sort": sort,
            "brands": brand_image,
            "query_params": query_params,
        },
    )

# ============================================== For main hero edit ========================================
@user_passes_test(admin_only)
def MainheroCreate(request):
    if request.method == "POST":
        maintitle = request.POST.get("mainhero_title")
        des_title = request.POST.get("mainhero_des_name")
        main_description = request.POST.get("mainhero_description")
        main_image = request.FILES.get("main_image")

        MainheroModel.objects.create(
            maintitle=maintitle,
            descriptionTitle=des_title,
            maindescription=main_description,
            mainimage=main_image,
        )

    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def MainheroUpdate(request, mainpk):
    if request.method == "POST":
        mainhero = MainheroModel.objects.get(id=mainpk)
        mainhero.maintitle = request.POST.get("mainhero_title")
        mainhero.descriptionTitle = request.POST.get("mainhero_des_name")
        mainhero.maindescription = request.POST.get("mainhero_description")

        new_image = request.FILES.get("main_image")
        if new_image:
            mainhero.mainimage.delete(save=False)
            mainhero.mainimage = new_image

        mainhero.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def MainheroDalete(request, mainpk):
    mainhero = MainheroModel.objects.get(id=mainpk)
    mainhero.delete()
    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def MainheroActive(request, mainactpk):
    mainhero = MainheroModel.objects.get(id=mainactpk)
    if request.method == "POST":
        mainhero.is_active = True
        mainhero.save()
        messages.success(request, "Main hero is activate successfully")
        return redirect("/superuser/admincontrol")


@user_passes_test(admin_only)
def MainheroDeactive(request, maindepk):
    mainhero = MainheroModel.objects.get(id=maindepk)
    if request.method == "POST":
        mainhero.is_active = False
        mainhero.save()
        messages.success(request, "Main hero is deactivate successfully")
        return redirect("/superuser/admincontrol/")

    # =================================================================


@user_passes_test(admin_only)
def AboutCreate(request):
    if request.method == "POST":
        title = request.POST.get("about_title")
        image = request.FILES.get("image")
        description = request.POST.get("about_description")

        AboutModel.objects.create(title=title, description=description, image=image)

    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def AboutUpdate(request, aboutpk):
    if request.method == "POST":
        about = AboutModel.objects.get(id=aboutpk)

        about.title = request.POST.get("about_input_title")
        about.description = request.POST.get("about_input_description")

        about_image = request.FILES.get("about_input_image")
        if about_image:
            about.image.delete(save=False)
            about.image = about_image

        about.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def AboutDelete(request, aboutpk):
    about = AboutModel.objects.get(id=aboutpk)
    about.delete()
    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def BrandCreate(request):
    if request.method == "POST":
        brand_image = request.FILES.get("brand_image")

        BrandModel.objects.create(image=brand_image)

    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def BrandUpdate(request, brandpk):
    if request.method == "POST":
        brand = BrandModel.objects.get(id=brandpk)
        brand_image = request.FILES.get("brand_image")
        if brand_image:
            brand.image.delete(save=False)
            brand.image = brand_image

        brand.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def BrandDelete(request, Brandpk):
    if request.method == "POST":
        brand = BrandModel.objects.get(id=Brandpk)
        brand.delete()
    return redirect("/superuser/admincontrol/")


@login_required(login_url="/login/")
def CardList(request, cardpk):
    card = CardModel.objects.get(id=cardpk)
    related_products = CardModel.objects.exclude(id=card.id).order_by("-created_at")[
        :10
    ]

    if request.method == "POST":
        size = request.POST.get("product_size")

        CardModel.objects.create(product=card, size=size, quantity=1)

    return render(
        request,
        "shop-single.html",
        {
            "Card": card,
            "related_products": related_products,
        },
    )


@user_passes_test(admin_only)
def CardCreate(request):
    if request.method == "POST":
        name = request.POST.get("Card_name")
        size = request.POST.get("Card_size")
        price = request.POST.get("Card_price")
        starrating = int(request.POST.get("Card_rating", 0))
        description = request.POST.get("Card_description")
        image = request.FILES.get("Card_image")
        category_id = request.POST.get("category_id")

        category = CategoryModel.objects.get(id=category_id)

        CardModel.objects.create(
            name=name,
            size=size,
            price=price,
            description=description,
            image=image,
            starrating=starrating,
            category=category,
        )
    return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def CardUpdate(request, cardpk):
    if request.method == "POST":
        Card = CardModel.objects.get(id=cardpk)
        Card.name = request.POST.get("Card_name")
        Card.price = request.POST.get("Card_price")
        Card.starrating = int(request.POST.get("Card_rating", 0))
        Card.description = request.POST.get("Card_description")
        Card.category_id = request.POST.get("category_id")

        image = request.FILES.get("Card_image")
        if image:
            Card.image.delete(save=False)
            Card.image = image

        Card.save()
        return redirect("/superuser/admincontrol/")


@user_passes_test(admin_only)
def CardDelete(request, cardpk):
    Card = CardModel.objects.get(id=cardpk)
    Card.delete()
    return redirect("/superuser/admincontrol/")


def Contact(request):
    if request.method == "POST":

        if not request.user.is_authenticated:

            request.session["contact_form"] = {
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "subject": request.POST.get("subject"),
                "message": request.POST.get("message"),
            }

            return redirect("/login/?next=/contact/")

        data = request.session.pop("contact_form", None)

        if data:
            ContactModel.objects.create(**data)
            messages.success(request, "Message sent successfully!")
            return redirect("/contact/")

        # normal submit
        ContactModel.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        messages.success(request, "Message sent successfully!")
        return redirect("/contact/")

    return render(request, "contact.html")


def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.warning(request, "Already logged in")
            return redirect("/")
        return render(request, "login.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            LoginHistory.objects.create(user=user)

            messages.success(request, "Login Successful")
            if user.is_staff:
                return redirect("/superuser/admincontrol/")
            else:
                return redirect("/")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")


def Register(request):
    if request.method == "GET":
        return render(request, "register.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/register/")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        messages.success(request, f"Account created for {user.username}")
        return redirect("/login/")


def Logout(request):
    logout(request)
    return redirect("/")


def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = User.objects.filter(email=email).first()

        if user:
            otp = PasswordResetOTP.objects.create(user=user)

            send_mail(
                "Your Password Reset Code",
                f"Your OTP code is: {otp.code}",
                "yourgmail@gmail.com",
                [email],
            )

        return redirect("verify_otp")

    return render(request, "send_otp.html")


def verify_otp(request):

    if request.method == "POST":

        code = request.POST.get("code")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # password match check
        if new_password != confirm_password:
            return render(
                request, "verify_otp.html", {"error": "Passwords do not match"}
            )

        # find OTP only
        otp_obj = PasswordResetOTP.objects.filter(code=code).first()

        if not otp_obj:
            return render(request, "verify_otp.html", {"error": "Invalid OTP"})

        # OPTIONAL: expiry check (10 min)
        if otp_obj.created_at < timezone.now() - timedelta(minutes=10):
            otp_obj.delete()
            return render(request, "verify_otp.html", {"error": "OTP expired"})

        # reset password
        user = otp_obj.user
        user.set_password(new_password)
        user.save()

        otp_obj.delete()

        return redirect("login")

    return render(request, "verify_otp.html")


@login_required(login_url="/login/")
def add_to_cart(request, cardpk):

    card = CardModel.objects.get(id=cardpk)

    if request.method == "POST":

        action = request.POST.get("action")
        size = request.POST.get("product_size")
        qty = int(request.POST.get("quantity", 1))

        # ================= SHOP HEART =================
        if action == "quick_cart":

            AddToCardModel.objects.create(
                user=request.user,
                product=card,
                size="Free Size",
                quantity=1,
                price=card.price,
            )

            messages.success(request, "Quick Added")
            return redirect("shop")

        # ================= SINGLE SHOP CART =================
        elif action == "cart":

            if not size:
                messages.error(request, "Please select size")
                return redirect("CardList", cardpk=cardpk)

            AddToCardModel.objects.create(
                user=request.user,
                product=card,
                size=size,
                quantity=qty,
                price=card.price,
            )

            messages.success(request, "Added to cart")
            return redirect("shop")

        # ================= ORDER =================
        elif action == "order":

            if not size:
                messages.error(request, "Please select size")
                return redirect("CardList", cardpk=cardpk)

            order = Order.objects.create(user=request.user)

            OrderItem.objects.create(
                order=order, product=card, size=size, quantity=qty, price=card.price
            )

            messages.success(request, "Order placed")
            return redirect("my_orders")

    return redirect("CardList", cardpk=cardpk)


@login_required(login_url="/login/")
def buy_now(request, cardpk):

    card = CardModel.objects.get(id=cardpk)

    if request.method == "POST":

        size = request.POST.get("product_size")
        qty = request.POST.get("quantity", 1)
        action = request.POST.get("action")

        if not size:
            messages.error(request, "Please select size")
            return redirect("CardList", cardpk=cardpk)

        if action == "order":

            order = Order.objects.create(user=request.user)

            OrderItem.objects.create(
                order=order,
                product=card,
                size=size,
                quantity=int(qty),
                price=card.price,
            )

            messages.success(request, "Order placed successfully")
            return redirect("my_orders")

        # cart action (optional)
        elif action == "cart":
            AddToCardModel.objects.create(
                user=request.user,
                product=card,
                size=size,
                quantity=int(qty),
                price=card.price,
            )

            messages.success(request, "Added to cart")
            return redirect("cart")

    return redirect("shop", cardpk=cardpk)


@login_required(login_url="/login/")
def checkout(request):

    cart_items = AddToCardModel.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Cart is empty")
        return redirect("cart_list")

    order = Order.objects.create(user=request.user)

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            size=item.size,
            quantity=item.quantity,
            price=item.price,
        )

    cart_items.delete()

    messages.success(request, "Order placed successfully")
    return redirect("my_orders")


@login_required(login_url="/login/")
def order_single(request, item_id):

    item = AddToCardModel.objects.get(id=item_id, user=request.user)

    order = Order.objects.create(user=request.user)

    OrderItem.objects.create(
        order=order,
        product=item.product,
        size=item.size,
        quantity=item.quantity,
        price=item.price,
    )

    item.delete()

    messages.success(request, "Order placed successfully")
    return redirect("my_orders")


@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):

    orders = Order.objects.exclude(status="cancelled").order_by("-created_at")
    return render(request, "superuser/order.html", {"orders": orders})


@user_passes_test(lambda u: u.is_staff)
def approve_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":
        order.status = "approved"
        order.save()

    messages.success(request, "Order is approved")
    return redirect("admin_orders")


@user_passes_test(lambda u: u.is_staff)
def reject_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":
        order.status = "rejected"
        order.save()
    messages.success(request, "Order is rejected")
    return redirect("admin_orders")


@login_required(login_url="/login/")
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "user_order_view.html", {"orders": orders})


@login_required(login_url="/login/")
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status == "pending":
        order.status = "cancelled"
        order.save()

    messages.success(request, "Order cancel ")
    return redirect("my_orders")


@login_required(login_url="/login/")
def cart_list(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    cart_items = AddToCardModel.objects.filter(user=request.user)

    AddToCardModel.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

    grand_total = 0

    for item in cart_items:
        item.total_price = item.price * item.quantity
        grand_total += item.total_price

    return render(
        request, "Addtocard_list.html", {"cart_items": cart_items, "total": grand_total}
    )


@login_required(login_url="/login/")
def remove_from_cart(request, item_id):
    item = AddToCardModel.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect("/cart/")


@user_passes_test(admin_only)
def AdminContactView(request):
    contact = ContactModel.objects.all()
    return render(request, "superuser/contactView.html/", {"contact": contact})


@user_passes_test(admin_only)
def AdminContactDelete(request, contactpk):
    contact = ContactModel.objects.get(id=contactpk)
    contact.delete()
    messages.success(request, f"Contact is successfully deleted")
    return redirect("/adminContact/view/")


@user_passes_test(admin_only)
def AdminLoginHistory(request):
    history = LoginHistory.objects.all().order_by("-login_time")
    return render(request, "superuser/login_history.html/", {"history": history})


@user_passes_test(admin_only)
def AdminLoginHistoryDeltete(request, logindetpk):
    login = LoginHistory.objects.get(id=logindetpk)
    login.delete()
    messages.success(request, f"Removal of User Login is successfully deleted")
    return redirect("/admincontrol/login/view/")

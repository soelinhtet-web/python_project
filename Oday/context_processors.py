from .models import AddToCardModel
from .models import CategoryModel

def cart_count(request):
    if request.user.is_authenticated:
        count = AddToCardModel.objects.filter(
            user=request.user,
            is_seen=False
        ).count()
    else:
        count = 0

    return {
        "cart_count": count
    }

def categories_processor(request):
    return {
        "categories": CategoryModel.objects.all()
    }


from .models import FooterSetting, FooterLink, CategoryModel


def footer_data(request):
    return {
        "footer": FooterSetting.objects.first(),
        "footer_links": FooterLink.objects.filter(is_active=True),
        "categories": CategoryModel.objects.filter(is_active=True),
    }


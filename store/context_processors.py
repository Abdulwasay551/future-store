from .models import Category

def categories_processor(request):
    """
    Context processor to make categories available in all templates
    """
    categories = Category.objects.all()
    return {'categories': categories} 
from .models import Category

def categories(request):
    """
    Get a list of all top-level categories.

    :return: A list of Category objects.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
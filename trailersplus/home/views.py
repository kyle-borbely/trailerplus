from product.models import Location
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from .models import ErrorPage
from my_store.models import StatePage, MyStore, Trailer
from product.models import Category


def error_404_view(request: HttpRequest, exception):
    previous = request.path
    previous_parts = previous.split('/')
    normalized_path = []
    redir = True
    for part in previous_parts:
        if not len(part):
            normalized_path.append('')
        elif part.lower() in ('en', 'es', 'trailer', 'inventory'):
            normalized_path.append(part.lower())
        elif part.lower() in [state.slug.lower() for state in StatePage.objects.all()]:
            normalized_path.append(StatePage.objects.get(slug_en__iexact=part).slug)
        elif part.lower() in [city.slug.lower() for city in MyStore.objects.all()]:
            normalized_path.append(MyStore.objects.get(slug_en__iexact=part).slug)
        elif part.lower() in set([cat.web_category.lower() for cat in Category.objects.all()]):
            normalized_path.append(Category.objects.filter(web_category__iexact=part)[0].web_category)
        elif part.lower() in set([cat.slug.lower() for cat in Category.objects.all()]):
            normalized_path.append(Category.objects.filter(slug__iexact=part)[0].slug)
        elif part.lower() in (
            'cargo',
            'utility',
            'hauler',
            'atv',
            'dump',
            'equipment',
            'gooseneck'
        ):
            if part.lower() == 'atv':
                normalized_path.append('ATV')
            else:
                normalized_path.append(part.capitalize())
        else:
            try:
                normalized_path.append(Trailer.objects.get(vin__iexact=part).vin)
            except (ObjectDoesNotExist, Trailer.DoesNotExist):
                redir = False
    if redir:
        return redirect('/'.join(normalized_path))
    try:
        error_page = ErrorPage.objects.get(slug_en__iexact="404")
    except (ObjectDoesNotExist, ErrorPage.DoesNotExist):
        return HttpResponse("Please create page with slug \"404\"")
    else:
        return redirect(error_page.url)


def search_redirect(request):
    url = f'{request.scheme}://{request.site_name}/'
    tt = request.GET.get('trailer-type', 'all')
    try:
        ts = Location.objects.get(store_city=request.GET.get('trailer-store', None)).get_slug()
    except ObjectDoesNotExist:
        return redirect(url)
    url += f'{ts}/inventory/'
    if tt != 'all':
        url += tt
    return redirect(url)

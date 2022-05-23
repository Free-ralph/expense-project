from django.core.paginator import Paginator
from django.http import HttpResponse
import json


def paginate_qs(request, queryset, paginate_by = None):
    if paginate_by is None:
        paginate_by = 4
    p_obj = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page')
    p_qs = p_obj.get_page(page_number)

    return p_qs

def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
       content_type = request.is_ajax() and 'application/json' or "text/html")
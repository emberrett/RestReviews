import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from .forms import AddRest
from .models import Rest
from django.contrib.auth import get_user_model
from main.view_functions import *
User = get_user_model()


CATEGORY_LIMIT = 30
REST_LIMIT = 300
ROWS_PER_PAGE = 10


def close_window(request):
    return render(request, 'close-window.html')


@login_required(login_url='/accounts/login')
def add_rest(request):
    if reached_max(user=request.user, rest_limit=REST_LIMIT):
        raise Exception(f"Rest limit reached {REST_LIMIT}")
    rests = Rest.objects.filter(user=request.user)
    categories = get_categories(rests)
    category_total = len(categories)
    if request.method == 'POST':
        if category_total <= CATEGORY_LIMIT:
            rest_post(request)
        return render(request, 'close-window.html')
    form = AddRest()
    category_max = category_total > CATEGORY_LIMIT
    return render(request, 'add-rest.html', {'form': form,
                                             'categories': categories,
                                             'category_max': category_max
                                             })


@login_required(login_url='/accounts/login')
def edit_rest(request, id):
    obj = get_object_or_404(Rest, id=id)
    rests = Rest.objects.filter(user=request.user)
    categories = get_categories(rests)
    category_total = len(categories)

    if obj.user != str(request.user):
        return HttpResponseForbidden('Unauthorized', status=401)
    if request.method == 'POST':
        if category_total < CATEGORY_LIMIT:
            rest_post(request, initial_obj=obj)
        return render(request, 'close-window.html')

    else:
        address = obj.address
        my_rating = obj.my_rating
        notes = obj.notes
        id = obj.pk
        rest_name = obj.rest

    submit_path = f'/edit-rest/{id}'
    category_max = category_total >= CATEGORY_LIMIT
    return render(request, f'edit-rest.html', {'my_rating': my_rating,
                                               submit_path: submit_path,
                                               'id': id,
                                               'rest_name': rest_name,
                                               'notes': notes,
                                               'address': address,
                                               'categories': categories,
                                               'current_category': obj.category,
                                               'category_max': category_max,
                                               'category_limit': CATEGORY_LIMIT})



@ login_required(login_url='/accounts/login')
def delete_rest(request, id):
    obj = Rest.objects.filter(id=id)
    if not obj.exists():
        return HttpResponseBadRequest(f'Rest with ID "{id}" does not exist.')
    if obj.values()[0]['user'] == str(request.user):
        obj.delete()
    else:
        return HttpResponseForbidden('Unauthorized', status=401)

    return render(request, 'close-window.html')




@ login_required(login_url='/accounts/login')
def show_rest(request):
    if request.method == 'POST':
        set_miles_bool(request)


    rests = Rest.objects.filter(user=request.user)
    rests = filter_search(request, rests)
    rests = filter_categories(request, rests)
    rests = set_distance(request, rests)

    page = get_page(request)
    start_index = get_start_index(page, ROWS_PER_PAGE)
    rests = rests.order_by(*eval(get_order_list_str(request))
                           )[start_index: start_index + ROWS_PER_PAGE]

    return render(request, 'my-rests.html',
                  {
                      'rests': rests,
                      'page': page,
                      'has_next': True if rests and len(rests) > ROWS_PER_PAGE * page else False,
                      'has_back': True if page > 1 else False,
                      'next_page': page + 1,
                      'back_page': page - 1,
                      'total_results': len(rests) if rests else 9,
                      'total_pages': math.ceil(len(rests) / ROWS_PER_PAGE) if rests else 1,
                      'categories': get_categories(rests),
                      'rest_max': reached_max(user=request.user, rest_limit=REST_LIMIT),
                      'rest_limit': REST_LIMIT
                  }
                  )


def homepage(request):
    has_rests = user_has_rests(request.user)
    return render(request, 'index.html', {'has_rests': has_rests, 'rest_max': reached_max(request.user, REST_LIMIT), 'rest_limit': REST_LIMIT})

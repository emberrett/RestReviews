from django.db.models.functions import Abs, Round
from django.db.models import F, Value, DecimalField
import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from .forms import AddRest
from .models import Rest
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()

CATEGORY_LIMIT = 30
REST_LIMIT = 300


@login_required(login_url='/accounts/login')
def add_rest(request):
    if reached_max(user=request.user):
        raise Exception(f"Rest limit reached {REST_LIMIT}")
    categories = get_categories(request.user)
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


def close_window(request):
    return render(request, 'close-window.html')

def rest_post(request, initial_obj=None):
    if initial_obj:
        form = AddRest(request.POST, instance=initial_obj)
    else:
        form = AddRest(request.POST)
    if request.POST.get('category_dropdown'):
        category = request.POST.get('category_dropdown', None)
    else:
        category = request.POST.get('category_text', None)

    if id:
        if not request.POST.get('latitude'):
            lat = initial_obj.latitude
            long = initial_obj.longitude
            address = initial_obj.address
            rating = initial_obj.rating
            rest = initial_obj.rest

        else:
            lat = request.POST.get('latitude', None)
            long = request.POST.get('longitude', None)
            address = request.POST.get('address', None)
            rating = request.POST.get('rating', None)
            if rating == 'undefined':
                rating = None
            rest = request.POST.get('rest', None)
    my_rating = None
    if request.POST.get('tried_radio') == 'true':
        my_rating = request.POST.get('my_rating')

    if form.is_valid():
        new_obj = form.save(commit=False)
        new_obj.latitude = lat
        new_obj.notes = request.POST.get('notes')
        new_obj.longitude = long
        new_obj.address = address
        new_obj.rating = rating
        new_obj.rest = rest
        new_obj.category = category
        new_obj.my_rating = my_rating
        new_obj.user = str(request.user)
        new_obj.save()


def reached_max(user):
    rest_count = Rest.objects.filter(user=user).count()
    if rest_count >= REST_LIMIT:
        return True
    return False


def homepage(request):
    rests = Rest.objects.filter(user=request.user)
    has_rests = False
    if rests:
        has_rests = True
    return render(request, 'index.html', {'has_rests': has_rests, 'rest_max': reached_max(request.user), 'rest_limit': REST_LIMIT})


def get_categories(user):
    categories = Rest.objects.filter(user=user).values('category').distinct()
    category_list = sorted([row["category"]
                           for row in categories], key=str.casefold)
    return category_list


@login_required(login_url='/accounts/login')
def edit_rest(request, id):
    obj = get_object_or_404(Rest, id=id)
    categories = get_categories(request.user)
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
        if request.POST.get("measurement") == "true":
            miles_bool = True
        else:
            miles_bool = False
        User.objects.filter(username=request.user).update(miles=miles_bool)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    start_index = 0
    rows_per_page = 10
    page = request.GET.get("page")
    startLong = request.GET.get("startLong")
    startLat = request.GET.get("startLat")
    if startLong and startLat:
        startLat = float(startLat)
        startLong = float(startLong)
    else:
        startLat = None
        startLong = None

    if not page:
        page = 1
    else:
        page = int(page)

    order = request.GET.get('order')
    order_list = []
    acceptable_values = ["category", "rest", "rating", "my_rating", "distance"]
    negative_values = []
    for value in acceptable_values:
        negative_values.append("-"+value)
    acceptable_values.extend(negative_values)
    if order:
        for col in order.split(','):
            if col not in acceptable_values:
                raise Exception(f"Invalid value for order parameter:{col}")
            if col.startswith('-'):
                order_list.append(
                    f"F('{str(col.replace('-',''))}').desc(nulls_last=True)")
            else:
                order_list.append(f"F('{str(col)}').asc(nulls_first=True)")
    else:
        order_list.append("F('id').asc(nulls_last=True)")
    order_list = "[" + ",".join(order_list) + "]"

    category_filter = request.GET.get("categories")

    if category_filter:
        if category_filter == "none":
            rests = None
        else:
            category_filter = category_filter.split(",")
            rests = Rest.objects.filter(
                user=request.user, category__in=category_filter)
    else:
        rests = Rest.objects.filter(user=request.user)
        if not rests:
            return HttpResponseRedirect('/add-rest')

    if not rests:
        total_results = 0
    else:
        total_results = len(rests)

    categories = [category['category']
                  for category in list(Rest.objects.filter(user=request.user).values('category'))]
    categories = sorted(set(categories))

    if page > 1:
        start_index = ((page - 1) * rows_per_page)

    if rests:
        if startLat and startLong:
            rests = rests.annotate(
                distance=Round(Abs(F('latitude') - Value(startLat, DecimalField())) + Abs(F('longitude') - Value(startLong, DecimalField())), precision=2, output_field=DecimalField(max_digits=5, decimal_places=2))).order_by(*eval(order_list))[
                start_index: start_index + rows_per_page]
        else:
            rests = rests.annotate(
                distance=Value(None, output_field=DecimalField())).order_by(*eval(order_list))[
                start_index: start_index + rows_per_page]

    has_next = False
    if total_results > rows_per_page * page:
        has_next = True
    has_back = False
    if page > 1:
        has_back = True
    if total_results:
        total_pages = math.ceil(total_results / rows_per_page)
    else:
        total_pages = 1

    return render(request, 'my-rests.html',
                  {
                      'rests': rests,
                      'page': page,
                      'has_next': has_next,
                      'has_back': has_back,
                      'next_page': page + 1,
                      'back_page': page - 1,
                      'total_results': total_results,
                      'total_pages': total_pages,
                      'categories': categories,
                      'rest_max': reached_max(user=request.user),
                      'rest_limit': REST_LIMIT
                  }
                  )
    # add to order query from current page
    # add to query if order query exists, if not start it
    # if col already in query, reset and order by that col,
    # if clicked col is at end of query and asc, switch to desc, else turn off order

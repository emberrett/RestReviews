from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from .forms import AddRest
from .models import Rest
from django.contrib.auth.decorators import login_required
import math
from django.db.models import F, Value, DecimalField
from django.db.models.functions import Abs, Round


def homepage(request):
    return render(request, 'index.html', context={})


@login_required(login_url='/accounts/login')
def add_rest(request):
    if request.method == 'POST':
        rest_post(request)
        return HttpResponseRedirect("/my-rests")
    form = AddRest()
    categories = get_categories(request.user)
    return render(request, 'add-rest.html', {'form': form, 'categories': categories})


def rest_post(request, initial_obj=None):
    if initial_obj:
        form = AddRest(request.POST, instance=initial_obj)
    else:
        form = AddRest(request.POST)
    print(request.POST)
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


def get_categories(user):
    categories = Rest.objects.filter(user=user).values('category').distinct()
    category_list = sorted([row["category"]
                           for row in categories], key=str.casefold)
    return category_list


@login_required(login_url='/accounts/login')
def edit_rest(request, id):
    obj = get_object_or_404(Rest, id=id)
    print(obj)
    if obj.user != str(request.user):
        return HttpResponseForbidden('Unauthorized', status=401)
    if request.method == 'POST':
        rest_post(request, initial_obj=obj)
        return HttpResponseRedirect(request.path)
 
    else:
        address = obj.address
        my_rating = obj.my_rating
        notes = obj.notes
        id = obj.pk
    categories = get_categories(request.user)
    submit_path = f'/edit-rest/{id}'
    return render(request, f'edit-rest.html', {'my_rating': my_rating,
                                               submit_path: submit_path,
                                               'id': id,
                                               'notes': notes,
                                               'address': address,
                                               'categories': categories,
                                               'current_category': obj.category})


@login_required(login_url='/accounts/login')
def delete_rest(request, id):
    obj = Rest.objects.filter(id=id)
    if not obj.exists():
        return HttpResponseBadRequest(f'Rest with ID "{id}" does not exist.')
    if obj.values()[0]['user'] == str(request.user):
        obj.delete()
    else:
        return HttpResponseForbidden('Unauthorized', status=401)
    
    return HttpResponseRedirect("/my-rests")


@login_required(login_url='/accounts/login')
def show_rest(request):
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
    if order:
        for col in order.split(','):
            if col.startswith('-'):
                order_list.append(
                    f"F('{str(col.replace('-',''))}').desc(nulls_last=True)")
            else:
                order_list.append(f"F('{str(col)}').asc(nulls_first=True)")
    else:
        order_list.append("F('id').asc(nulls_last=True)")
    order_list = "[" + ",".join(order_list) + "]"
    if page > 1:
        start_index = ((page - 1) * rows_per_page)

    if startLat and startLong:
        rests = Rest.objects.filter(user=request.user).annotate(
            distance=Round(Abs(F('latitude') - Value(startLat, DecimalField())) + Abs(F('longitude') - Value(startLong, DecimalField())),precision =2, output_field=DecimalField(max_digits=5, decimal_places=2)))
    else:
        rests = Rest.objects.filter(user=request.user).annotate(
            distance=Value(None, output_field=DecimalField()))

    rests = rests.order_by(*eval(order_list))[
        start_index: start_index + rows_per_page]
    total_results = Rest.objects.filter(user=request.user).count()
    if not total_results:
        return HttpResponseRedirect('/add-rest')
    has_next = False
    if total_results > rows_per_page * page:
        has_next = True
    has_back = False
    if page > 1:
        has_back = True
    total_pages = math.ceil(total_results / rows_per_page)

    return render(request, 'my-rests.html',
                  {
                      'rests': rests,
                      'page': page,
                      'has_next': has_next,
                      'has_back': has_back,
                      'next_page': page + 1,
                      'back_page': page - 1,
                      'total_results': total_results,
                      'total_pages': total_pages
                  }
                  )
    # add to order query from current page
    # add to query if order query exists, if not start it
    # if col already in query, reset and order by that col,
    # if clicked col is at end of query and asc, switch to desc, else turn off order

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from .forms import AddRest
from .models import Rest
from django.contrib.auth.decorators import login_required
import math


def homepage(request):
    return render(request, 'index.html', context={})


@login_required(login_url='/accounts/login')
def add_rest(request):
    if request.method == 'POST':
        rest_post(request)
        return HttpResponseRedirect('my-rests/1')
    else:
        form = AddRest()

    return render(request, 'add-rest.html', {'form': form})


def rest_post(request, initial_obj=None):
    if initial_obj:
        form = AddRest(request.POST, instance=initial_obj)
    else:
        form = AddRest(request.POST)

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
                rating = 0
            rest = request.POST.get('rest', None)

    if form.is_valid():
        new_obj = form.save(commit=False)
        new_obj.latitude = lat
        new_obj.longitude = long
        new_obj.address = address
        new_obj.rating = rating
        new_obj.rest = rest
        new_obj.user = str(request.user)
        new_obj.save()


@login_required(login_url='/accounts/login')
def edit_rest(request, id):

    obj = get_object_or_404(Rest, id=id)
    if obj.user != str(request.user):
        return HttpResponseForbidden('Unauthorized', status=401)
    if request.method == 'POST':
        rest_post(request, initial_obj=obj)
        return HttpResponseRedirect('/my-rests/1')
    else:
        form = AddRest(instance=obj)
        address = obj.address

    submit_path = f'/edit-rest/{id}'
    return render(request, f'edit-rest.html', {'form': form, submit_path: submit_path, 'address': address})


@login_required(login_url='/accounts/login')
def delete_rest(request, id):
    obj = Rest.objects.filter(id=id)
    if not obj.exists():
        return HttpResponseBadRequest(f'Rest with ID "{id}" does not exist.')
    if obj.values()[0]['user'] == str(request.user):
        obj.delete()
    else:
        return HttpResponseForbidden('Unauthorized', status=401)
    return HttpResponseRedirect('../my-rests/1')


@login_required(login_url='/accounts/login')
def show_rest(request, page):


    # only get 25 results at a time, or do we just fill the page?
    start_index = 0
    rows_per_page = 10
    if page > 1:
        start_index = ((page - 1) * rows_per_page)
    rests = Rest.objects.filter(user=request.user).order_by('id')[
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

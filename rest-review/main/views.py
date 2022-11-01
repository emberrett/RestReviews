from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from .forms import AddRest
from .models import Rest
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'index.html', context={})


@login_required(login_url='/accounts/login')
def add_rest(request):
    if request.method == 'POST':
        form = AddRest(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
        return HttpResponseRedirect('my-rests/1')
    else:
        form = AddRest()

    return render(request, 'add-rest.html', {'form': form})


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
def edit_rest(request, id):

    obj = get_object_or_404(Rest, id=id)
    if obj.user != str(request.user):
        return HttpResponseForbidden('Unauthorized', status=401)
    if request.method == 'POST':
        form = AddRest(request.POST, instance=obj)
        form.user = request.user
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        return HttpResponseRedirect('/my-rests/1')
    else:

        form = AddRest(instance=obj)

    submit_path = f'/edit-rest/{id}'
    return render(request, f'edit-rest.html', {'form': form, submit_path: submit_path})


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
    has_next = False
    if total_results > rows_per_page * page:
        has_next = True
    has_back = False
    if page > 1:
        has_back = True

    return render(request, 'my-rests.html',
                  {
                      'rests': rests,
                      'page': page,
                      'has_next': has_next,
                      'has_back': has_back,
                      'next_page': page + 1,
                      'back_page': page - 1
                  }
                  )

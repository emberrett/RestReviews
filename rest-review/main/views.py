from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
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
        #form = form_object.save(commit=False)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
        return HttpResponseRedirect('my-rests')
    else:
        form = AddRest()

    return render(request, 'add-rest.html', {'form': form})


@login_required(login_url='/accounts/login')
def edit_rest(request, **kwargs):
    id = kwargs['id']
    obj = get_object_or_404(Rest, id=id)
    if request.method == 'POST':
        form = AddRest(request.POST, instance=obj)
        form.user = request.user
        if form.is_valid():
            print("HERE HERE HERE")
            obj = form.save(commit=False)
            obj.save()
        return HttpResponseRedirect('my-rests')
    else:
        form = AddRest(instance=obj)

    return render(request, 'edit-rest.html', {'form': form})


@login_required(login_url='/accounts/login')
def show_rest(request):
    rests = Rest.objects.filter(user=request.user)
    return render(request, 'my-rests.html', {'rests': rests})

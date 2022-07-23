from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user
from .forms import AddRest
from main.models import Rest
from django.contrib.auth.decorators import login_required

def homepage(request):
  return render(request, 'index.html', context={})

@login_required(login_url='/accounts/login')
def get_rest(request):
    if request.method == 'POST':
        user = request.user.id
        form = AddRest(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')

    else:
        user = get_user(request)
        form = AddRest(initial={'user': user})

    return render(request, 'add-rest.html', {'form': form})

@login_required(login_url='/accounts/login')
def show_rest(request):
    query_results = Rest.objects.all()
    return render(request, 'my-rests.html', {'rests': query_results})

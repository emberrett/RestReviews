from django.shortcuts import render
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
        form = AddRest(request.POST, user=request.user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('my-rests')
    else:
        form = AddRest(user=request.user)
        

    return render(request, 'add-rest.html', {'form': form})

@login_required(login_url='/accounts/login')
def show_rest(request):
    rests = Rest.objects.filter(user=request.user)
    return render(request, 'my-rests.html', {'rests': rests})
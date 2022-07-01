from django.shortcuts import render

def homepage(request):
  return render(request, 'index.html', context={})

def createpost(request):
        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('content'):
                post=Post()
                post.title= request.POST.get('title')
                post.content= request.POST.get('content')
                post.save()
                
                return render(request, 'add_rest.html')  

        else:
                return render(request,'add_rest.html')
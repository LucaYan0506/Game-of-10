from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Game

from guest_user.decorators import allow_guest_user

@allow_guest_user
def hello_guest(request):
    request.user.first_name = 'tes'
    request.user.save()
    return HttpResponse(f"Hello, Guest{request.user.username}!")

# Create your views here.
def index_view(request):
    message = request.GET.get('message')
    return render(request,'index.html',{'message':message})


def match_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Error, no user")
    if request.method == 'POST':
        code = request.POST['code']
        '''
        verify user and/or login as guest
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "hotelManagement/login.html", {
                "message": "Invalid username and/or password."
            })
        '''
        game = Game.objects.filter(code=code)
        if len(game) == 1:
            return render(request,'match.html',{
                'creatorName':game[0].creator_name,
                'code':game[0].code,
                'board':game[0].board,
                'player2':request.user.username
                })

        return HttpResponseRedirect(reverse('index') + '?message=Invalid code')

    return HttpResponse('Error, you are in the wrong page')
    


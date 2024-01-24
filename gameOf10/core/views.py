from django.shortcuts import render,reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseRedirect
from .models import Game,User
import uuid

def generateGuestUser(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Hello {request.user}")
    
    guest_username = f'guest_{uuid.uuid4().hex[:8]}'
    while User.objects.filter(username=guest_username).exists():
        guest_username = f'guest_{uuid.uuid4().hex[:8]}'
        
    guestUser = User.objects.create(username = guest_username, isGuest = True, )
    guestUser.set_unusable_password()
    guestUser.save()

    user = authenticate(request, username=guest_username,password = None)
    login(request, user)

    return HttpResponse(f"Hello, {guestUser.username}!")

# Create your views here.
def index_view(request):
    message = request.GET.get('message')
    return render(request,'index.html',{'message':message})


def match_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Error, no user")
    if request.method == 'POST':
        code = request.POST['code']
        game = Game.objects.filter(code=code)
        if len(game) == 1:
            player = None
            if game[0].creator_name.id == request.user.id:
                if game[0].player != None:
                    player = game[0].player.username
            else:
                if game[0].player == None:
                    game[0].player = request.user
                    player = request.user.username
                else:
                    return HttpResponse("This room is full, please create a new game or join another game")
            return render(request,'match.html',{
                'creatorName':game[0].creator_name.username,
                'code':game[0].code,
                'board':game[0].board,
                'player':player
                })

        return HttpResponseRedirect(reverse('index') + '?message=Invalid code')

    return HttpResponse('Error, you are in the wrong page')
    

def getGameInfo(request):
    if not request.user.is_authenticated:
        pass#you are in the wrong url
    if not request.method == 'POST':
        pass#you are wrong in the wrong method

    pass#return json 
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
        
    guestUser = User(username = guest_username, isGuest = True)
    guestUser.set_password('test')
    guestUser.save()
    user = authenticate(request, username=guest_username,password = 'test')
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
            cards = None
            if game[0].creator_name.id == request.user.id:
                cards = game[0].creator_cards
                if game[0].player != None:
                    player = game[0].player.username
            else:
                cards = game[0].player_cards
                if game[0].player == None:
                    game[0].player = request.user
                    game[0].save()
                    player = request.user.username
                elif game[0].player.id == request.user.id:
                    player = request.user.username
                else:
                    return HttpResponse("This room is full, please create a new game or join another game")
            return render(request,'match.html',{
                'board_size':range(1,14),
                'creatorName':game[0].creator_name.username,
                'cards':cards,
                'code':game[0].code,
                'board':game[0].board,
                'player':player,
                })

        return HttpResponseRedirect(reverse('index') + '?message=Invalid code')

    return HttpResponse('Error, you are in the wrong page')
    

def getGameInfo(request):
    if not request.user.is_authenticated:
        pass#you are in the wrong url
    if not request.method == 'POST':
        pass#you are wrong in the wrong method

    pass#return json 
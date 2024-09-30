from django.shortcuts import render,reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Game,User
import uuid, json, random, math
from django.db.models import Q
from django.db import IntegrityError

OP = ['-','+','/','*']

def solveEquation(equation):
    opCount = 0 #count only multiplication and divition
    equationList = []
    currN = 0
    for x in equation:
        if x.isdigit():
            currN = currN * 10 + int(x)
        else:
            if x in '*/':
                opCount += 1
            equationList.append(currN)
            equationList.append(x)
            currN = 0

    #save last num
    equationList.append(currN)

    #do the multiplication and division first
    while opCount:
        newEq = []
        for i in range(len(equationList)):
            if equationList[i] == '*':
                opCount -= 1
                temp = equationList[i - 1] * equationList[i + 1]
                newEq = equationList[0:i - 1] + [temp]
                if i + 2 < len(equationList):
                    newEq = newEq + equationList[i + 2:]
                equationList = newEq
                break
            elif equationList[i] == '/':
                opCount -= 1
                temp = 0.0
                if equationList[i + 1] == 0:
                    return "Error"
                temp = equationList[i - 1] / equationList[i + 1]
                newEq = equationList[0:i - 1] + [temp]
                if i + 2 < len(equationList):
                    newEq = newEq + equationList[i + 2:]
                equationList = newEq
                break

    print(equationList)
    res = 0.00
    sign = 1

    for x in equationList:
        if x == '+':
            sign = 1
        elif x == '-':
            sign = -1
        else:
            res += x * sign


    return res

def checkEquation(equation,getCardFromLeft):
     #make sure that the equation is valid. E.g. start & endwith a number and doesn't have 2 operation next to each other
    if (equation[0] in ['*','/'] and not getCardFromLeft) or equation[len(equation) - 1] in OP:
        return {'valid':False,'message':'You must create a valid equation'}

    prev = equation[0]
    for i in range(1, len(equation) - 1):
        if equation[i] in OP and prev in OP:
            return {'valid':False,'message':'You must create a valid equation'}
        prev = equation[i]


    result = solveEquation(equation)
    print(f'{equation} = {result}')

    if result == 'Error':
        return {'valid':False,'message':"Your equation is invalid"}

    if (result <= 0):
        return {'valid':False,'message':"Your equation can't be less or equal to 0"}


    if (math.log10(result) % 1 != 0):
        return {'valid':False,'message':'Your equation must be equal to the nth power of 10. (e.g. 0.1 1 10 100 etc)'}

        

    return {'valid':True,'message':'Success'}

def isValidAction(board, action):
    sameColomn = sameRow = True
    prev = action[0]
    equation = ""
    
    #check if all cards are placed in the same row/column
    for i in range(1,len(action)):
        if prev['row'] != action[i]['row']:
            sameRow = False
        if prev['column'] != action[i]['column']:
            sameColomn = False
        
        if not sameColomn and not sameRow:
            return {'valid':False,'message':'Your cards must be in the same row or column'}
        
    #check if in the same row/column of the action from the most left card to the most right card is occupied by a number 
    getCardFromLeft = False#this variable checks if our equation have gotten card from the board (in other words not from action) as the first elem
    if sameColomn:
        firstActionRow = 14 
        lastActionRow = -1
        column = int(action[0]['column'])

        for x in action:
            firstActionRow = min(firstActionRow,int(x['row']))
            lastActionRow = max(lastActionRow,int(x['row']))

        lastActionRow = max(lastActionRow,firstActionRow)#make sure that we get the whole line as equation

        for i in range(firstActionRow - 1, -1, -1):
            if board[i][column] != ' ':
                getCardFromLeft = True
                equation += board[i][column]
            else:
                break

        equation = equation[::-1]

        for i in range(firstActionRow,lastActionRow + 1):
            if board[i][column] == ' ':
                return {'valid':False,'message':'You must create a valid equation'}
            equation += board[i][column]

        for i in range(lastActionRow + 1, 13):
            if board[i][column] != ' ':
                equation += board[i][column]
            else:
                break

        res = checkEquation(equation, getCardFromLeft)
        if res['valid']:
            return res
    if sameRow:
        firstActionCol = 14 
        lastActionCol = -1
        row = int(action[0]['row'])

        for x in action:
            firstActionCol = min(firstActionCol,int(x['column']))
            lastActionCol = max(lastActionCol,int(x['column']))

        lastActionCol = max(lastActionCol,firstActionCol)#make sure that we get the whole line as equation

        for j in range(firstActionCol - 1, -1, -1):
            if board[row][j] != ' ':
                getCardFromLeft = True
                equation += board[row][j]
            else:
                break

        equation = equation[::-1]
        for j in range(firstActionCol,lastActionCol + 1):
            if board[row][j] == ' ':
                return {'valid':False,'message':'You must create a valid equation'}
            equation += board[row][j]

        for j in range(lastActionCol + 1, 13):
            if board[row][j] != ' ':
                equation += board[row][j]
            else:
                break

    return checkEquation(equation,getCardFromLeft)

def getNewCard(val):
    isOp = False
    for x in OP:
        if val == x:
            isOp = True

    if isOp:
        return random.choice(OP)

    return str(random.choice(range(10)))




# Create your views here.
def showProfile(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Hello {request.user}")
    
    #generate guest user
    guest_username = f'guest_{uuid.uuid4().hex[:8]}'
    while User.objects.filter(username=guest_username).exists():
        guest_username = f'guest_{uuid.uuid4().hex[:8]}'
        
    guestUser = User(username = guest_username, isGuest = True)
    guestUser.set_password('test')
    guestUser.save()
    user = authenticate(request, username=guest_username,password = 'test')
    login(request, user)

    return HttpResponseRedirect(reverse('index') + f"?message=Hello, {guestUser.username}!")

def index_view(request):
    if request.user.is_authenticated:
        game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
        if game.exists():
            return HttpResponseRedirect(reverse('match'))

    return render(request,'index.html',{
        'message':request.GET.get('message'),
        'isLogin':request.user.is_authenticated,
        })

def match_view(request):
    if not request.user.is_authenticated:
         #generate guest user
        guest_username = f'guest_{uuid.uuid4().hex[:8]}'
        while User.objects.filter(username=guest_username).exists():
            guest_username = f'guest_{uuid.uuid4().hex[:8]}'
            
        guestUser = User(username = guest_username, isGuest = True)
        guestUser.set_password('test')
        guestUser.save()
        user = authenticate(request, username=guest_username,password = 'test')
        login(request, user)
        #return HttpResponseRedirect(reverse('index') + '?message=Please log in or create an account')
    if request.method == 'POST':
        code = request.POST['code']
        game = Game.objects.filter(code=code)
        if game.exists():
            game = game[0]
        else:
            return HttpResponseRedirect(reverse('index') + '?message=Invalid code')
        
        cards = None
        myScore = 0
        enemyScore = 0
        if game.creator_name.pk == request.user.pk:
            cards = game.creator_cards
            enemyScore = game.player_score
            myScore = game.creator_score
        else:
            cards = game.player_cards
            myScore = game.player_score
            enemyScore = game.creator_score
            if game.player == None:
                game.player = request.user
                game.save()
            elif game.player.pk == request.user.pk:
                pass
            else:
                return HttpResponse("This room is full, please create a new game or join another game")
        
        myTurn = (game.turn == 1 and game.creator_name.pk == request.user.pk) or  (game.turn == 2 and game.player.pk == request.user.pk)
        
        lastMove = None
        if game.lastMove is not None:
            lastMove = json.loads(game.lastMove.replace("'",'"'))
        return render(request,'match.html',{
            'board_size':range(13),
            'creatorName':game.creator_name.username,
            'cards':cards,
            'code':game.code,
            'board':game.board,
            'myTurn':myTurn,
            'myScore':myScore,
            'enemyScore':enemyScore,
            'lastMove':lastMove
            })

    elif request.method == 'GET':
            game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
            if game.exists():
                game = game[0]
            else:
                return HttpResponse({f"user {request.user.username} didn't join any game"})
            
            cards = None
            myScore = 0
            enemyScore = 0
            if game.creator_name.pk == request.user.pk:
                cards = game.creator_cards
                enemyScore = game.player_score
                myScore = game.creator_score
            else:
                cards = game.player_cards
                myScore = game.player_score
                enemyScore = game.creator_score
            myTurn = (game.turn == 1 and game.creator_name.pk == request.user.pk) or  (game.turn == 2 and game.player.pk == request.user.pk)
            lastMove = None
            if game.lastMove is not None:
                lastMove = json.loads(game.lastMove.replace("'",'"'))
            return render(request,'match.html',{
                'board_size':range(13),
                'creatorName':game.creator_name.username,
                'cards':cards,
                'code':game.code,
                'board':game.board,
                'myTurn':myTurn,
                'myScore':myScore,
                'enemyScore':enemyScore,
                'lastMove':lastMove
                })
    return HttpResponse('Error, you are in the wrong page')

def submitAction(request):
    if not request.user.is_authenticated or not request.method == 'POST':
        return HttpResponse('You are in the wrong page')
    game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
    if game.exists():
        game = game[0]
    else:
        return JsonResponse({'message':f"user {request.user.username} didn't join any game"},status=400)

    board_copy = [[' ' for _ in range(13)] for _ in range(13)]
    action = json.loads(request.POST['action'])
    opCount = 0
    numberCount = 0
    i = j = 0    

    if not action:
        return JsonResponse({'message':'Error, no card placed'},status=400)

    for x in game.board:
        if j == 13:
            i += 1
            j = 0

        board_copy[i][j] = x
        j += 1
        

    for x in action:
        board_copy[int(x['row'])][int(x['column'])] = x['val']
        if x['val'] in OP:
            opCount += 1
        else:
            numberCount += 1

    check = isValidAction(board_copy,action)
    if not check['valid']:
        return JsonResponse({'message':check['message']},status=400)
    
    board = ""

    for row in board_copy:
        for x in row:
            board += x
    
    game.board = board

    if game.turn == 1:
        game.turn = 2
    else:
        game.turn = 1

    if request.user == game.creator_name:
        oldCard = list(game.creator_cards)
        newCard = ''
        for x in action:
            for i in range(len(oldCard)):
                if oldCard[i] == x['val']:
                    newCard += getNewCard(oldCard[i])
                    oldCard[i] = ' '

        for x in oldCard:
            if x != ' ':
                newCard += x
        
        game.creator_cards = newCard
        game.creator_score = game.creator_score + opCount + (numberCount == 4) * 4
        game.lastMove = action
        game.save()
    else:
        oldCard = list(game.player_cards)
        newCard = ''
        for x in action:
            for i in range(len(oldCard)):
                if oldCard[i] == x['val']:
                    newCard += getNewCard(oldCard[i])
                    oldCard[i] = ' '

        for x in oldCard:
            if x != ' ':
                newCard += x
        
        game.player_cards = newCard
        game.player_score = game.player_score + opCount + (numberCount == 4) * 4
        game.lastMove = action
        game.save()

    return JsonResponse({},status=200)

def discardCard(request):
    if not request.user.is_authenticated or not request.method == 'POST':
        return HttpResponse('You are in the wrong page')
    
    selectedCard = request.POST['selectedCard']
    if not selectedCard:
        return JsonResponse({'message':"invalid card selected"},status=400)

    game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
    if game.exists():
        game = game[0]
    else:
        return JsonResponse({'message':f"user {request.user.username} didn't join any game"},status=400)
    
    if request.user == game.creator_name:
        newCard = ''
        found = False
        for x in game.creator_cards:
            if not found and x == selectedCard:
                found = True
                newCard += getNewCard(selectedCard)
            else:
                newCard += x
        
        if not found:
            return JsonResponse({'message':"invalid card selected"},status=400)

        game.creator_cards = newCard
        game.turn = 2
        game.save()
    else:
        newCard = ''
        found = False
        for x in game.player_cards:
            if not found and x == selectedCard:
                found = True
                newCard += getNewCard(selectedCard)
            else:
                newCard += x
        
        if not found:
            return JsonResponse({'message':"invalid card selected"},status=400)

        game.player_cards = newCard
        game.turn = 1
        game.save()

    
    return JsonResponse({},status=200)

def getMyTurn(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are in the wrong page')
    game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
    if game.exists():
        game = game[0]
    else:
        return JsonResponse({'message':f"user {request.user.username} didn't join any game"})
    
    myTurn = (game.turn == 1 and game.creator_name == request.user) or  (game.turn == 2 and game.player == request.user)

    return JsonResponse({'myTurn':myTurn})

def loginView(request):
    if request.method == 'POST':
        # Validate and sanitize input
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # Authentication failed
            return HttpResponse('Invalid username or password')

    # Handle GET request or failed authentication
    # You might want to render a login page or redirect to a login view
    return HttpResponse('You are in the wrong page')

def newGameView(request):
    if not request.user.is_authenticated or not request.method == 'POST':
        return HttpResponse('You are in the wrong page')
    
    game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
    if game.exists():
        game = game[0]
    else:
        return JsonResponse({'message':f"user {request.user.username} didn't join any game"},status=400)
    
    game.board = ''
    game.creator_score = 0
    game.player_score = 0
    game.lastMove = '[]'
    game.save()

    return HttpResponseRedirect(reverse('match'))

def registerView(request):
    if not request.method == 'POST':
        return HttpResponse('You are in the wrong page')
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    username = request.POST["username"]
    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmPassword"]
    if password != confirmation:
        return JsonResponse({
            "message": "Passwords must match."
        }, status=400)

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, "", password)
        user.save()
    except IntegrityError:
        return JsonResponse({
             "message": "Username already taken."
        }, status=400)
    login(request, user)
    return HttpResponseRedirect(reverse("index"))

#last move
from django.shortcuts import render,reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Game,User
import uuid, json, random, math
from django.db.models import Q

OP = ['-','+','/','*']

def solveEquation(equation):
    result = 0
    operand = 0
    operator = '+'
    pending_operation = None  # To handle multiplication or division

    for char in equation:
        if char.isdigit():
            operand = operand * 10 + int(char)
        elif char in {'+', '-'}:
            result = perform_pending_operation(result, operator, operand, pending_operation)
            operator = char
            operand = 0
            pending_operation = None  # Reset pending operation for addition or subtraction
        elif char == '*':
            pending_operation = ('*', operand)
            operand = 0
        elif char == '/':
            pending_operation = ('/', operand)
            operand = 0

    #do last operation
    result = perform_pending_operation(result, operator, operand, pending_operation)

    return result

def perform_pending_operation(result, operator, operand, pending_operation):
    if pending_operation:
        op, value = pending_operation
        if op == '*':
            operand *= value
        elif op == '/':
            if value != 0:
                operand /= value

    if operator == '+':
        result += operand
    elif operator == '-':
        result -= operand

    return result

def isValidAction(board, action):
    sameColomn = sameRow = True
    prev = action[0]
    
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
        equation = ""

        for x in action:
            firstActionRow = min(firstActionRow,int(x['row']))
            lastActionRow = max(lastActionRow,int(x['row']))

        for i in range(firstActionRow - 1, -1, -1):
            if board[i][column] != ' ':
                getCardFromLeft = True
                equation += board[i][column]

        equation = equation[::-1]

        for i in range(firstActionRow,lastActionRow + 1):
            if board[i][column] == ' ':
                return {'valid':False,'message':'You must create a valid equation'}
            equation += board[i][column]

        for i in range(lastActionRow + 1, 13):
            if board[i][column] != ' ':
                equation += board[i][column]

    elif sameRow:
        firstActionCol = 14 
        lastActionCol = -1
        row = int(action[0]['row'])
        equation = ""

        for x in action:
            firstActionCol = min(firstActionCol,int(x['column']))
            lastActionCol = max(lastActionCol,int(x['column']))

        for j in range(firstActionCol - 1, -1, -1):
            if board[row][j] != ' ':
                getCardFromLeft = True
                equation += board[row][j]

        equation = equation[::-1]

        for j in range(firstActionCol,lastActionCol + 1):
            if board[row][j] == ' ':
                return {'valid':False,'message':'You must create a valid equation'}
            equation += board[row][j]

        for j in range(lastActionCol + 1, 13):
            if board[row][j] != ' ':
                equation += board[row][j]

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

    if (result == 0):
        return {'valid':False,'message':"Your equation can't be 0"}


    if (math.log10(result) % 1 != 0):
        return {'valid':False,'message':'Your equation must be equal to the nth power of 10. (e.g. 0.1 1 10 100 etc)'}

        

    return {'valid':True,'message':'Success'}


def getNewCard(val):
    isOp = False
    for x in OP:
        if val == x:
            isOp = True

    if isOp:
        return random.choice(OP)

    return str(random.choice(range(10)))


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
            
            myTurn = (game[0].turn == 1 and game[0].creator_name.id == request.user.id) or  (game[0].turn == 2 and game[0].player.id == request.user.id)
            
            return render(request,'match.html',{
                'board_size':range(13),
                'creatorName':game[0].creator_name.username,
                'cards':cards,
                'code':game[0].code,
                'board':game[0].board,
                'player':player,
                'myTurn':myTurn,
                })

        return HttpResponseRedirect(reverse('index') + '?message=Invalid code')

    return HttpResponse('Error, you are in the wrong page')
    

def submitAction(request):
    if not request.user.is_authenticated or not request.method == 'POST':
        return HttpResponse('You are in the wrong page')
    game = Game.objects.filter(Q(creator_name=request.user) | Q(player=request.user))
    if game.exists():
        game = game[0]
    else:
        return JsonResponse({'message':f"user {request.user.username} didn't join any game"})

    board_copy = [[' ' for _ in range(13)] for _ in range(13)]
    action = json.loads(request.POST['action'])
    i = j = 0    
    for x in game.board:
        if j == 13:
            i += 1
            j = 0

        board_copy[i][j] = x
        j += 1
        

    for x in action:
        board_copy[int(x['row'])][int(x['column'])] = x['val']

    check = isValidAction(board_copy,action)
    print(check['message'])
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
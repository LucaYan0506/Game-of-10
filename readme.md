# Game of power of 10
## Live demo

## Context
**Development team:**
* Zhong Yi Yan - backend developer
* Oleksandr- frontend developer

## Rule of the game
It is a maths based game. The are 2 players in this game. Initially, each player will have 6 cards:  
* 4 numbers
* 2 operations  

For each round the player needs to use as much operation as possible to create an equation that is equal to the power of 10. The player will get 1 point for each operation used. If the player used all the numbers, he will get 4 points. The player that reach 11 first wins.   
If in a round the player can't make an equation that is equal to the power of 10, he can skip that turn by discarding one card (therefore draw a new one).  
You can make horizontal and vertical equation. You can also use cards that are already placed in the table.

## How to create a match
In the home page, there is button that allow you to create a new match. After clicking it, you can change the follwing setting:  
* easy mode: if you enable this mode, it will help you to calculate the equation
* limit time: you can set the limit time that each player has for each turn to make the equation. It the time expired, the player must discard a card and skip this turn.
* include more operation: you can include more complicated operator such as factorial (!)
## How to join a match
  
  
  
## How to run the website in your local network:
Make sure that [python](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installation/) and [pipenv](https://pipenv.pypa.io/en/latest/install/) are installed. Run the following code to:   
#### set up virtual environment 
```
pipenv shell
pip install -r requirements.txt
```
#### create a superuser (optional)
```
python manage.py createsuperuser
```
#### run the app
```
python manage.py migrate
python manage.py runserver
```

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import config

def play(request):
    #if it is new game, than board don't exists yet
    if not request.session.get('board'):
        #crate new board
        board = init_board()
        #save board in session
        request.session['board'] = board
        #set first turn as null
        turn = 0
        request.session['turn'] = turn   
    return render(request, 'four_in_a_row/index.html')

def clicked(request, cord):
    column = cord[0]
    if request.session.get('win'):
        return HttpResponseRedirect(reverse_lazy('four_in_a_row:play'))
    else:
        takeTheLowest(request, column)
        checkTheResult(request)
        return HttpResponseRedirect(reverse_lazy('four_in_a_row:play'))

def reset(request):
    try:
        del request.session['board']
        del request.session['win']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse_lazy('four_in_a_row:play'))


def init_board():
    board = {}
    for y in config.vertically:
        for x in config.horizontally:
            coordinates = str(x)+str(y)
            board.update({coordinates:'white'})
    return board

def getColor(request):
    color = ''
    turn = request.session['turn']
    if turn % 2 == 0:
        color = 'red'
    else:
        color = 'blue'
    return color

def takeTheLowest(request, column):
    board = request.session['board']
    turn = request.session['turn']
    color = getColor(request)
    for row in reversed(range(config.y)):
        cord = column+str(row)
        if board[cord] == "white":
            board[cord] = color
            turn += 1
            request.session['prevTurn'] = cord
            break

    request.session['board'] = board
    request.session['turn'] = turn

def checkTheResult(request):
    board = request.session['board']
    red_x = 0
    red_y = 0
    blue_x = 0
    blue_y = 0

    #4 in a row
    for y in config.vertically:
        for x in config.horizontally:
            coordinates = str(x)+str(y)
            if board[coordinates] == "red":
                red_x += 1
            else:
                red_x = 0
            if red_x == 4:
                request.session['win'] = "Red"
            if board[coordinates] == "blue":
                blue_x += 1
            else:
                blue_x = 0
            if blue_x == 4:
                request.session['win'] = "Blue"
        red_x = 0
        blue_x = 0
    #4 in a column
    for x in config.horizontally:
        for y in config.vertically:
            coordinates = str(x)+str(y)
            if board[coordinates] == "red":
                red_y += 1
            else:
                red_y = 0
            if red_y == 4:
                request.session['win'] = "Red"
            if board[coordinates] == "blue":
                blue_y += 1
            else:
                blue_y = 0
            if blue_y == 4:
                request.session['win'] = "Blue"
        red_y = 0
        blue_y = 0
    #diagonals
    red = 0
    blue = 0
    diagonals = getDiagonals(config.x, config.y, config.inRow)
    for diagonal in diagonals:
        for coordinates in diagonal:
            if board[coordinates] == 'red':
                red += 1
            else:
                red = 0
            if red == 4:
                request.session['win'] = "Red"
            if board[coordinates] == 'blue':
                blue += 1
            else:
                blue = 0
            if blue == 4:
                request.session['win'] = "Blue"
        red = 0
        blue = 0


def getDiagonals(horizontally, vertically, minDiagonal):
    diagonals = []
    diagonal = []
    #from up to down
    for x in range(horizontally):
        y = 0
        while x < horizontally and y < vertically:    
            diagonal.append(str(x) + str(y))
            x += 1
            y += 1
        if len(diagonal) >= minDiagonal :
            diagonals.append(diagonal)
        diagonal = []
        
    for y in range(1, vertically):
        x = 0
        while x < horizontally and y < vertically:    
            diagonal.append(str(x) + str(y))
            x += 1
            y += 1
        if len(diagonal) >= minDiagonal :
            diagonals.append(diagonal)
        diagonal = []        

    #from down to up
    for x in range(horizontally):
        y = vertically - 1
        while x < horizontally and y >= 0:

            diagonal.append(str(x) + str(y))
            x += 1
            y -= 1
        if len(diagonal) >= minDiagonal :
            diagonals.append(diagonal)
        diagonal = []     

    for y in reversed(range(vertically)):
        if y == vertically - 1:
            continue
        x = 0
        while x < horizontally and y >= 0:    
            diagonal.append(str(x) + str(y))
            x += 1
            y -= 1
        if len(diagonal) >= minDiagonal :
            diagonals.append(diagonal)
        diagonal = []       

    return diagonals
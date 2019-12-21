from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

import random
from .forms import PlayForm

def play(request):
    board = init_board()
    #set default balance to 1000 points
    if request.session.get('balance'):
        balance = request.session['balance']
    else:
        balance = 1000
        request.session['balance'] = balance

    #create blank PlayForm
    play_form = PlayForm(initial={'balance': balance})

    return render(request, 'slot_machine/index.html', {'board':board, 'play_form':play_form})

def pull(request):
    if request.method == 'POST':
        #fetch values from form
        play_form = PlayForm(request.POST)
        if play_form.is_valid():
            #assign rate from request and current balance from session
            rate = play_form.cleaned_data['rate']
            balance = request.session['balance']
            #check if it's enough points in balance
            if validateRate(request, balance, rate) == True:
                #create random board
                board = setRandom_board()
                #check results in board and update balance value
                new_balance = checkResult(request, balance, rate, board)
                request.session['balance'] = new_balance
                #create new PlayForm to display:
                play_form_dspl = PlayForm(initial={'balance': request.session['balance'], 'rate': rate})
                return render(request, 'slot_machine/index.html', {'board':board, 'play_form':play_form_dspl})
            else:
                return HttpResponseRedirect(reverse_lazy('slot_machine:play'))
        else:
            return HttpResponseRedirect(reverse_lazy('slot_machine:play'))

def reset(request):
    try:
        del request.session['balance']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse_lazy('slot_machine:play'))

def init_board():
    #create list board, which consist of three rows: upper, middle and bottom
    upper_row = [0, 0, 0]
    middle_row = [0, 0, 0]
    bottom_row = [0, 0, 0]
    board = [upper_row, middle_row, bottom_row]
    return board

def setRandom_board():
    board = init_board()
    #assign random values between 0 to 6, to each square
    for x in range(3):
        for y in range(3):
            board[x][y] = random.randint(0,6)
    return board

def checkResult(request, balance, rate, board):
    balance -= rate
    success = 0
    #check upper row:
    if len(set(board[0])) == 1:
        factor = getFactor(board[0][0])
        success += success + (rate * factor * 2)
        messages.success(request, 'Rate: %(rate)i points x %(factor)i (Factor) x 2 (Row) = %(success)i points'%{'rate':rate,'factor':factor,'success':success})

    #check middle row:
    if len(set(board[1])) == 1:
        factor = getFactor(board[1][0])
        success += success + (rate * factor * 3)
        messages.success(request, 'Rate: %(rate)i points x %(factor)i (Factor) x 3 (Row) = %(success)i points'%{'rate':rate,'factor':factor,'success':success})
    elif len(set(board[1])) == 2:
        messages.success(request, 'Bonus! Two Same Sign In Middle Row! +%(rate)i points'%{'rate':rate})
        success += success + rate

    #check bottom row:
    if len(set(board[2])) == 1:
        factor = getFactor(board[2][0])
        success += success + (rate * factor)
        messages.success(request, 'Rate: %(rate)i x %(factor)i points (Factor) = %(success)i points'%{'rate':rate,'factor':factor,'success':success})

    balance += success
    return balance

def validateRate(request, balance, rate):
    if balance >= rate:
        return True
    else:
        messages.error(request, 'You don\'t have enough points! Change rate.')
        return False

def getFactor(value):
    if value == 0:
        factor = 0
    elif value == 1:
        factor = 2
    elif value == 2:
        factor = 5
    elif value == 3:
        factor = 5
    elif value == 4:
        factor = 6
    elif value == 5:
        factor = 6
    elif value == 6:
        factor = 10
    return factor
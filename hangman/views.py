from string import ascii_uppercase as letters
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
import random
import re

from .models import Country

def play(request):
    #if it is new game, than variable chance don't exists yet. 
    if not request.session.get('game'):
        #create variables in session: chance, letters(from A to Z)
        request.session['game'] = 'on'
        request.session['chance'] = 0
        request.session['letters'] = list(letters)
        #get random country from Database
        country = getCountry()
        #mask word
        masked_word = maskWord(request, country)
        #save word and maksed_word in session
        request.session['word'] = country
        request.session['masked_word'] = masked_word
    return render(request, 'hangman/index.html')

def shot(request, letter):
    #fetch chances from session
    chance = request.session['chance']
    #no more chance or word is guessed, then game is over
    if chance == 11 or chance == 12:
        return HttpResponseRedirect(reverse_lazy('hangman:play'))
    else:
        #fetch word and actual letters from session
        letters = request.session['letters']
        word = request.session['word']
        #remove selected letter
        letters.remove(letter)
        #update letters in session
        request.session['letters'] = letters   
        
        #if selected letter isn't in word
        if not re.search(letter, word):
            chance += 1

        #mask left letters
        masked_word = maskWord(request, word)

        #check if word is guessed
        if not re.search('\*', masked_word):
            chance = 12
        
        #update variables is session
        request.session['chance'] = chance
        request.session['masked_word'] = masked_word
        return HttpResponseRedirect(reverse_lazy('hangman:play'))

def reset(request):
    try:
        del request.session['chance']
        del request.session['game']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse_lazy('hangman:play'))

def getCountry():
    countries_quantity = Country.objects.all().count()
    if countries_quantity == 0:
        return "no data"
    country_id = random.randint(1, countries_quantity)
    country = str(Country.objects.get(pk=country_id))
    country = country.upper()
    return country

def maskWord(request, word):
    letters = request.session['letters']
    letters_str = ''
    for letter in letters:
        letters_str += letter
    letters_str = '[' + letters_str + ']'
    word = re.sub(letters_str, '*', word)
    return word
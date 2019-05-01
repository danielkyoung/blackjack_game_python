# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:42:07 2019
Contains:
    Card
    Deck
    Player
for the blackjack game

@author: daniel
"""

import random

class Card:
    '''
    Object representing a single card. 
    Contains suit and rank and method to 
    create a graphical representation of the card
    '''
    def __init__(self, suit,rank):
        self.suit = suit
        self.rank = rank
    def graphic_card(self):
        if self.suit == 'spade':
            symbol = '♠'
        elif self.suit == 'clove':
            symbol = '♣'
        elif self.suit == 'heart':
            symbol = '♥'
        elif self.suit == 'diamond':
            symbol = '♦'
        if self.rank == '10':
            space = ''
        else:
            space = ' '
        number = self.rank
        card_picture_list = ['┌─────────┐',\
                             '│{}{}       │'.format(number,space),\
                             '│         │',\
                             '│         │',\
                             '│    {}    │'.format(symbol),\
                             '│         │',\
                             '│         │',\
                             '│       {}{}│'.format(space,number),\
                             '└─────────┘']

        return card_picture_list
    def get_value(self):
        if self.rank == 'K' or self.rank=='Q' or self.rank=='J':
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Deck:
    '''
    Object representing deck of cards. 
    '''
    suit_list = ['spade','clove','heart','diamond']
    rank_list = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    def __init__(self):
        self.card_list = []
        for x in range (0,4):
            for suit in Deck.suit_list:
                for rank in Deck.rank_list:
                    self.card_list.append(Card(suit,rank))
    def reset_cards(self):
        self.card_list = []
        for x in range (0,4):
            for suit in Deck.suit_list:
                for rank in Deck.rank_list:
                    self.card_list.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.card_list)
        
class Player:
    '''
    Object representing each player
    Contains hand,name,bank,bet,and insurancebet
    '''
    def __init__(self,name,money=0,bet=0):
        self.hands = [Hand()]
        self.name = name
        self.bank = money
        self.bet = bet
        self.insurancebet = 0
        self.insurance = False
        self.doubledown = False
        self.natural = False
    def reset(self):
        self.hands = [Hand()]
        self.bet = 0
        self.insurancebet = 0
        self.insurance - False
        self.doubledown = False
        self.natural = False
class Hand:
    def __init__(self):
        self.cards = []
        self.bust = False
        self.blackjack = False
    def hit(self,card):
        self.cards.append(card)
    def get_value(self):
        value = 0
        acecount = 0
        for card in self.cards:
            if card.rank == 'K' or card.rank == 'Q' or card.rank == 'J':
                value += 10
        for card in self.cards:
            try:
                value += int(card.rank)
            except:
                pass
        for card in self.cards:
            if card.rank == 'A':
                value += 1
                acecount += 1
        for x in range(acecount):
            if value <= 11:
                value += 10
        return value
    def has_ace(self):
        for card in self.cards:
            if card.rank == 'A':
                return True
        return False
    def can_doubledown(self):
        if self.get_value()==9 or self.get_value()==10 or self.get_value()==11:
            return True
        else:
            return False
    def can_split(self):
        if self.cards[0].get_value() == self.cards[1].get_value():
            return True
        else:
            return False
    def make_graphic_list(self):
        graphic_card_list = []
        for card in self.cards:
            graphic_card_list.append(card.graphic_card())
        return graphic_card_list
    def make_dealer_list(self):
        graphic_card_list = [self.cards[0].graphic_card(),[ '┌─────────┐',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '│░░░░░░░░░│',\
                                                                    '└─────────┘']]
    
        return graphic_card_list
    def clear_hand(self):
        self.cards = []

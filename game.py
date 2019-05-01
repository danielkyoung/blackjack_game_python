# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 07:27:10 2019

BLACJACK. Played with standard blackjack rules

@author: daniel
"""
print('\n'*10)
import items
deck = items.Deck()
players = []
dealer = items.Player('Dealer',0)
def run_game():
    global deck
    global players
    global dealer
    players = initialize_players()
    while True:
        if len(players) == 0:
            break
        for player in players:
            player.reset()
        dealer.reset()
        deck.reset_cards()
        deck.shuffle()
        for player in players:
            print('\n'*500)
            while True:
                entry = input(f'{player.name}, enter your bet (the minium bet is $10)\nYour current bankroll is {player.bank}\n')
                try:
                    player.bet = int(entry)
                except:
                    print('Please enter an integer amount')
                else:
                    if player.bet >= 1:
                        break
                    else:
                        print('The minium bet is $1')
        for player in players:
            player.hands[0].hit(deck.card_list.pop())
            player.hands[0].hit(deck.card_list.pop())
        dealer.reset()
        dealer.hands[0].hit(deck.card_list.pop())
        dealer.hands[0].hit(deck.card_list.pop())
        card_reveal()
        for player in players:
            if player.bank <= 0:
                players.remove(player)
            else:
                turn(player)
        dealer_turn()
        settlement()
        for player in players:
            entry = input('Player {}, press ENTER to continue playing or 0 to leave the table'.format(player.name))
            if entry == '0':
                players.remove(player)
def display_cards(card_list):
    line_list = ['','','','','','','','','']
    for x in range(0,9):
        for card in card_list:
            line_list[x] += card[x]
    for line in line_list:
        print(line)
def display_single_card(graphic_card):
    for line in graphic_card:
        print (line)
def initialize_players():
    print("Welcome to BLACKJACK.")
    while True:
        try:
            player_number = int(input('How many players will be joining the table?\n'))
        except:
            print('please enter a valid number of players')
        else:
            break
    print('The starting bankroll will be $1000')
    players = []
    for x in range(0,player_number):
        name = input('Player {}, what is your name\n'.format(x+1))
        players.append(items.Player(name,1000,0))
    return players
def card_reveal():
    global players
    global dealer
    for player in players:
        print("Player {}'s hand".format(player.name))
        display_cards(player.hands[0].make_graphic_list())
        if player.hands[0].get_value()==21:
            player.natural = True
    print("Dealer's hand")
    display_cards(dealer.hands[0].make_dealer_list())
    if dealer.hands[0].cards[0].get_value()==11:
        for player in players:
            entry = input('{}, Enter 1 for insurance or ENTER to continue\n'.format(player.name))
            if entry == '1':
                print('You made an insurance bet')
                player.insurancebet = int(player.bet*0.5)
                player.insurance = True
    if dealer.hands[0].get_value()==21:
        print('Dealer has natural')
        display_cards(dealer.hands[0].make_graphic_list())
        for player in players:
            if player.insurance:
                print("Player {} won {} from insurance".format(player.name, (player.insurancebet*2)))
                player.bank += int(player.insurancebet*2)
        dealer.natural = True
    else:
        for player in players:
            if player.insurance:
                print("Player {} lost {} from insurance".format(player.name, (player.insurancebet*2)))
                player.bank -= player.insurancebet
    input('Press enter to continue')
def turn(player):
    global deck
    global dealer
    print('\n'*500)
    print("Player {}'s turn".format(player.name))
    print('Your hand')
    display_cards(player.hands[0].make_graphic_list())
    print("Dealer's hand")
    if dealer.hands[0].get_value()==21:
        display_cards(dealer.hands[0].make_graphic_list())
    else:
        display_cards(dealer.hands[0].make_dealer_list())
    while True:
        if player.natural and not dealer.natural:
            print('{} BLACKJACK'.format(player.name))
            input('Press Enter to continue')
            break
        elif player.natural and dealer.natural:
            print('PUSH')
            input('Press Enter to continue')
            break
        elif dealer.natural and not player.natural:
            print('Dealer BLACKJACK')
            input('Press Enter to continue')
            break
        else:
            if player.bank >= player.bet*2:
                if player.hands[0].can_split() and player.hands[0].can_doubledown():
                    entry = input('Enter 1 for split, 2 for double down or ENTER to continue\n')
                    if entry == '1':
                        print('Your cards have been split')
                        player.hands.append(items.Hand())
                        player.hands[1].hit(player.hands[0].cards.pop())
                    elif entry == '2':
                        print('You doubled down')
                        player.bet = player.bet*2
                        player.doubledown = True
                elif player.hands[0].can_split():
                    entry = input('Enter 1 for split or ENTER to continue\n')
                    if entry == '1':
                        print('Your cards have been split')
                        player.hands.append(items.Hand())
                        player.hands[1].hit(player.hands[0].cards.pop())
                elif player.hands[0].can_doubledown():
                    entry = input('Enter 1 for doubledown or ENTER to continue\n')
                    if entry == '1':
                        print('You doubled down')
                        player.bet = player.bet*2
                        player.doubledown = True
            x = 0
            for hand in player.hands:
                x += 1
                print("{}'s hand {}".format(player.name, x))
                display_cards(hand.make_graphic_list())
                if player.doubledown:
                    card = deck.card_list.pop()
                    hand.hit(card)
                    print('You got')
                    display_single_card(card.graphic_card())
                    print('Your final hand is')
                    display_cards(hand.make_graphic_list())
                    print("Total is {}".format(hand.get_value()))
                    if hand.get_value()>21:
                        print('BUST')
                    break
                else:
                    while True:
                        entry = input('Press 1 to hit or 2 to stand\n')
                        if entry == '2':
                            print('Your final hand is')
                            display_cards(hand.make_graphic_list())
                            print('Total is {}'.format(hand.get_value()))
                            break
                        elif entry == '1':
                            card = deck.card_list.pop()
                            hand.hit(card)
                            print('You got')
                            display_single_card(card.graphic_card())
                            print('Your updated hand is')
                            display_cards(hand.make_graphic_list())
                            if hand.get_value() >21:
                                print('BUST')
                                print('You lost {}'.format(player.bet))
                                break
                            elif hand.get_value() == 21:
                                print('You got 21')
                                break
            input('Press ENTER to continue')
            break
def dealer_turn():
    print('\n'*500)
    player_remaining = False
    global players
    global dealer
    for player in players:
        for hand in player.hands:
            if hand.get_value() <= 21:
                player_remaining = True
    if player_remaining:
        print("Dealer's turn")
        print("Dealer's hand")
        display_cards(dealer.hands[0].make_graphic_list())
        while True:
            if dealer.natural:
                print('Dealer has natural blackjack')
                break
            elif dealer.hands[0].get_value()>21:
                print("Dealer busted")
                break
            elif dealer.hands[0].get_value()==21:
                print("Dealer got 21")
                break
            elif dealer.hands[0].get_value()>=17:
                print('Dealer stands at {}'.format(dealer.hands[0].get_value()))
                break
            else:
                print('Dealer hits')
                card = deck.card_list.pop()
                dealer.hands[0].hit(card)
                print('Dealer got')
                display_single_card(card.graphic_card())
                print("Dealer's updated hand")
                display_cards(dealer.hands[0].make_graphic_list())
    else:
        print("All players busted")
    input('Press Enter to continue')
def settlement():
    global players
    global dealer
    dealer_total = dealer.hands[0].get_value()
    for player in players:
        if player.natural and not dealer.natural:
            print("{} wins {} with natural blackjack".format(player.name,(player.bet*1.5)))
            player.bank += int(player.bet*1.5)
        elif player.natural and dealer.natural:
            pass
            print('{} push, no win/loss'.format(player.name))
        elif dealer.natural and not player.natural:
            print("{} loses {} with dealer's natural blackjack".format(player.name,player.bet))
            player.bank -= player.bet
        else:
            for hand in player.hands:
                print("Player {}'s {} against Dealer's {}".format(player.name, hand.get_value(),dealer_total))
                if hand.get_value() >21:
                    print("{} loses {} by bust".format(player.name,player.bet))
                    player.bank -= player.bet
                elif dealer_total >21:
                    print("{} wins {} by dealer's bust".format(player.name,player.bet))
                    player.bank += player.bet
                elif hand.get_value() > dealer_total:
                    print("{} wins {}".format(player.name,player.bet))
                    player.bank += player.bet
                elif hand.get_value() < dealer_total:
                    print("{} loses {}".format(player.name,player.bet))
                    player.bank -= player.bet
                else:
                    print("{} push, no win/loss".format(player.name))
if __name__ == '__main__':
    run_game()
        




        

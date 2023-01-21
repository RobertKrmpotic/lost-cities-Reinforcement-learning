import pandas as pd
from datetime import datetime
from card import Card
from deck import Deck
from player import Player
import random


class GameManager():
    def __init__(self) -> None:
        self.colours = ["red","blue", "yellow", "green", "white"]
        self.player1= Player(1)
        self.player2= Player(2)
        self.players = {1:self.player1, 2:self.player2}
        self.player_turn = 1
        self.deck = self.generate_deck()
        self.discard_pile = self.generate_discard()
        self.score_dict = {}

    def next_player(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else: 
            self.player_turn=1

    def generate_deck(self):
        numbers = [0,0,0,2,3,4,5,6,7,8,9,10]
        cards = []
        for colour in self.colours:
            for number in numbers:
                cards.append(Card(number, colour))
        deck = Deck(cards)
        return deck

    def generate_discard(self):
        discard_dict = {}
        for colour in self.colours:
            discard_dict[colour] = []
        return discard_dict

    def check_card_to_expedition(self,player_n:int, card_n:int):
        ''' check if card is too small to be played to the expedition'''
        player = self.players[player_n]
        card = player.hand[card_n]
        colour = card.colour

        if len(player.expedition[colour]) == 0:
            return True

        if player.expedition[colour][-1].number <= card.number:
            return True

        else:
            return False
 
    def is_move_legal(self,player:int, card:int, to_expedition:bool, draw_from:int):
        ''' Check if player is allowed to do this move'''
    	#is allowed to play that expedition
        if to_expedition:
            allowed_to_expedition =  self.check_card_to_expedition(player, card)
            if not allowed_to_expedition:
                return False
        
        #is allowed to drawi from pile
        if draw_from > -1:
            colour = self.colours[draw_from]
            if len (self.discard_pile[colour]) ==0:
                return False
        
        return True

    def take_random_action(self,player:int):
        ''' generate_random action'''
        card = random.randint(0,7)
        to_expedition = random.choice([True,False])
        draw_from = random.randint(-1,4)

        legal = self.is_move_legal(player,card, to_expedition, draw_from)
        if legal:
            self.take_action(player,card, to_expedition, draw_from)
            self.next_player()
        else: 
            self.take_random_action(player)

    def print_commentary(self, player_n:int, card:Card, to_expedition:bool, draw_from:int):
        if to_expedition:
            destination = "expedition"
        else:
            destination = "disard pile"

        if draw_from == -1:
            draw_location = "deck"
        else:
            draw_location = self.colours[draw_from]

        print( f"Player {player_n} plays {card.colour} {card.number} to: {destination}, and draws from: {draw_location}")

    def take_action(self, player_n:int, card_n:int, to_expedition:bool, draw_from:int ):
        ''' Player takes action, choosing card from hand (number 0 to 7), 
        chooses if they play it to expedition or to discard pile. Also chooses if they draw from  '''
        
        player = self.players[player_n]
        card = player.hand.pop(card_n)
        colour = card.colour
        #self.print_commentary(player_n, card, to_expedition, draw_from)
        
        if to_expedition:
            player.expedition[colour].append(card)
        else:
            self.discard_pile[colour].append(card)

        if draw_from == -1:
            self.draw_card_from_deck(player)
        else:
            draw_colour = self.colours[draw_from]
            card = self.discard_pile[draw_colour].pop() #takes last item
            player.hand.append(card)

    def initiate_expeditions(self):
        #empty dicts for player expeditions
        for n,player in self.players.items():
            expedition_dict = {}
            for colour in self.colours:
                expedition_dict[colour] = []
            player.expedition= expedition_dict
    
    def draw_card_from_deck(self,player:Player):
        ''' draw a card from the deck and deal it to the player'''
        card = self.deck.list.pop()
        player.hand.append(card)

    def deal_starting_cards(self):
        ''' deal 8 cards to each player'''
        for n,player in self.players.items():
            for _ in range(0,8):
                self.draw_card_from_deck(player)

    def start_game(self):
        self.deck.shuffle_deck()
        self.initiate_expeditions()
        self.deal_starting_cards()

    def play_game(self):
        while len(self.deck.list) > 0:
            self.take_random_action(self.player_turn)
        self.score()
        #self.write_score()
        #print("end")
    
    def reset_game(self):
        pass

    def score(self):
        score_dict = {1:0, 2:0}
        for player_n, player in self.players.items():
            for colour,colour_list in player.expedition.items():
                if len(colour_list) == 0:
                    pass
                else:
                    n_wagers = 0
                    total = 0
                    for card in colour_list:
                        if card.number == 0:
                            n_wagers += 1
                        else:
                            total += card.number
                    score = (total - 20) * (n_wagers +1)
            
                    if len(colour_list) >= 8:
                        score += 20

                    #print(f"player {player_n}: colour{colour}: {score} len_list = {len(colour_list) }")
                    score_dict[player_n] += score
        
        self.score_dict = score_dict


    def write_score(self):
        df = pd.read_csv("data/game_history.csv", index_col=0)
        # Insert Dict to the dataframe using DataFrame.append()
        new_row = {'Datetime':f"{datetime.now()}", 
        'Player1 score': self.score_dict[1], 
        'Player2 score':self.score_dict[2], 
        'Player 1 model':"random moves", 
        'Player 2 model':"random moves",  }
        df = df.append(new_row, ignore_index=True)
        df.to_csv("data/game_history.csv")

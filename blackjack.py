from baseComponents import Deck, Hand, Player


class BJHand(Hand):
    def __init__(self):
        super().__init__()
        self.reset()
        self.busted = False

    '''
    * @param c: The Card being added to the hand
    * First, tack the card on the hand list
    * Then, update all current hand values
    * Also, if the card is an ace,
    * Add a new value where the ace is treated as an 11
    '''
    def add_card(self, c):
        self.hand.append(c)
        size = len(self.hand_value)
        for pos in range(size):
            if c.value == 1:  # deal with Aces counting as 11 first
                self.hand_value.append(self.hand_value[pos] + 11)
            if c.value <= 10:
                self.hand_value[pos] += c.value
            else:
                self.hand_value[pos] += 10
        self.num_of_cards += 1

    '''
    * Rules:
    * Can only split if hand size is 2
    * Can only split if both cards' values are the same
    * @return Whether the hand can be split
    '''
    def can_split(self):
        """Determine whether to allow a hand split on the current hand"""
        if len(self.hand) != 2:
            return False
        return self.hand[0].compare_to(self.hand[1]) == 0

    def stand(self):
        """Set the player's best score,
            and pull him out of the dealing process
        """
        best = 0
        for v in self.hand_value:
            if v >= best:
                best = v
        del(v)
        self.hand_value = best

    def reset(self):
        """Return a hand to its default state"""
        self.hand = []
        self.hand_value = [0]
        self.num_of_cards = 0
        self.still_in = True

    def are_busted(self):
        """Iterate through each possible hand value in the player's hand
            If a particular value is greater than 21,
            remove it from the list
        """
        nVal = []
        for val in self.hand_value:
            if val <= 21:
                nVal.append(val)
        del(val)
        self.hand_value = nVal
        if len(self.hand_value) <= 0:
            return True
        return False

    def have_blackjack(self):
        if len(self.hand) == 2 and (
               len(self.hand_value)
               == 2 and self.hand_value[1] == 21):
            self.hand_value = -1
            return True
        return False

    '''
    * @param alt_hand: The other player's hand we are comparing 'self' to
    * @return 1: If self's value > alt_hand's value
    * @return 0: If self's value == alt_hand's value
    * @return -1: If self's value < alt_hand's value
    '''
    def compare_to(self, alt_hand):
        """Compare this hand to another"""
        if self.hand_value > alt_hand.hand_value or (self.hand_value
           == -1 and alt_hand.hand_value != -1):
            return 1
        elif self.hand_value == alt_hand.hand_value:
            return 0
        else:
            return -1


class BJPlayer(Player):

    def __init__(self, name):
        self.hand = [BJHand()]
        super().__init__(name, 100)

    '''
    * @param: The card to be added
    '''
    def deal_card(self, c, hand_number):
        """Player is dealt a card and adds it to his hand"""
        self.hand[hand_number].add_card(c)

    '''
    * @param card1: The card to be added to the first hand
    * @param card2: The card to be added to the second hand
    '''
    def split_hand(self, card1, card2, hand_number):
        """Turn one hand into multiple hands"""
        first_card = self.hand[hand_number].hand[0]
        second_card = self.hand[hand_number].hand[1]
        self.hand[hand_number] = BJHand()
        self.deal_card(first_card, hand_number)
        self.deal_card(card1, hand_number)
        self.hand.append(BJHand())
        self.deal_card(second_card, len(self.hand) - 1)
        self.deal_card(card2, len(self.hand) - 1)

    def reset(self):
        """Reset the player's hand in case they have multiple from splits."""
        self.hand = [BJHand()]


class Dealer:
    def __init__(self):
        self.hand = BJHand()

    def decide_to_hit(self):
        """
        * If a hand has a value that leaves it between 17 and 21
        * The dealer must stay
        * Otherwise, the dealer must hit
        """
        for val in self.hand.hand_value:
            if val >= 17 and val <= 21:
                return False
        del(val)
        return True


player_number = -1
player_list = []
dealer = Dealer()


def start_game():
    """Determine how many players are in the game"""
    player_number = -1
    while player_number <= 0:
        player_number = (int)(input('How many players would like '
                                    + 'a chair at the table?\nMax 5: '))
    for i in range(player_number):
        pName = input("Player {}, choose a name: ".format(i + 1))
        print("{name} is your name".format(name=pName))
        player_list.append(BJPlayer(pName))
    del(i)


def accept_bets():
    """Take bets from all players"""
    for player in player_list:
        valid = False
        while not valid:
            print("{n}: You have ${m}.".format(n=player.name, m=player.money))
            amount = int(input("Place your bet on this hand: "))
            valid = player.place_bet(amount)


def deal_hands(deck):
    """
    * Starting with the players then moving to the dealer,
    * Deal each person a card from the deck
    * Then repeat the process
    """
    for round in range(2):
        for player in player_list:
            print("Dealing to " + player.name)
            player.deal_card(deck.deal_card(), 0)
        dealer.hand.add_card(deck.deal_card())
    dealer.hand.hand[1].flip()
    del(round, player)


def player_loop(player, deck):
    """Allow the player to place bets until they bust or stop"""
    current_hand = 0
    while current_hand < len(player.hand):
        to_next_hand = False
        while player.hand[current_hand].still_in and not to_next_hand:
            if player.hand[current_hand].have_blackjack():
                print("Blackjack! You win!")
                break
            is_valid = False
            print("Dealer is showing ", dealer.hand.hand[0])
            while not is_valid:
                print("{n}: Your Hand is {h}".format(
                    n=player.name, h=player.hand[current_hand]))
                decision = input("1. ('h')it "
                                 + "2. ('s')tand? "
                                 + ("3. spli('t') "
                                    if player.hand[current_hand].can_split()
                                    else ""))
                if decision == "h":
                    player.deal_card(deck.deal_card(), current_hand)
                    if player.hand[current_hand].are_busted():
                        player.hand[current_hand].still_in = False
                        print("You busted with "
                              + repr(player.hand[current_hand]))
                        to_next_hand = True
                    is_valid = True
                elif decision == "s":
                    player.hand[current_hand].stand()
                    to_next_hand = True
                    is_valid = True
                elif decision == "t":
                    if not player.hand[current_hand].can_split():
                        print("This is not a valid move. Try again.")
                    else:
                        player.split_hand(deck.deal_card(),
                                          deck.deal_card(), current_hand)
                        player.place_bet(player.bet)
                else:
                    print("This is not a valid move. Try again.")
        current_hand += 1


def dealer_loop(deck):
    """The dealer's sequence of plays.

    Rules:
        1) The dealer must hit on all hands less than 17
        2) The dealer must stand on all hands at or above 17 (no soft 17s)
    @return The status the dealer leaves with...
        -1) The dealer has blackjack
        0) The dealer busts
        *) The dealer's hand value
    """
    print("Dealer is showing " + repr(dealer.hand.hand[0]))
    dealer.hand.hand[1].flip()
    print("Dealer reveals his face-down card: ",
          dealer.hand.hand[1])
    if len(dealer.hand.hand) == 2:
        if len(dealer.hand.hand_value) == 2\
           and (dealer.hand.hand_value[1] == 21):
            print("Dealer has blackjack!")
            return -1
    playing = True
    while playing:
        playing = dealer.decide_to_hit()
        if playing:
            dealer.hand.add_card(deck.deal_card())
            print("Dealer now has ", dealer.hand)
            if dealer.hand.are_busted():
                print("Dealer busted with ", dealer.hand, "!")
                return 0
    dealer.hand.stand()
    print("Dealer stands at " + str(dealer.hand.hand_value))
    return dealer.hand.hand_value


def check_winner(player, hand_number, dealer, dealer_status):
    """Determine who wins between a player's hand and the dealer"""
    if dealer_status == 0:
        player.receive_winnings(player.bet * 2)
        print(player.name + " wins!")
        return 1
    elif dealer_status == -1:
        # Dealer hit blackjack, all players lose except those with BJ
        if player.hand[hand_number].hand_value == -1:
            player.receive_winnings(player.bet)
            print("{n}: You pushed and have received your bet back.".format(
                  n=player.name))
            return 0
        else:
            print("Sorry, {n}: dealer's blackjack means you lose.".format(
                  n=player.name))
            return -1
    else:
        # Calculate who wins between dealers and players that are still in
        winner = player.hand[hand_number].compare_to(dealer.hand)
        if winner == 1:
            player.receive_winnings(player.bet * 2)
            print("Congrats, {n}, you win ${m}".format(
                  n=player.name, m=player.bet))
            return 1
        elif winner == 0:
            player.receive_winnings(player.bet)
            print("{n}: You pushed and have received your bet back.".format(
                  n=player.name))
            return 0
        else:
            print("Dealer beats {n}\'s {pVal} with {dVal}. ".format(
                  n=player.name, pVal=player.hand[hand_number].hand_value,
                  dVal=dealer.hand.hand_value) + "Better luck next time.")
            return -1


def clean_up_players():
    """
    * Figure out who still wants to play
    * If a player is out either by choice or by lack of funds
    * Remove them from the list of available players
    """
    global player_list
    players_to_remove = []
    for p in player_list:
        print(p.name + " has $" + str(p.money))
        if p.money <= 0:
            print("Sorry, " + p.name + ", you are out of money. Goodbye")
            players_to_remove.append(p)
        else:
            p.reset()
            print(p.name + "\'s hand has been reset")
    for out in players_to_remove:
        player_list.remove(out)
    dealer.hand.reset()
    if len(player_list) == 0:
        print("It seems all players are out. Goodbye")
        return False
    return True


def go():
    """The main runner for the program"""
    deck = Deck()
    deck.shuffle()
    start_game()
    are_playing = True
    while are_playing:
        accept_bets()
        deal_hands(deck)
        for player in player_list:
            player_loop(player, deck)
        dealer_status = dealer_loop(deck)
        for player in player_list:
            for current_hand in range(len(player.hand)):
                if player.hand[current_hand].still_in:
                    check_winner(player, current_hand, dealer, dealer_status)
        answer = input("Continue playing? ")
        if not(answer == "yes" or answer == "y"):
            are_playing = False
        else:
            are_playing = clean_up_players()
            deck.fill_deck()
            deck.shuffle()

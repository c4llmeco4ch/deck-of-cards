from baseComponents import Card, Deck, Hand, Player


class BJHand:
    def __init__(self):
        self.reset()
        self.busted = False

    def __repr__(self):
        """Convert this hand to a readable string"""
        currentHand = "| "
        for c in self.hand:
            currentHand += repr(c) + ", "
        currentHand = currentHand[:len(currentHand) - 2] + "|"
        return currentHand

    '''
    * @param c: The Card being added to the hand
    * First, tack the card on the hand list
    * Then, update all current hand values
    * Also, if the card is an ace,
    * Add a new value where the ace is treated as an 11
    '''
    def addCard(self, c):
        self.hand.append(c)
        size = len(self.handValue)
        for pos in range(size):
            if c.value == 1:  # deal with Aces counting as 11 first
                self.handValue.append(self.handValue[pos] + 11)
            if c.value <= 10:
                self.handValue[pos] += c.value
            else:
                self.handValue[pos] += 10
        self.numOfCards += 1

    '''
    * Rules:
    * Can only split if hand size is 2
    * Can only split if both cards' values are the same
    * @return Whether the hand can be split
    '''
    def canSplit(self):
        """Determine whether to allow a hand split on the current hand"""
        if len(self.hand) != 2:
            return False
        return self.hand[0].compareTo(self.hand[1]) == 0

    def stand(self):
        """Set the player's best score,
            and pull him out of the dealing process"""
        best = 0
        for v in self.handValue:
            if v >= best:
                best = v
        del(v)
        self.handValue = best

    def reset(self):
        """Return a hand to its default state"""
        self.hand = []
        self.handValue = [0]
        self.numOfCards = 0
        self.stillIn = True

    def areBusted(self):
        """Iterate through each possible hand value in the player's hand
            If a particular value is greater than 21,
            remove it from the list"""
        nVal = []
        for val in self.handValue:
            if val <= 21:
                nVal.append(val)
        del(val)
        self.handValue = nVal
        if len(self.handValue) <= 0:
            return True
        return False

    '''
    * @param altHand: The other player's hand we are comparing 'self' to
    * @return 1: If self's value > altHand's value
    * @return 0: If self's value == altHand's value
    * @return -1: If self's value < altHand's value
    '''
    def compareTo(self, altHand):
        """Compare this hand to another"""
        if self.handValue > altHand.handValue or (self.handValue
           == -1 and altHand.handValue != -1):
            return 1
        elif self.handValue == altHand.handValue:
            return 0
        else:
            return -1


class BJPlayer:

    def __init__(self, name):
        self.money = 100
        self.hand = [BJHand()]
        self.name = name
        self.bet = 0

    '''
    * @param m: The amount of money a player is betting on his hand
    * If the player cannot pay 'm' dollars, return false to show this inability
    * Otherwise, subtract that amount of money from the player's account
    '''
    def placeBet(self, m):
        """Place an 'm'-sized bet for this player"""
        if m > self.money:
            print("You do not have that much money. Try again")
            return False
        elif m <= 0:
            print("Please place a bet greater than $0.")
            return False
        else:
            self.money -= m
            self.bet = m  # Might need to make this '+='.
            return True   # If so, reset bets after each hand

    '''
    * @param m: The amount of money a player wins from a particular hand
    '''
    def receiveWinnings(self, m):
        """This player adds 'm' money to his account"""
        self.money += m

    '''
    * @param: The card to be added
    '''
    def dealCard(self, c, handNumber):
        """Player is dealt a card and adds it to his hand"""
        self.hand[handNumber].addCard(c)

    '''
    * @param card1: The card to be added to the first hand
    * @param card2: The card to be added to the second hand
    '''
    def splitHand(self, card1, card2, handNumber):
        """Turn one hand into multiple hands"""
        firstCard = self.hand[handNumber].hand[0]
        secondCard = self.hand[handNumber].hand[1]
        self.hand[handNumber] = BJHand()
        self.dealCard(firstCard, handNumber)
        self.dealCard(card1, handNumber)
        self.hand.append(BJHand())
        self.dealCard(secondCard, len(self.hand) - 1)
        self.dealCard(card2, len(self.hand) - 1)

    def reset(self):
        """Reset the player's hand in case they have multiple from splits."""
        self.hand = [BJHand()]


class Dealer:
    def __init__(self):
        self.hand = BJHand()

    def decideToHit(self):
        """
        * If a hand has a value that leaves it between 17 and 21
        * The dealer must stay
        * Otherwise, the dealer must hit
        """
        for val in self.hand.handValue:
            if val >= 17 and val <= 21:
                return False
        del(val)
        return True


playerNumber = -1
playerList = []
dealer = Dealer()


def startGame():
    """Determine how many players are in the game"""
    playerNumber = -1
    while playerNumber <= 0:
        playerNumber = (int)(input("How many players would like "
                                   + "a chair at the table?\nMax 5: "))
    for i in range(playerNumber):
        pName = input("Player {}, choose a name: ".format(i + 1))
        print("{name} is your name".format(name=pName))
        playerList.append(BJPlayer(pName))
    del(i)


def acceptBets():
    """Take bets from all players"""
    for player in playerList:
        valid = False
        while not valid:
            print("{n}: You have ${m}.".format(n=player.name, m=player.money))
            amount = int(input("Place your bet on this hand: "))
            valid = player.placeBet(amount)


def dealHands(deck):
    """
    * Starting with the players then moving to the dealer,
    * Deal each person a card from the deck
    * Then repeat the process
    """
    for round in range(2):
        for player in playerList:
            print("Dealing to " + player.name)
            player.dealCard(deck.dealCard(), 0)
        dealer.hand.addCard(deck.dealCard())
    dealer.hand.hand[1].flip()
    del(round, player)


def playerLoop(player, deck):
    """Allow the player to place bets until they bust or stop"""
    currentHand = 0
    while currentHand < len(player.hand):
        toNextHand = False
        while player.hand[currentHand].stillIn and not toNextHand:
            if len(player.hand[currentHand].hand) == 2 and (
               len(player.hand[currentHand].handValue)
               == 2 and player.hand[currentHand].handValue[1] == 21):
                print("Blackjack! You win!")
                player.hand[currentHand].handValue = -1
                break
            isValid = False
            print("Dealer is showing ", dealer.hand.hand[0])
            while not isValid:
                print("{n}: Your Hand is {h}".format(
                    n=player.name, h=player.hand[currentHand]))
                decision = input("1. (\'h\')it "
                                 + "2. (\'s\')tand? "
                                 + ("3. spli(\'t\') "
                                    if player.hand[currentHand].canSplit()
                                    else ""))
                if decision == "h":
                    player.dealCard(deck.dealCard(), currentHand)
                    if player.hand[currentHand].areBusted():
                        player.hand[currentHand].stillIn = False
                        print("You busted with "
                              + repr(player.hand[currentHand]))
                        toNextHand = True
                    isValid = True
                elif decision == "s":
                    player.hand[currentHand].stand()
                    toNextHand = True
                    isValid = True
                elif decision == "t":
                    if not player.hand[currentHand].canSplit():
                        print("This is not a valid move. Try again.")
                    else:
                        player.splitHand(deck.dealCard(),
                                         deck.dealCard(), currentHand)
                        player.placeBet(player.bet)
                else:
                    print("This is not a valid move. Try again.")
        currentHand += 1


def dealerLoop(deck):
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
        if len(dealer.hand.handValue) == 2 and dealer.hand.handValue[1] == 21:
            print("Dealer has blackjack!")
            return -1
    playing = True
    while playing:
        playing = dealer.decideToHit()
        if playing:
            dealer.hand.addCard(deck.dealCard())
            print("Dealer now has ", dealer.hand)
            if dealer.hand.areBusted():
                print("Dealer busted with ", dealer.hand, "!")
                return 0
    dealer.hand.stand()
    print("Dealer stands at " + str(dealer.hand.handValue))
    return dealer.hand.handValue


def checkWinner(player, handNumber, dealer, dealerStatus):
    """Determine who wins between a player's hand and the dealer"""
    if dealerStatus == 0:
        player.receiveWinnings(player.bet * 2)
        print(player.name + " wins!")
        return 1
    elif dealerStatus == -1:
        # Dealer hit blackjack, all players lose except those with BJ
        if player.hand[handNumber].handValue == -1:
            player.receiveWinnings(player.bet)
            print("{n}: You pushed and have received your bet back.".format(
                  n=player.name))
            return 0
        else:
            print("Sorry, {n}: dealer's blackjack means you lose.".format(
                  n=player.name))
            return -1
    else:
        # Calculate who wins between dealers and players that are still in
        winner = player.hand[handNumber].compareTo(dealer.hand)
        if winner == 1:
            player.receiveWinnings(player.bet * 2)
            print("Congrats, {n}, you win ${m}".format(
                  n=player.name, m=player.bet))
            return 1
        elif winner == 0:
            player.receiveWinnings(player.bet)
            print("{n}: You pushed and have received your bet back.".format(
                  n=player.name))
            return 0
        else:
            print("Dealer beats {n}\'s {pVal} with {dVal}. ".format(
                  n=player.name, pVal=player.hand[handNumber].handValue,
                  dVal=dealer.hand.handValue) + "Better luck next time.")
            return -1


def cleanUpPlayers():
    """
    * Figure out who still wants to play
    * If a player is out either by choice or by lack of funds
    * Remove them from the list of available players
    """
    global playerList
    playersToRemove = []
    for p in playerList:
        print(p.name + " has $" + str(p.money))
        if p.money <= 0:
            print("Sorry, " + p.name + ", you are out of money. Goodbye")
            playersToRemove.append(p)
        else:
            p.reset()
            print(p.name + "\'s hand has been reset")
    for out in playersToRemove:
        playerList.remove(out)
    dealer.hand.reset()
    if len(playerList) == 0:
        print("It seems all players are out. Goodbye")
        return False
    return True


def go():
    """The main runner for the program"""
    deck = Deck()
    deck.shuffle()
    startGame()
    arePlaying = True
    while arePlaying:
        acceptBets()
        dealHands(deck)
        for player in playerList:
            playerLoop(player, deck)
        dealerStatus = dealerLoop(deck)
        for player in playerList:
            for currentHand in range(len(player.hand)):
                if player.hand[currentHand].stillIn:
                    checkWinner(player, currentHand, dealer, dealerStatus)
        answer = input("Continue playing? ")
        if not(answer == "yes" or answer == "y"):
            arePlaying = False
        else:
            arePlaying = cleanUpPlayers()
            deck.fillDeck()
            deck.shuffle()

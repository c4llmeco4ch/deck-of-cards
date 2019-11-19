class Player:

    def __init__(self, money):
        self.money = money
        self.bet = 0

    def placeBet(self, amount):
        """Place an 'amount'-sized bet for this player"""
        if amount > self.money:
            print("You do not have that much money. Try again")
            return False
        elif amount <= 0:
            print("Please place a bet greater than $0.")
            return False
        else:
            self.money -= amount
            self.bet = amount  # Might need to make this '+='.
            return True   # If so, reset bets after each hand

    '''
    * @param m: The amount of money a player wins from a particular hand
    '''
    def receiveWinnings(self, amount):
        """This player adds 'amount' money to his account"""
        self.money += amount
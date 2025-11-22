#!/usr/bin/env python3

class SincereAscendingStrategy:
    """
    Sincere (truthful) bidding strategy for ascending (English) auctions.

    - The bidder stays active as long as the current price is less than or equal to
      their private value and within their remaining budget.
    - This reflects the 'sincere bidding' rule: stay in until price > value.
    """

    def __init__(self, num_strategies):
        self.num_strategies = num_strategies
        self.remaining_money = 0
        self.num_auctions = 0
        self.value = 0

    def name(self):
        return "Sincere Ascending Strategy"

    def author(self):
        return "Taofeek Bello"

    # Called before the first auction
    def set_num_auctions(self, num_auctions):
        self.num_auctions = num_auctions

    # Initial money setup
    def set_money(self, money):
        self.remaining_money = money

    # Called after winning an auction to deduct payment
    def won(self, price):
        self.remaining_money -= price

    # Called before every auction to set the bidder's private value
    def set_value(self, value):
        self.value = value

    # Sincere bidding rule for ascending auctions
    def interested(self, price, active_strats):
        """
        Stay in the auction while:
        - The current price is less than or equal to our true value
        - The price to be paid is still affordable within our remaining money
        """
        return price <= self.value and price <= self.remaining_money


class TruthfulDescendingStrategy:
    """
    Truthful (sincere) bidding strategy for descending (Dutch) auctions.

    - The bidder waits while the price is above their private value.
    - As soon as the price drops to their true value (or below) and they can afford it,
      they accept the item immediately.
    """

    def __init__(self, num_strategies):
        self.num_strategies = num_strategies
        self.remaining_money = 0
        self.num_auctions = 0
        self.value = 0

    def name(self):
        return "Truthful Descending Strategy"

    def author(self):
        return "Taofeek Bello"

    # Called before the first auction
    def set_num_auctions(self, num_auctions):
        self.num_auctions = num_auctions

    # Initial money setup
    def set_money(self, money):
        self.remaining_money = money

    # Called after winning an auction to deduct payment
    def won(self, price):
        self.remaining_money -= price

    # Called before every auction to set the bidder's private value
    def set_value(self, value):
        self.value = value

    # Truthful bidding rule for descending auctions
    def interested(self, price, active_strats):
        """
        Accept the auction as soon as:
        - The current price is less than or equal to our true private value
        - We have enough remaining money to pay
        """
        return price <= self.value and price <= self.remaining_money


# Factory functions for simulator compatibility
def strategy_ascending(num_strategies):
    """Return a sincere bidding strategy for ascending auctions."""
    return SincereAscendingStrategy(num_strategies)


def strategy_descending(num_strategies):
    """Return a truthful bidding strategy for descending (Dutch) auctions."""
    return TruthfulDescendingStrategy(num_strategies)

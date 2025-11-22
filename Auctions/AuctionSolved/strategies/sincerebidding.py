#!/usr/bin/env python3

class SincereAscendingStrategy:
    """
    Sincere bidding strategy for ascending auctions.

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
        - We can still afford to pay that price
        """
        return price <= self.value and price <= self.remaining_money


# Factory functions for simulator compatibility
def strategy_ascending(num_strategies):
    """Return a sincere bidding strategy for ascending auctions."""
    return SincereAscendingStrategy(num_strategies)


def strategy_descending(num_strategies):
    # Return a dummy passive bidder so the simulator runs without errors
    class PassiveStrategy:
        def name(self): return "Passive Descending Strategy"
        def author(self): return "Taofeek Bello"
        def set_num_auctions(self, n): pass
        def set_money(self, m): pass
        def set_value(self, v): pass
        def won(self, p): pass
        def interested(self, price, active_strats): return False
    return PassiveStrategy()


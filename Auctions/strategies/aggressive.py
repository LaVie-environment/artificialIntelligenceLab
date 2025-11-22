class AggressiveCombinedStrategy:

    def __init__(self, num_strategies, auction_type="ascending"):
        self.num_strategies = num_strategies
        self.remaining_money = 0
        self.num_auctions = 0
        self.auction_type = auction_type  # Either "ascending" or "descending"

    # name of the strategy - make sure it is unique
    def name(self):
        return f"Aggressive {self.auction_type.capitalize()} Strategy"

    # name of the author of the strategy
    def author(self):
        return "John Doe"

    # number of auctions that will be simulated - called before the first auction
    def set_num_auctions(self, num_auctions):
        self.num_auctions = num_auctions

    # amount of money available for all auctions - called before the first auction
    def set_money(self, money):
        self.remaining_money = money

    # called after winning an auction with the price that was paid for the object
    def won(self, price):
        self.remaining_money -= price

    # value of the object for this agent - called before every auction
    def set_value(self, value): 
        self.value = value

    # shows interest in the object for the current price, called in each iteration of each auction
    def interested(self, price, active_strats):
        if self.auction_type == "ascending":
            # Ascending auction: allow bidding up to 20% above value
            aggressive_value = self.value * 1.2
            return price <= aggressive_value and price <= self.remaining_money
        elif self.auction_type == "descending":
            # Descending auction: bid if price is at or below 110% of value
            aggressive_threshold = self.value * 1.1
            return price <= aggressive_threshold and price <= self.remaining_money
        else:
            raise ValueError("Invalid auction type. Must be 'ascending' or 'descending'.")

# Factory functions for each type of auction strategy
def strategy_ascending(num_strategies):
    return AggressiveCombinedStrategy(num_strategies, auction_type="ascending")

def strategy_descending(num_strategies):
    return AggressiveCombinedStrategy(num_strategies, auction_type="descending")

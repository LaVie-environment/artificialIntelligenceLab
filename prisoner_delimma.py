#!/usr/bin/env python3

import random

class TitForTatWithForgiveness:

    @staticmethod
    def author_name():
        return "xbello1"

    @staticmethod
    def strategy_name():
        return "Tit-for-Tat with Forgiveness"

    def __init__(self, forgiveness_rate: float = 0.1):
        """Initialize with a forgiveness rate (default 10%)."""
        self.forgiveness_rate = forgiveness_rate
        self.last_opponent_move = 'C'  # start by assuming cooperation

    def reset(self):
        """Reset strategy state before a new match."""
        self.last_opponent_move = 'C'

    def last_move(self, my_move, other_move):
        """Record the opponent's last move."""
        self.last_opponent_move = other_move

    def play(self):
        """Decide the next move based on Tit-for-Tat with forgiveness."""
        if self.last_opponent_move == 'D':
            # Normally defect back, but sometimes forgive
            if random.random() < self.forgiveness_rate:
                return 'C'
            return 'D'
        return 'C'  # if opponent cooperated last, cooperate

def create_strategy():
    return TitForTatWithForgiveness()

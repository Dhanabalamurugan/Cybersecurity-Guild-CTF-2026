import random

from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa.ellipticcurve import CurveFp, Point


class Casino:
    N = 0xDB02EB1DDCDB0798F63CA143C24EE00240F4430E724843BAC31E4A764BA05DF3
    pX = 0x35495D877123DB4181BA781D843E07194FE8B707FB0C70E095636A54F68398BE
    pY = 0xA11AF18E9EDC908ABE6C97D1C6964C9147855889F44F749902BD7069206899C6
    win = bytes_to_long(b"You've been pwned")

    def __init__(self):
        secret = random.randint(1, 2**99)
        self.curve = CurveFp(self.N, 1, 4)
        self.point = Point(self.curve, self.pX, self.pY) * secret
        self.casino_edge_odds = [1.9, 5.8, [1.8, 35]]

    def flip_coin(self, guess, bet):
        result = random.choice(["heads", "tails"])
        if guess == result:
            return True, self.casino_edge_odds[0] * bet
        return False, 0

    def roll_dice(self, guess, bet):
        result = random.randint(1, 6)
        if guess == result:
            return True, self.casino_edge_odds[1] * bet
        return False, 0

    def play_roulette(self, bet_type, guess, bet):
        if bet_type == "color":
            result = random.choice(["red", "black"] * bet)
            if guess == result:
                return True, self.casino_edge_odds[2][0] * bet
        elif bet_type == "number":
            result = random.randint(0, 36)
            if guess == result:
                return True, self.casino_edge_odds[2][1] * bet
        return False, 0

    def sign_amount(self, amount: int):
        pt = bytes_to_long(f"money {amount}".encode())
        return long_to_bytes((self.point * pt).x()).hex()

    def verify_amount(self, amount: int, given):
        pt = bytes_to_long(f"money {amount}".encode())
        if long_to_bytes((self.point * pt).x()).hex() == given:
            return True
        return False

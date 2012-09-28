"""
Standard Convertible bond parameters and construct.
"""
from __future__ import absolute_import

import numpy as np

from model import WienerJumpProcess, BinomialModel, FDEModel, FDEBVModel
from payoff import CallA, Stack, Time, VariableStrike
from convertible_bond.payoff import Annuity, Call, Put

__all__ = ["dS", "dS_total", "dS_partial", "B", "P", "C", "S", "payoff", "T"]

# Time till maturity = 5 years
T = 5

# Stock price is a Wiener process with default jump.
#       Drift rate = 5%
#       Volatility = 20%
#       Hazard rate = 2%
# Total default (default = 100%)
dS_total = WienerJumpProcess(r=0.05, sigma=0.2, lambd_=0.02, eta=1)
# Partial default (default = 0%)
dS_partial = WienerJumpProcess(r=0.05, sigma=0.2, lambd_=0.02, eta=0)
# No default
dS = WienerJumpProcess(r=0.05, sigma=0.2)

# Bond
#       Nominal value = 100
#       Semi-annual coupon = 4
#       Recovery factor = 0
B = Annuity(T, np.arange(0.5, T + 0.5, 0.5), C=4, N=100, R=0)

# American put option on portfolio
#       Strike = 105
#       Time = 3
P = Time(Put(T, 105, B), times=[3])

# Reversed American call option on portfolio
#       Strike = 110
#       Time = [2, 5]
C = Time(Call(T, 110, B), times=[(2, 5)])

# Stock option (conversion option into stock for portfolio)
S = CallA(T, 0)

# Convertible bond:
#       Bond
#       American put option on portfolio
#       Reversed American call option on portfolio
#       Stock
payoff = Stack([B, P, C, S])

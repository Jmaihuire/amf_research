"""
Customised payoffs for pricing convertible bonds.
"""
from __future__ import absolute_import

from payoff import Annuity, CallVR, PutV, VariableStrike

__all__ = ["Annuity", "Call", "Put"]

class Annuity(Annuity):
    """Customised Annuity where coupon is payed as part of nominal."""
    def coupon(self, t):
        if t != self.T:
            return super(Annuity, self).coupon(t)
        return 0.0

    def terminal(self, S):
        V = super(Annuity, self).terminal(S)
        if self.T in self.times:
            V += self.C
        return V


class DirtyStrike(VariableStrike):
    """Create a strike that is adjusted for outstanding interest."""
    def __init__(self, T, K, A):
        super(DirtyStrike, self).__init__(T, K)
        self._A = A

    def strike(self, t):
        ti = 0
        accC = 0
        for i in self._A.times:
            if i > t:
                accC = self._A.C * (t - ti) / (i - ti)
                break
            ti = i
        return self.K + accC


class Put(DirtyStrike, PutV):
    """Customised PutV where strike price is adjusted for outstanding coupon."""
    pass


class Call(DirtyStrike, CallVR):
    """Customised CallVR where strike price is adjusted for outstanding coupon."""
    pass

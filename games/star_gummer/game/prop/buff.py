from abc import ABC, abstractmethod

class Buff(ABC):
    @abstractmethod
    def buff(self, player):
        pass

class RecoverBuff(Buff):
    def buff(self, player):
        player.hp += 10

class WSPBuff(Buff):
    def buff(self, player):
        if player.wsp < player.max_wsp:
            player.wsp += 1

class AttackBuff(Buff):
    def buff(self, player):
        player.attack += 3

class RangeBuff(Buff):
    def buff(self, player):
        player.range += 1
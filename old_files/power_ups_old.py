import pygame

class Power_ups():
    def __init__(self, duration, drop_rate):
        self.duration = duration
        self.drop_rate = drop_rate

class Shield(Power_ups): #misschien HP i.p.v duration
    def __init__(self, duration):
        super().__init__(duration)

class Speed_boost(Power_ups):
    def __init__(self, duration, multiplier):
        super().__init__(duration)

class Rapid_fire(Power_ups):
    def __init__(self, duration, multiplier):
        super().__init__(duration)

class Health_regain(Power_ups):
    def __init__(self, duration, regain_HP):
        super().__init__(duration)
        
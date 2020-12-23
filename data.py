import math
import random


class ProbabilisticValue:
    def __init__(self, values, upper_bounds):
        self.values = values
        self.upper_bounds = upper_bounds

    def get_a_value(self):
        index = 0
        seed = random.random()
        while True:
            if self.upper_bounds[index] >= seed:
                return self.values[index]
            index += 1


applications = 250
intake_size = 50
waitlist_size = 10

familyScoring = {"Unknown": 0
                ,"Known": 1
                ,"Established": 2
                ,"Prominent": 3
                ,"Illustrious": 5
                ,"Legendary": math.inf}

abilityScoring = {"Non-magical": -math.inf
                 ,"Magic-aware": -2
                 ,"Magic-user": 0
                 ,"Talented": 3
                 ,"Gifted": 6}

achievementsScoring = {"None": -1
                      ,"As Expected": 0
                      ,"Exceeding": 3
                      ,"Extraordinary": 6}

personalityScoring = {"Undesirable": -math.inf
                     ,"Suspect": -2
                     ,"As Expected": 0
                     ,"Good Fit": 2
                     ,"Excellent Fit": 4}

familyGen = ProbabilisticValue(["Unknown", "Known", "Established", "Prominent", "Illustrious", "Legendary"]
                              ,[0.16, 0.48, 0.75, 0.9, 0.985, 1.0])
abilityGen = ProbabilisticValue(["Non-magical", "Magic-aware", "Magic-user", "Talented", "Gifted"]
                               ,[0.14, 0.32, 0.75, 0.96, 1.0])
achievementsGen = ProbabilisticValue(["None", "As Expected", "Exceeding", "Extraordinary"]
                                   ,[0.3, 0.7, 0.96, 1.0])
personalityGen = ProbabilisticValue(["Undesirable", "Suspect", "As Expected", "Good Fit", "Excellent Fit"]
                                   ,[0.1, 0.3, 0.6, 0.9, 1.0])

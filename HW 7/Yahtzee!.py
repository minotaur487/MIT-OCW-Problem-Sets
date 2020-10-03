import random, math, pylab


class Die(object):

    def __init__(self):
        self.results = []


    def rollDie(self):
        rolled = math.ceil(6 * random.random())
        self.results.append(rolled)
        return rolled

def yahtzeeDiceSimulation(number, trials):
    yahtzee = 0
    dice = []
    for x in range(number):
        dice.append(Die())
    # xAxis = list(range(trials))
    # yAxis = []
    for trial in range(trials):
        t_res = []
        for die in dice:
            t_res.append(die.rollDie())
        if len(list(set(t_res))) == 1:
            yahtzee += 1
        # yAxis.append(yahtzee)
    # pylab.ylabel('Yahtzee')
    # pylab.xlabel('Roll')
    # pylab.plot(xAxis, yAxis)
    # pylab.show()
    return yahtzee/trials


xAxis = list(range(1, 101))
yAxis = []
for x in range(100):
    yAxis.append(yahtzeeDiceSimulation(5, 100000))
pylab.title('Probability of rolling a Yahtzee!')
pylab.ylabel('Probability')
pylab.xlabel('Trial')
pylab.hist(yAxis)
# pylab.plot(xAxis, yAxis)
pylab.show()

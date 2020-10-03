# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        prob = random.random()
        if prob < self.clearProb:
            return True
        return False

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        random_value = random.random()
        if random_value < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException()



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear():
                viruses.remove(virus)
        pop_density = len(viruses)/self.maxPop
        # pop_density = self.getTotalPop()/self.maxPop
        for virus in viruses:
            try:
                offspring = virus.reproduce(pop_density)
                viruses.append(offspring)
            except NoChildException:
                pass
        self.viruses = viruses
        return self.getTotalPop()



#
# PROBLEM 2
#
def simulationWithoutDrug(birth, clear):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    maxPop = 1000
    viruses = []
    for x in range(100):
        viruses.append(SimpleVirus(birth, clear))
    yAxis = [len(viruses)]
    # xAxis = [x for x in range(301)]
    patient = SimplePatient(viruses, maxPop)
    for y in range(300):
        yAxis.append(patient.update())
    # pylab.ylim(0, 600)
    # pylab.title('Virus Population in an Untreated Patient')
    # pylab.ylabel('Virus Population')
    # pylab.xlabel('Time Steps')
    # pylab.plot(xAxis, yAxis, 'bd')
    # pylab.show()
    return yAxis

finalResults = None

for i in range(100):
    # print "running trial", i
    results = simulationWithoutDrug(0.1, 0.05)
    if finalResults == None:
        finalResults = results
    else:
        for j in range(len(results)):
            finalResults[j] += results[j]

for i in range(len(finalResults)):
    finalResults[i] /= float(100)

pylab.plot(finalResults, label="SimpleVirus")
pylab.title("SimpleVirus simulation")
pylab.xlabel("time step")
pylab.ylabel("# viruses")
pylab.legend(loc="best")
pylab.show()

# simulationWithoutDrug(0.1, 0.05)
# simb = [x/100 for x in range(10, 100, 10)]
# simc = [x/100 for x in range(1, 20, 2)]
# for x in range(9):
#     simulationWithoutDrug(simb[x], 0.05)
# for x in range(9):
#     print(simc[x])
#     simulationWithoutDrug(0.1, simc[x])

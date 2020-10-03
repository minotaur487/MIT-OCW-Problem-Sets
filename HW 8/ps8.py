# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        return self.resistances[drug]


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        resistances_copy = self.resistances.copy()
        for drug in activeDrugs:
            if resistances_copy[drug] is False:
                # print("kapo")
                # print(self.resistances)
                raise NoChildException()

        random_value = random.random()
        if random_value < self.maxBirthProb * (1 - popDensity):
            for resistance in self.resistances:
                r_value = random.random()
                if self.mutProb > r_value:
                    # print("before", resistances_copy)
                    resistances_copy[resistance] = not self.resistances[resistance]
            #         print("after", resistances_copy)
            # print("done", resistances_copy)
            return ResistantVirus(self.maxBirthProb, self.clearProb, resistances_copy, self.mutProb)
        # print("chimp")
        raise NoChildException()


class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugTreatments = []



    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        self.drugTreatments.append(newDrug)
        set(self.drugTreatments)
        return list(self.drugTreatments)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugTreatments

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        pop_copy = []
        for x in range(len(self.viruses)):
            for drug in drugResist:
                if self.viruses[x].isResistantTo(drug) is True:
                    pop_copy.append(self.viruses[x])
        # for x in pop_copy:
        #     print(x.resistances)
        return len(pop_copy)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear():
                viruses.remove(virus)
        pop_density = float(len(viruses)) / self.maxPop
        # print(len(viruses))
        for virus in viruses:
            try:
                offspring = virus.reproduce(pop_density, self.drugTreatments)
                viruses.append(offspring)
            except NoChildException:
                # print("d")
                pass
        self.viruses = viruses
        return self.getTotalPop()


#
# PROBLEM 2
#

def simulationWithDrug():
    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    y_totdata = []
    y_guttadata = []
    x_totdata = range(300)
    for x in range(100):
        viruses = []
        for x in range(100):
            viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005))
        patient = Patient(viruses, 1000)
        timestep_list = []
        timestep_list_for_gutta = []
        for x in range(150):
            timestep_list.append(patient.update())
            timestep_list_for_gutta.append(patient.getResistPop(['guttagonol']))
        patient.addPrescription('guttagonol')
        for x in range(150):
            timestep_list.append(patient.update())
            timestep_list_for_gutta.append(patient.getResistPop(['guttagonol']))
        if len(y_totdata) == 0:
            y_totdata = timestep_list[:]
        else:
            for x in range(len(y_totdata)):
                y_totdata[x] += timestep_list[x]
        if len(y_guttadata) == 0:
            y_guttadata = timestep_list_for_gutta[:]
        else:
            for x in range(len(y_guttadata)):
                y_guttadata[x] += timestep_list_for_gutta[x]
    for x in range(len(y_totdata)):
        y_totdata[x] = y_totdata[x]/100
        y_guttadata[x] = y_guttadata[x] / 100
    # print(y_guttadata)
    pylab.title("Average Virus Population")
    pylab.plot(x_totdata, y_totdata, label="Average Pop")
    # pylab.title("Average Guttagonol-Resistant Virus Population")
    pylab.plot(x_totdata, y_guttadata, label="Guttagonol Resistant Pop")
    pylab.legend()
    pylab.show()


simulationWithDrug()

#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO




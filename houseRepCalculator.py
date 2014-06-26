#! /usr/bin/env python2

'''
Created on Apr 10, 2014
This is a little pgroam that takes a list of states by population and calculates the number of Congresmen for that state in the house of Representatives
@author: Matt - ASUS
'''



import operator
import math

def processLine(line):
    #basically, sometimes excel stores numbers as strings (if they contain a ,)
    #we need to remove these so we can return everything as a string
    placeholderLine = []
    line.replace(u'\xa0', u' ').encode('utf-8')
    line = line.split('\"')
    if (len(line) > 1) :
        line[1] = line[1].replace(',','') #removes all the commas in a number stored as a string
    for l in line:
        l = l.split(',') #splits finally
        [placeholderLine.append(i) for i in l]
        placeholderLine = [x for x in placeholderLine if x != '']

    line = placeholderLine
    return line 

def dictCreator(file):
    f = open(file, 'r')
    stateToPop = {}

    start = False
    for line in f:
        dataLine = processLine(line)
        if (dataLine[0] == '1') :
            start = True
        if (start): 
            if (len(dataLine) > 2) :
                stateToPop[dataLine[1]] = int(dataLine[2])
    f.close()
    return stateToPop

def huntingtonHillCalc(pop, n):
    return pop/(math.sqrt(n*(n+1)))

def calculateHouseSeats(stateToPop, priorityList, statesRepList, numSeats):
    for x in range(1, numSeats-len(priorityList) + 1):
        priorityList = sorted(priorityList, key = operator.itemgetter(1), reverse = True )
        firstState = priorityList[0][0]
        statesRepList[firstState] = statesRepList[firstState] + 1
        priorityList[0] = (firstState, (stateToPop[firstState]/math.sqrt(statesRepList[firstState]*(statesRepList[firstState]+1))))
    return statesRepList

def calculations(stateToPop, numSeats):
    statePriority = [(k, huntingtonHillCalc(v, 1)) for k, v in stateToPop.items()]
    stateReps = {k: 1 for k,v in stateToPop.items()}
    return (calculateHouseSeats(stateToPop,statePriority,stateReps,numSeats))
        

if __name__ == '__main__':

    #To do: Make not hardocoded
    #stateToPop = dictCreator('C:\\Users\\Matt - ASUS\\Dropbox\\Actual Fun\\AnglosphereEnglandAsMultiple.csv')            
    stateToPop = dictCreator('C:\\Users\\Matt - ASUS\\Dropbox\\Actual Fun\\AnglosphereEnglandAsMultiple.csv')            
    statePriority = [(k, huntingtonHillCalc(v, 1)) for k, v in stateToPop.items()]
    
    outputList = []
    output = (calculations(stateToPop, 435))
    f = open('C:\\Users\\Matt - ASUS\\Dropbox\\Actual Fun\\AnglosphereEnglandAsMultipleOutput.csv', 'w')
    for k,v in output.items() :
        outputList.append((k, v))
        s = str(k) + ',' + str(v) + '\n'
        f.write(s)
    outputList.sort(key = operator.itemgetter(0))
    
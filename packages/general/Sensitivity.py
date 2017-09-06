"""
Sensitivity

Date: 30-Oct-15
Authors: Y.M. Dijkstra
"""
import copy
import logging
import numpy as np
from src.util.diagnostics import KnownError
from nifty import toList
import numbers
import os

class Sensitivity:
    # Variables
    logger = logging.getLogger(__name__)
    skippedfiles = 0

    # Methods
    def __init__(self, input):
        self.input = input
        self.variables = toList(self.input.v('variables'))

        # check if values of variables are provided
        for var in self.variables:
            if self.input.v(var) is None:
                message = ("Not all required variables are given. Missing '%s' in module '%s'" % (var, self.__module__))
                raise KnownError(message)
        return

    def stopping_criterion(self, iteration):
        self.iteration = iteration+self.skippedfiles
        stop = False

        # stop if iteration number exceeds number of prescribed variables
        if self.iteration >= np.product(self.numLoops):
            stop = True
        return stop

    def run_init(self):
        """
        """
        # 1. Interpret values of variables; set values in self.values
        self.iteration=0
        self.values = {}
        for var in self.variables:
            # check if values are given directly or in a separate substructure
            varkeys = self.input.getKeysOf(var)

            # case 1: values supplied directly
            if not varkeys:
                values = self.input.v(var)
                values = self.interpretValues(values)
                self.values[var] = values
            # case 2: values in sub-dict
            else:
                # load values per key
                values = {}
                for key in varkeys:
                    temp = self.input.v(var, key)
                    values[key] = self.interpretValues(temp)

                # check that all keys have the same number of arguments
                for key in varkeys:
                    if len(values[key]) != len(values[varkeys[0]]):
                        raise KnownError('Problem with values of "%s" in input of module %s. Number of values in "%s" is unequal to number of values in "%s" ' % (var, self.__module__, key, varkeys[0]))

                # rewrite dict with lists to list with dicts
                self.values[var] = []
                for i in range(0,len(values[varkeys[0]])):
                    self.values[var].append({})
                    for key in varkeys:
                        self.values[var][i][key]=values[key][i]

        # Setup loop based on loopstyle
        if self.input.v('loopstyle') == 'permutations':
            self.numLoops =  [len(self.values[key]) for key in self.variables]
        elif self.input.v('loopstyle') == 'simultaneous':
            self.numLoops = [len(self.values[key]) for key in self.variables]
            # verify that number of values is the same in all variables
            for l in self.numLoops:
                    if l != self.numLoops[0]:
                        raise KnownError('Problem in input of module %s for loopstyle "simultaneous". Number of values in "%s" is unequal to number of values in "%s" ' % (self.__module__, var, self.variables[0]))
            self.numLoops = self.numLoops[0]
        else:
            raise KnownError('loopstyle "%s" in input of module %s unknown ' % (str(self.values.v('loopstyle')), self.__module__))

        d = self.run()
        return d

    def run(self):
        d = {}
        validfile = False
        while not validfile:
            # set variables
            iterationindex = np.unravel_index(self.iteration, self.numLoops)
            newvals = {}
            #   In case of simultaneous variations or single parameter
            if len(iterationindex)==1:
                for key in self.variables:
                    newvals[key] = self.values[key][iterationindex[0]]
            #   In case of permutative variation of multiple parameters
            else:
                for i, key in enumerate(self.variables):
                    newvals[key] = self.values[key][iterationindex[i]]

            # load to dictionary
            for key in self.variables:
                d[key] = copy.deepcopy(newvals[key])

            # check if this run can be skipped
            if self.input.v('checkFiles') == 'True':
                if self.checkIfExists(d):
                    if not self.stopping_criterion(self.iteration-self.skippedfiles+1):
                        self.skippedfiles += 1
                    else:
                        validfile = True
                else:
                    validfile = True
            else:               # never skip a file
                validfile = True

        self.logger.info('Sensitivity Analysis iteration %i of %i' % (self.iteration+1, np.prod(self.numLoops)))
        self.logger.info('\tValues:')
        for key in d:
            self.logger.info('\t%s = %s' % (key, str(d[key])))

        return d

    def interpretValues(self, values):
        #inpterpret values on input as space-separated list or as pure python input
        values = toList(values)

        # case 1: pure python: check for (, [, range, np.arange
        #   merge list to a string
        valString = ' '.join([str(f) for f in values])
        #   try to interpret as python string
        if any([i in valString for i in ['(', '[', ',', 'np.arange', 'range']]):
            try:
                valuespy = None
                exec('valuespy ='+valString)
                return valuespy
            except Exception as e:
                try: errorString = ': '+ e.msg
                except: errorString = ''
                raise KnownError('Failed to interpret input as python command %s in input: %s' %(errorString, valString), e)

        # case 2: else interpret as space-separated list
        else:
            return values

    def checkIfExists(self, newsettings):
        cwdpath = self.input.v('CWD') or ''       # path to working directory
        path = os.path.join(cwdpath, self.input.v('path'))
        if path[-1]!='/' or path[-1]!='\\':
            path += '/'
        ext = '.p'
        dc = self.input
        dc.merge(newsettings)

        # Prepare output file name format
        outputformat = ''.join(self.input.v('filename'))
        outputnames = []
        while outputformat.find('@{')>0:
            start = outputformat.find('@{')
            end = outputformat.find('}')
            outputnames.append(outputformat[start+2:end])
            outputformat = outputformat.replace(outputformat[start:end+1], '%s')

        counter = [0]*len(outputnames)    # set a counter for the case where the outputnames cannot be evaluated to a number; the counter then replaces this.

        # set output file name
        outnames = []
        for i, key in enumerate(outputnames):
            exec('outnames.append(dc.v('+key+'))')
            if not isinstance(outnames[-1], numbers.Number):
                try:
                    outnames[-1] = float(outnames[-1])
                except:
                    outnames[-1] = counter[i]
                    counter[i]+=1
        filename = outputformat % tuple(outnames)

        # check if file name already exists. If it does, append the filename by '_' + the first number >1 for which the path does not exist
        if os.path.exists(path+filename+ext):
            return True
        else:
            return False

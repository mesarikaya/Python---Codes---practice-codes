'''
Created on Jan 15, 2017

@author: Ergin
'''
# MSDice.py
#     Class definition for an n-sided dice

from random import randrange

class MyClass(object):
    '''
    classdocs
    '''
    def __init__(self, sides):
        '''
        Constructor
        '''
        self.sides = sides
        self.value = 1
        
        def roll(self):
            self.value = randrange(1,self.sides)
            
        def getValue(self):
            return self.value
        
        def setValue(self,value):
            self.value = value
            
        
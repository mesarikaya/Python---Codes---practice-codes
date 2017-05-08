# -*- coding: utf-8 -*-
"""
Created on Mon Apr 3

@author: Ergin Sarikaya
"""

def solution(args):
    
    """A format for expressing an ordered list of integers is to use a comma 
    separated list of either;
    -  individual integers
    -  or a range of integers denoted by the starting integer separated from the
    end integer in the range by a dash, '-'. The range includes all integers in
    the interval including both endpoints. It is not considered a range unless
    it spans at least 3 numbers. For example ("12, 13, 15-17")
    Complete the solution so that it takes a list of integers in increasing order
    and returns a correctly formatted string in the range format.

    Example:
    
    solution([-6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20])
    # returns "-6,-3-1,3-5,7-11,14,15,17-20"
    Courtesy of rosettacode.org"""
    
    # Find the difference between the consecutive numbers
    if len(args) <= 1:
        return args
    else:
        diff_list = [args[i+1]-args[i] for i in range(len(args)-1)]
        
        # Find the locations of differences that are bigger than 1
        locs = [i+1 for i in range(len(diff_list)) if diff_list[i]>1]
        if locs == []:
            return []
        else:
            if locs[-1] < (len(args)-1):
                locs.append(len(args))
        # print(locs)
        result = []
        
        # Create the final representation
        for i in range(len(locs)):
            # print("locs:", locs[i])
            if i == 0:
                if locs[i]>2:
                    result.append(str(args[0]) + "-" + str(args[locs[i]-1]))
                else:
                    for k in range(locs[i]):
                        result.append(str(args[k]))
                #result.append(args[0:locs[i]+1])
            else:
                if locs[i] - locs[i-1] >=3:
                    if locs[i] == len(args)-1:
                        result.append(str(args[locs[i-1]]) + "-" + str(args[locs[i]-1]))
                        result.append(str(args[locs[i]]))
                    else:
                        result.append(str(args[locs[i-1]]) + "-" + str(args[locs[i]-1]))
                else:
                    if locs[i] == len(args)-1:
                        for n in range(locs[i-1], locs[i]+1):
                            result.append(str(args[n]))                        
                    else:
                        for n in range(locs[i-1], locs[i]):
                            result.append(str(args[n]))
            # print(result)
        return ",".join(result)
        
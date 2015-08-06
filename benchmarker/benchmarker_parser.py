#!/usr/bin/python3.4

"""This module contains the functions parse_time_output,
   merge_CommandStats, print_CS and the object CommandStat.
   CommandStat: stats are those parsed from the output of /usr/bin/time.
   parse_time_output: parses file containing batch output of
                      /usr/bin/time to produce CommandStat objects.
   merge_CommandStats: merges CommandStat objects with statistics
                       for the same command."""
import os

class CommandStat(object):
    """CommandStat object. Holds a list of Stat objects.
       E.g. Elapsed time, resident stack size, produced by /usr/bin/time"""
    def __init__(self, name, stat_list):
        """init with a name and a list of Stat objects"""
        self.name = name
        self.stats = stat_list
        
    def merge(self,CS):
        """updates self to append Stat values of another CS object."""
        #create temp list to store merged list
        new_list = []
        #iterate by index through self.stats and CS.stats
        for i in range(len(self.stats)):
            stat1 = self.stats[i]
            stat2 = CS.stats[i]
            stat1.values += stat2.values

class Stat(object):
    """Stat object. Holds a name and list of values. E.g. Time: 12, 2"""
    def __init__(self, name, value):
        """Init with name and single value, converted to list,
           accommodates later merging with Stat of same name."""
        self.name = name
        self.values = [value]


def parse_time_output(fname):
    """Take a file name to parse, return list of CommandStat objects."""
    #split by "Command being timed:"
    s = open(fname).read().split("Command being timed: ")[1:]
    #temp list to hold returned CommandStat objects
    l = []
    for i in s:
        #"sh -c name" is the first element if split by newline
        name = i.split("\n")[0].split()[2]
        #templist that will be the CommandStat's list of Stats
        temp_list = []
        #first being name, 24th being the last.
        for line in i.split("\n")[1:24]:
            if "Elapsed" not in line:
                #all except elapsed time are name:value, so split by :
                stat_name = line.split(":")[0].lstrip("\t")
                #a few different cases where command:val, val not float
                if stat_name == "Percent of CPU this job got":
                    stat_val = float(line.split(":")[1].rstrip("%"))/100
                    stat_name = "Fraction of CPU this job got"
                elif "Submission date and time" in stat_name:
                    #submission date and time will have 2 or 3 :s in the line 
                    stat_name = stat_name.lstrip("\t")
                    stat_val = ":".join(line.split(":")[1:])
                else:
                    stat_val = float(line.split(":")[1])
                stat = Stat(stat_name, stat_val)
            else:
                #in this case, convert hh:mm:ss to seconds for graphing
                stat_name = ":".join(line.split(":")[0:4]).lstrip("\t")
                stat_val = line.split(":")[4:]
                #wall clock time can either me hh:mm:ss or m:ss
                stat_name = "Elapsed (wall clock) time in seconds"
                if len(stat_val) == 3:
                    stat_val = float(line.split(":")[4])*3600 + float(line.split(":")[5])*60 + float(line.split(":")[6])
                else:
                    stat_val = float(line.split(":")[4])*60 + float(line.split(":")[5])
                stat = Stat(stat_name, stat_val)
            temp_list.append(stat)
        #l now contains a list of tuples, so create CommandStat to hold it
        l.append(CommandStat(name, temp_list))
    #return a merged list of CommandStats
    return merge_CommandStats(l)

def merge_CommandStats(CS_list):
    """Takes list of CommandStat objects, merges those with the same name"""
    used_names = {}
    for i in CS_list:
        if i.name not in used_names:
            used_names[i.name] = i
        else:
            #otherwise the names is already taken, update previous CS
            used_names[i.name].merge(i)
    # return merged CommandStat objects
    return [q for i,q in used_names.items()]

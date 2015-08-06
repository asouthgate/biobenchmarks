#!/usr/bin/python3.4

import os

"""Module for writing information contained in CommandStat objects
   to .csv outfile."""

def write_csv(CSs, outfile):
    """Takes CS object, formats stats and appends them to outfile.csv"""
    current_dir = os.path.join(os.path.dirname(__file__))
    out = open(current_dir+"/../output/" + outfile,"w")
    for CS in sorted(CSs, key=lambda x:x.name):
        maxlen = max([len(i.values) for i in CS.stats])
        out.write(CS.name+","*(maxlen+2)+"avg,stdev,min,max"+"\n")
        for i in CS.stats:
            if i.name != "Submission date and time":
                avg = sum([val for val in i.values])/len(i.values)
                mini = min(i.values)
                maxi = max(i.values)
                var = ((sum([(val-avg)**2 for val in i.values]))/(len(i.values)-1))
                stdev = var**(1/2)
                out.write(i.name+","+",".join([str(val) for val in i.values])+",,"+str(avg)+","+str(stdev)+","+str(mini)+","+str(maxi)+"\n")
            else:
                out.write(i.name+","+",".join([str(val) for val in i.values])+"\n")
        out.write("\n")
    out.close()
    return 0

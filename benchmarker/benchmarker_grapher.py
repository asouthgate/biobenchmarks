#!/usr/bin/python3.4

"""This module contains graph_CS(), produces graphs for CommandStat objects"""

import matplotlib.pyplot as plt
import numpy
import benchmarker.benchmarker_parser
import traceback
import os

current_dir = os.path.join(os.path.dirname(__file__))

#unwanted statistics; don't graph these
unwanted = {"Fraction of CPU this job got",
            "Average shared text size (kbytes)",
            "Average unshared data size (kbytes)",
            "Average resident set size (kbytes)",
            "Average stack size (kbytes)",
            "Average total size (kbytes)",
            "Socket messages sent",
            "Socket messages received",
            "Signals delivered",
            "Page size (bytes)",
            "Exit status",
            "Submission date and time"}
            
def graph_CS(CS):
    """Take CommandStat object CS and for each pair in
       CS.stats, plot a bar chart against submission datetime"""
    #submission datetimes are always the last stat in CS.stats.
    submission_datetimes = CS.stats[-1].values
    #iterate through all statistics in CS.stats
    for stat in CS.stats:
        #check if statistics[0], the title, is unwanted
        if stat.name not in unwanted:                        
            try:
                #produce the graph
                title = CS.name + "-" + stat.name
                yvals = stat.values
                fig = plt.figure()
                indd = numpy.arange(len(yvals))
                plt.bar(indd, yvals, width=0.8)
                plt.xticks(indd, submission_datetimes)
                plt.ylabel(stat.name)
                plt.xlabel("Date and time")
                plt.title(title)
                fig.autofmt_xdate()
                current_dir = os.path.join(os.path.dirname(__file__))
                plt.savefig(current_dir+"/../output/graphs/"+title.replace("/","").replace(" ","_"))
                plt.close()
            except:
                print(traceback.format_exc())

def graph_scores():
    """Graph final scores"""
    with open(current_dir + "/../output/scores.csv") as f:
        scores = f.read().split("\n")[:-1]
    title = "Benchmarking scores as relative speedup to reference times"
    yvals = [float(i.split(",")[1]) for i in scores]
    xvals = [i.split(",")[0] for i in scores]
    fig = plt.figure()
    indd = numpy.arange(len(yvals))
    plt.bar(indd, yvals, width=0.8)
    plt.xticks(indd, xvals)
    plt.ylabel("Relative speedup")
    plt.xlabel("Tools")
    plt.title(title)
    fig.autofmt_xdate()
    plt.savefig(current_dir+"/../output/graphs/scores")
    plt.close()
        

#!/usr/bin/python3.4

import sys
import os
from functools import reduce

"""Parser for .csv output of benchmarker-runner write_csv.
Takes two inputs, the dataset, and the reference for comparison of speedup."""

commands = ["gunzip", "velvetg", "velveth", "snippy", "beast", "phyml",
            "prokka", "nhmmer", "blastn", "muscle"]

def csv_parser(fname):
    """Take filename.csv, return average Elapsed time for each command"""
    average_times = {}
    f = open(fname)
    for line in f:
        fields = line.split(",")
        #to be compatible with old outfile.csv
        #get only those up to an empty field (any further will be new stats such as stdev)
        for i in range(len(fields)):
            if fields[i] == '':
                fields = fields[:i]
                break
        comm = fields[0].strip().split("/")[-1]
        if comm in commands:
            command_name = comm
        if fields[0].startswith("Elapsed"):
            avg = sum([float(i) for i in fields[1:]])/len(fields[1:])
            average_times[command_name] = avg
    f.close()
    return average_times

def get_score_dict(average_times, reference_times):
    """Take two dicts, return new dict of quotient of vals for each key"""
    return {i:reference_times[i]/q for i,q in average_times.items()}

def get_scores(fname):
    """Call csv_parser and get_score_dict, write to outfile"""
    current_dir = os.path.join(os.path.dirname(__file__))
    average_times = csv_parser(fname)
    reference_average_times = csv_parser(current_dir+"/res/arcca_output_22_07.csv")
    final_scores = get_score_dict(average_times, reference_average_times)
    outf = open(current_dir+"/../output/scores.csv", "w")
    for i,q in sorted(final_scores.items()):
        outf.write(i + "," + str(q)[:8]+"\n")
    score_vals = [val for i,val in final_scores.items()]
    outf.write("geometric mean," + str(reduce(lambda x, y: x * y, score_vals, 1)**(1/len(score_vals)))[:8] + "\n\n\n\n\n")
    outf.write("\n")
    outf.close()
    return 0

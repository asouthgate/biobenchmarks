#!/usr/bin/python3.4

"""This module contains the parse_and_graph function.
   parse_and_graph: calls benchmarker_parser.parse_time_output,
                    parsing output/command_times.out,
                    then calls benchmarker_parser.write_CS_csv
                    or benchmarker_grapher.graph_CS"""

import benchmarker.benchmarker_parser as parser
import benchmarker.benchmarker_grapher as grapher
import benchmarker.benchmarker_write_csv as csv_writer
import benchmarker.benchmarker_scorer as scorer
import os

def parse_and_graph(arg):
    """Takes 'write_csv' or 'graph' as arguments
       Calls parser.parse_time_output,
       producing a list of CommandStat objects.
       Calls benchmarker_write_csv.write_CS_csv
       or benchmarker_grapher.graph_CS"""
    current_dir = os.path.join(os.path.dirname(__file__))
    #Get a list of CommandStats by parsing command_times.out
    if arg == "graph_scores":
        grapher.graph_scores()
        return 0
    CSs = parser.parse_time_output(current_dir+"/../output/command_times.out")
    #Iterate through list, and for each CS, write_CS_csv and graph_CS
    if arg == "output":
        csv_writer.write_csv(CSs, "outfile.csv")
        scorer.get_scores(current_dir+"/../output/outfile.csv")
    if arg == "graph_data":
        for CS in CSs:
            grapher.graph_CS(CS)
    return 0

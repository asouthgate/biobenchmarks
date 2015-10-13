#!/usr/bin/python3.4

"""Benchmarker script containing main().
   Takes one of four arguments: run, graph, write_csv, devWipe.
   run: runs benchmarks; calls benchmarker_timer.time_commands.
        If counter.txt contains a number, run that many times,
        rebooting in between runs.
        Warning!: Reboot intended for possible VM use only.
   graph: calls benchmarker_parse_and_graph.parse_and_graph;
          generates graphs in output/graphs/<graph>.
   write_csv: calls benchmarker_parse_and_graph.parse_and_graph,
          writes csv to output/outfile.csv
   devWipe: calls cleanup.bsh; wipes all temp and output"""

usage = "Usage: benchmarker-runner.py [command] \n\
commands: \n\
        run n        - runs benchmarks, where optional n specifies the number of runs to perform, with n-1 restarts in between \n\
        output       - outputs data to output/ \n\
        sysinfo      - retrieves sysinfo, outputs to /output/sysinfo/ and /output/combined_sysinfo \n\
        graph_data   - graphs raw data to output/graphs \n\
        graph_scores - graphs scores to output/graphs \n\
        devWipe      - wipes all collected data, scores, and temp files"

from benchmarker.benchmarker_grapher import graph_CS
from benchmarker.benchmarker_parse_and_graph import parse_and_graph
from benchmarker.benchmarker_timer import time_commands

import sys
import os
import subprocess

__version__ = "0.1.0"

def main():
        """Takes four command-line arguments: run, output, sysinfo, graph, devwipe"""
        current_dir = os.path.join(os.path.dirname(__file__))
        #If called with no arguments, print usage
        if len(sys.argv) == 1:
                print(usage)
                return 1
        if sys.argv[1] == "graph_data":
                parse_and_graph("graph_data")
        elif sys.argv[1] == "graph_scores":
                parse_and_graph("graph_scores")
        elif sys.argv[1] == "sysinfo":
                subprocess.call("./sysinfo_commands",shell=True,
                                cwd=current_dir);
                print("see output/sysinfo/ for individual sysinfos, outout/combined_sysinfo for combined");
        elif sys.argv[1] == "output":
                parse_and_graph("output")
                subprocess.call("cat ../output/scores.csv ../output/outfile.csv > ../output/combined_output.csv",
                                shell=True, cwd=current_dir)
                print("see output/scores.csv for scores")
                print("see output/outfile.csv for data")
                print("see output/combined_data.csv for combined scores and data")
        elif sys.argv[1] == "devWipe":
                subprocess.call("./cleanup.bsh",shell=True,
                                cwd=current_dir)
        #If called with run, call time_commands and perform reboot check
        elif sys.argv[1] == "run":
                if len(sys.argv) == 3:
                        #if speficied, n will determine the number of reboots to perform
                        n_restarts = int(sys.argv[2])-1
                        f = open(current_dir+"/counter.txt", "w")
                        f.write(str(n_restarts))
                        f.close()
                time_commands("commands.txt", current_dir)
                number_of_runs = int(open(current_dir+"/counter.txt").read())
                #If this number is > 0, perform a reboot
                if number_of_runs > 0:
                        countf = open(current_dir+"/counter.txt", "w")
                        countf.write(str(number_of_runs-1))
                        countf.close()
                        print("Rebooting...")
                        subprocess.call("sudo reboot".split())
                else:
                        print("No reboot.")
        else:
                print(usage)
                return 1
        return 0
    
	

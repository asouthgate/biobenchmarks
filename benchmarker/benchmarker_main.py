#!/usr/bin/python3.4

"""Benchmarker script containing main().
   Takes one of four arguments: run, graph, write_csv, devWipe.
   run: runs benchmarks; calls benchmarker_timer.time_commands.
        If counter.txt contains a number, run that many times,
        rebooting in between runs.
        Warning!: Reboot intended for possible VM use only.
   output: calls benchmarker_parser, benchmarker_write_csv,
          benchmarker_scorer.
          writes csv to output/outfile.csv
   devWipe: calls cleanup.bsh; wipes all temp and output"""

usage = "Usage: benchmarker-runner.py [command] \n\
commands: \n\
        run n        - runs benchmarks, where optional n specifies the number of runs to perform, with n-1 restarts in between \n\
        output       - outputs data to output/ \n\
        devWipe      - wipes all collected data, scores, and temp files"

from benchmarker.benchmarker_timer import time_commands
import benchmarker.benchmarker_parser as parser
import benchmarker.benchmarker_write_csv as csv_writer
import benchmarker.benchmarker_scorer as scorer

import sys
import os
import subprocess

__version__ = "0.1.0"

def main():
        """Takes four command-line arguments: run, output, graph, devwipe"""
        current_dir = os.path.join(os.path.dirname(__file__))
        #If called with no arguments, print usage
        if len(sys.argv) == 1:
                print(usage)
                return 1
        if sys.argv[1] == "output":
                #Get a list of CommandStat objects by parsing command_times.out
                CSs = parser.parse_time_output(current_dir+"/../output/command_times.out")
                csv_writer.write_csv(CSs, "outfile.csv")
                scorer.get_scores(current_dir+"/../output/outfile.csv")
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
    
	

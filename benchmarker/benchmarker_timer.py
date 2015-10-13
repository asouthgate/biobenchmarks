#!/usr/bin/python3.4

"""Timer module that contains the function: time_commands."""

import subprocess

def time_commands(filename, curwd):
        """Take the name of a file containing commands
           and a working directory, call subrocess
           with /usr/bin/time for each command in the file"""
        for command in open(curwd+"/"+filename):
                if command.startswith("#"):
                         #in this case, we don't want to time it
                         print("not timing: ", command[1:])
                         subprocess.call(command[1:].strip(), shell=True, cwd=curwd)
                else:
                         #t_command and date_time are full command and
                         #current date and time, respectively
                         t_command = "/usr/bin/time -v -a -o ../output/command_times.out -p sh -c " +"'"+ command.strip()+"'"
                         print(t_command)
                         date_time = """echo '\tSubmission date and time: ' $(date "+%Y-%m-%d %H:%M:%S")'\n' >> ../output/command_times.out"""
                         subprocess.call(t_command, shell=True, cwd=curwd)
                         subprocess.call(date_time, shell=True, cwd=curwd)
        return 0

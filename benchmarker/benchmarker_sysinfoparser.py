#!/usr/bin/python3.4

import sys

def parse_cpuinfo(fname, outfname):
        wanted = ["processor", "cpu family", "model", "model name", "stepping", "microcode", "cpu MHz",
                  "cache size", "cpu cores", "core id", "clflush size", "cache_alignment", "address sizes"]
        outf = open(outfname, "a")
        for i in open(fname):
                l = [q.strip() for q in i.strip().split(":")]
                if l[0] in wanted:
                        outf.write(l[0]+","+l[1]+"\n")
        outf.write("\n\n")
        outf.close()

def parse_dmidecode(fname, outfname):
        wanted = ["Memory Device", "Type", "Speed"]
        outf = open(outfname, "a")
        for i in open(fname):
                l = [q.strip() for q in i.strip().split(":")]
                if l[0] in wanted:
                        if len(l) > 1:
                                if l[1].strip() not in ["Desktop", "Central Processor", "Video", "OK"]:
                                        outf.write(l[0]+","+l[1]+"\n")
                        else:
                                outf.write(l[0]+"\n")
        outf.write("\n\n")
        outf.close()

def parse_memoinfo(fname, outfname):
        wanted = ["MemTotal"]
        outf = open(outfname, "a")
        for i in open(fname):
                l = [q.strip() for q in i.strip().split(":")]
                if l[0] in wanted:
                        outf.write(l[0]+","+l[1]+"\n")
        outf.write("\n\n")
        outf.close()

def parse_lspci(fname, outfname):
        outf = open(outfname, "a")
        for i in open(fname):
                outf.write(i.replace(" ", ","))
        outf.write("\n\n")
        outf.close()

def parse_release(fname, outfname):
        outf = open(outfname, "a")
        for i in open(fname):
                if i.split("=")[0] in ["DISTRIB_ID", "DISTRIB_RELEASE"]:
                        outf.write(i.replace("=", ","))
        outf.write("\n\n")
        outf.close()
        

if __name__ == "__main__":
        parse_cpuinfo(sys.argv[1]+"/cpuinfo.sysinfo", sys.argv[2])
        parse_memoinfo(sys.argv[1]+"/meminfo.sysinfo", sys.argv[2])
        parse_release(sys.argv[1]+"/release.sysinfo", sys.argv[2])
        parse_lspci(sys.argv[1]+"/lspci.sysinfo", sys.argv[2])
        parse_dmidecode(sys.argv[1]+"/dmidecode.sysinfo", sys.argv[2])


        

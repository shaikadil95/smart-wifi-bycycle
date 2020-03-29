import time, sys, os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("square", help="display",
                    type=int)
args = parser.parse_args()
print args.square
time.sleep(args.square)
print "BAN!"

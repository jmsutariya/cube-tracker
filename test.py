#!/usr/bin/env python3

from rubikscolorresolver import RubiksColorSolverGeneric, RubiksColorSolver3x3x3
from math import sqrt
import argparse
import json
import logging
import sys

# logging.basicConfig(filename='rubiks-rgb-solver.log',
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)5s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))

# To add a test case:
# - place the cube in the robot, solve it
# - in the log output grab the "RGB json" and save that in a file in test-data
# - in the log output grab the "Final cube for kociema", this is what you put in the entry in the test_cases tuple
test_cases = (
    ('2x2x2 solved',       'test-data/2x2x2-solved.txt',       'DDDDBBBBLLLLUUUUFFFFRRRR'),
    ('3x3x3 solved',       'test-data/3x3x3-solved.txt',       'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'),
    ('3x3x3 checkerboard', 'test-data/3x3x3-checkerboard.txt', 'UDUDUDUDURLRLRLRLRFBFBFBFBFDUDUDUDUDLRLRLRLRLBFBFBFBFB'),
    ('3x3x3 cross',        'test-data/3x3x3-cross.txt',        'DUDUUUDUDFRFRRRFRFRFRFFFRFRUDUDDDUDUBLBLLLBLBLBLBBBLBL'),
    ('3x3x3 tetris',       'test-data/3x3x3-tetris.txt',       'FFBFUBFBBUDDURDUUDRLLRFLRRLBBFBDFBFFUDDULDUUDLRRLBRLLR'),
    ('3x3x3 superflip',    'test-data/3x3x3-superflip.txt',    'UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB'),
    ('3x3x3 random 01',    'test-data/3x3x3-random-01.txt',    'DURUULDBRFDFLRRLFBRLUUFFUFFLRUDDDRRDLBBDLLBBBDFFBBRLUU'),
    ('4x4x4 solved',       'test-data/4x4x4-solved.txt',       'DDDDDDDDDDDDDDDDBBBBBBBBBBBBBBBBLLLLLLLLLLLLLLLLUUUUUUUUUUUUUUUUFFFFFFFFFFFFFFFFRRRRRRRRRRRRRRRR'),
    ('4x4x4 turn UR',      'test-data/4x4x4-turn-UR.txt',      'UUURUUUFUUUFUUUFRRRBRRRBRRRBRRRBRRRDFFFDFFFDFFFDDDDBDDDBDDDBDDDLFFFFLLLLLLLLLLLLULLLUBBBUBBBUBBB'),
)

results = []

for (desc, filename, expected) in test_cases:
    with open(filename, 'r') as fh:
        scan_data_str_keys = json.load(fh)
        scan_data = {}

        for (key, value) in scan_data_str_keys.items():
            scan_data[int(key)] = value

        square_count = len(scan_data.keys())
        square_count_per_side = int(square_count/6)
        width = int(sqrt(square_count_per_side))

        # remove the False if you want to test with the old RubiksColorSolver3x3x3
        if False and width == 3:
            cube = RubiksColorSolver3x3x3()
        else:
            cube = RubiksColorSolverGeneric(width)

        cube.enter_scan_data(scan_data)
        cube.crunch_colors()
        output = ''.join(cube.cube_for_kociemba_strict())

        if output == expected:
            results.append("PASS: %s" % desc)
        else:
            results.append("FAIL: %s %s" % (desc, output))
            results.append("   expected %s" % expected)

print('\n'.join(results))
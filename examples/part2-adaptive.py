# 
#      Scene Detection with Python and OpenCV - Example Program
# Part 2: Adaptive Fade Detection             By: Brandon Castellano
#
# http://www.bcastell.com/tech-articles/pyscenedetect-tutorial-part-2/
#
# This Python program implements a more advanced and optimized threshold-
# based scene detection algorithm, and improves the output format so
# the scene cuts can be more easily imported into other programs (e.g.
# ffmpeg, mkvmerge). Basic usage is:
#
#   > python part2-adaptive.py [-h] -i VIDEO_FILE
#
# Where -i denotes the input video, and -h shows the help message.
# Optional arguments that can be passed after VIDEO_FILE are:
#
#  -h, --help            show this help message and exit
#  -i VIDEO_FILE, --input VIDEO_FILE
#                        [REQUIRED] Path to input video. (default: None)
#  -t intensity, --threshold intensity
#                        8-bit intensity value, from 0-255, to use as a fade
#                        in/out detection threshold. (default: 8)
#  -m percent, --minpercent percent
#                        Amount of pixels in a frame, from 0-100%, that must
#                        fall under [intensity]. (default: 95)
#  -b rows, --blocksize rows
#                        Number of rows in frame to check at once, can be tuned
#                        for performance. (default: 32)
#  -s offset, --startindex offset
#                        Starting index for chapter/scene output. (default: 0)
#
# Example:
#   > python part2-adaptive.py -i testvideo.mp4
#   > python part2-adaptive.py -i testvideo.mp4  -t 8  -m 95  -b 32  -s 0
#
# For each fade/cut that is detected, the timecodes and frame numbers
# are printed to stdout. Note that this program depends on the Python
# OpenCV bindings and NumPy.
#
# Copyright (C) 2013-2014 Brandon Castellano <http://www.bcastell.com>.
# I hereby release this file into the public domain.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#


import sys
import argparse

import cv2
import numpy as np


def int_type_check(min_val, max_val = None, metavar = None):
    if metavar == None: metavar = 'value'
    def _type_check(value):
        value = int(value)
        valid = True
        msg   = ''
        if (max_val == None):
            if (value < min_val): valid = False
            msg = 'invalid choice: %d (%s must be at least %d)' % (
                value, metavar, min_val )
        else:
            if (value < min_val or value > max_val): valid = False
            msg = 'invalid choice: %d (%s must be between %d and %d)' % (
                value, metavar, min_val, max_val )
        if not valid:
            raise argparse.ArgumentTypeError(msg)
        return value
    return _type_check


def get_cli_parser():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = 'arguments'

    parser.add_argument('-i', '--input', metavar = 'VIDEO_FILE',
        type = file, required = True,
        help = '[REQUIRED] Path to input video.')
    parser.add_argument('-t', '--threshold',  metavar = 'intensity',
        type = int_type_check(0, 255, 'intensity'), default = 8,
        help = '8-bit intensity value, from 0-255, to use as a fade in/out detection threshold.')
    parser.add_argument('-m', '--minpercent', metavar = 'percent',
        type = int_type_check(0, 100, 'percentage'), default = 95,
        help = 'Amount of pixels in a frame, from 0-100%%, that must fall under [intensity].')
    parser.add_argument('-b', '--blocksize',  metavar = 'rows',
        type = int_type_check(0, None, 'number of rows'), default = 32,
        help = 'Number of rows in frame to check at once, can be tuned for performance.')
    parser.add_argument('-s', '--startindex', metavar = 'offset',
        type = int, default = 0,
        help = 'Starting index for chapter/scene output.')

    return parser


def main():
    args = get_cli_parser().parse_args()

    print args

    pass

    
if __name__ == "__main__":
    main()

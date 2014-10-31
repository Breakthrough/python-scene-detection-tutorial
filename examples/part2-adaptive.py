#!/usr/bin/env python
# 
#      Scene Detection with Python and OpenCV - Example Program
# Part 2: Adaptive Fade Detection             By: Brandon Castellano
#
# http://www.bcastell.com/tech-articles/pyscenedetect-tutorial-part-2/
#
# This Python program implements an optimized, threshold-based
# scene detection algorithm, and improves the output format so that
# scene cuts can be more easily imported into other programs (e.g.
# ffmpeg, mkvmerge).  Usage:
#
#   ./python part2-adaptive.py VIDEO_FILE [intensity = 16]
#
# Which will export a list of scenes and their timecodes (by default)
# detected in VIDEO_FILE, using the intensity as a threshold.  Other
# parameters (e.g. minimum match percent and block size) can be
# modified just above the main function in the source below.
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
import cv2
import numpy as np


# Advanced Scene Detection Parameters
INTENSITY_THRESHOLD = 16    # Pixel intensity threshold (0-255), default 16
MINIMUM_PERCENT     = 95    # Min. amount of pixels to be below threshold.
BLOCK_SIZE          = 32    # Num. of rows to sum per iteration.


def main():
    if len(sys.argv) < 2:
        print "Error - file name must be specified as first argument."
        return
    
    cap = cv2.VideoCapture()
    cap.open(sys.argv[1])
    
    if not cap.isOpened():
        print "Fatal error - could not open video %s." % sys.argv[1]
        return
    else:
        print "Parsing video %s..." % sys.argv[1]
        
    # Do stuff with cap here.

    width  = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print "Video Resolution: %d x %d" % (width, height)

    # Allow the threshold to be passed as an optional, second argument to the script.
    threshold = 16
    if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
        threshold = int(sys.argv[2])
    print "Detecting scenes with threshold = %d" % threshold
    print "Min. pixels under threshold = %d %%" % MINIMUM_PERCENT
    print "Block/row size = %d" % BLOCK_SIZE
    print ""

    min_percent = MINIMUM_PERCENT / 100.0
    num_rows    = BLOCK_SIZE
    last_amt    = 0     # Number of pixel values above threshold in last frame.
    start_time  = cv2.getTickCount()  # Used for statistics after loop.

    while True:
        # Get next frame from video.
        (rv, im) = cap.read()
        if not rv:   # im is a valid image if and only if rv is true
            break

        # Compute # of pixel values and minimum amount to trigger fade.
        num_pixel_vals = float(im.shape[0] * im.shape[1] * im.shape[2])
        min_pixels     = int(num_pixel_vals * (1.0 - min_percent))

        # Loop through frame block-by-block, updating current sum.
        frame_amt = 0
        curr_row  = 0
        while curr_row < im.shape[0]:
            # Add # of pixel values in current block above the threshold.
            frame_amt += np.sum(
                im[curr_row : curr_row + num_rows,:,:] > threshold )
            if frame_amt > min_pixels:  # We can avoid checking the rest of the
                break                   # frame since we crossed the boundary.
            curr_row += num_rows

        # Detect fade in from black.
        if frame_amt >= min_pixels and last_amt < min_pixels:
            print "Detected fade in at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )

        # Detect fade out to black.
        elif frame_amt < min_pixels and last_amt >= min_pixels:
            print "Detected fade out at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )

        last_amt = frame_amt      # Store current mean to compare in next iteration.

    # Get # of frames in video based on the position of the last frame we read.
    frame_count = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    # Compute runtime and average framerate
    total_runtime = float(cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    avg_framerate = float(frame_count) / total_runtime

    print "Read %d frames from video in %4.2f seconds (avg. %4.1f FPS)." % (
        frame_count, total_runtime, avg_framerate)

    cap.release()


if __name__ == "__main__":
    main()

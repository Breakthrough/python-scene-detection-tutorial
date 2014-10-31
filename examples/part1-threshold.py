# 
#      Scene Detection with Python and OpenCV - Example Program
# Part 1: Threshold/Fade-to-Black Detection      By: Brandon Castellano
#
# http://www.bcastell.com/tech-articles/pyscenedetect-tutorial-part-1/
#
# This Python program implements a simple threshold-based scene detection
# algorithm using a set threshold compared to the average pixel intensity
# of each frame. Usage:
#
#   > python part1-threshold.py [video-file] [intensity = 15]
#
# Where [video-file] is a path to the video to be parsed, and [intensity]
# is the average pixel intensity from 0 to 255 to be used as a cut-off
# (if unspecified, the default value of 15 is used).  Example:
#
#   > python part1-threshold.py testvideo.mp4 8
#
# For each fade/cut that is detected, the timecodes and frame numbers
# are printed to stdout. Note that this program depends on the Python
# OpenCV bindings and NumPy. This software is a proof of concept related
# to the tutorial above, so note many error checks are skipped for brevity.
#
# Copyright (C) 2013-2014 Brandon Castellano <http://www.bcastell.com>.
#
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

def main():
    if len(sys.argv) < 2:
        print "Error - file name must be specified as first argument."
        print "See the header of part1-threshold.py for usage details."
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
    threshold = 15
    if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
        threshold = int(sys.argv[2])
    print "Detecting scenes with threshold = %d.\n" % threshold

    last_mean  = 0                   # Mean intensity of the *last* frame processed.
    start_time = cv2.getTickCount()  # Used for benchmarking/statistics after loop.

    while True:
        # Get next frame from video.
        (rv, im) = cap.read()
        if not rv:   # im is a valid image if and only if rv is true
            break

        # Compute mean intensity of pixels in frame.
        frame_mean = np.sum(im) / float(im.shape[0] * im.shape[1] * im.shape[2])
        # Dividing the sum by the image size is 35-40% faster than using 
        # either im.mean() or np.mean(im).

        # Detect fade in from black.
        if frame_mean >= threshold and last_mean < threshold:
            print "Detected fade in at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )

        # Detect fade out to black.
        elif frame_mean < threshold and last_mean >= threshold:
            print "Detected fade out at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )

        last_mean = frame_mean      # Store current mean to compare in next iteration.

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

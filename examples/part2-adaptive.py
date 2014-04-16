# 
#      Scene Detection with Python and OpenCV - Example Program
# Part 2: Adaptive Fade Detection             By: Brandon Castellano
#
# http://www.bcastell.com/tech-articles/pyscenedetect-tutorial-part-2/
#
# This Python program implements a more advanced and optimized threshold-
# based scene detection algorithm, and improves the output format so
# the scene cuts can be more easily imported into other programs (e.g.
# ffmpeg, mkvmerge). Usage:
#
#   > python part2-adaptive.py [video] [intensity] [min %] [blocksize]
#
# Where [video] is a path to the video to be parsed, [intensity] is the
# pixel intensity from 0 to 255 to be used as a cut-off (default 16),
# [min %] is the minimum percent of pixels in the frame from 0 to 100
# that must fall under the threshold (default 90%), and [blocksize] is
# the amount of rows in the image to check at once (default 32, can be
# changed/tuned to optimize performance).  Example:
#
#   > python part2-adaptive.py testvideo.mp4 16 90 32
#
# Note that you must specify all options, unless you want to use the
# above default values, in which case simply specify [video]:
#
#   > python part2-adaptive.py testvideo.mp4
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

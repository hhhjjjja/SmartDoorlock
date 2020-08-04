#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import time
import Adafruit_SSD1306   # This is the driver chip for the Adafruit PiOLED

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import jetson.inference
import jetson.utils

import argparse
import sys

import RPi.GPIO as GPIO


cnt = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)


# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.imageNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="googlenet", help="pre-trained model to load (see below for options)")
parser.add_argument("--camera", type=str, default="0", help="index of the MIPI CSI camera to use (e.g. CSI camera 0)\nor for VL42 cameras, the /dev/video device to use.\nby default, MIPI CSI camera 0 will be used.")
parser.add_argument("--width", type=int, default=1280, help="desired width of camera stream (default is 1280 pixels)")
parser.add_argument("--height", type=int, default=720, help="desired height of camera stream (default is 720 pixels)")
parser.add_argument('--headless', action='store_true', default=(), help="run without display")

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)



# 128x64 display with hardware I2C:

# setting gpio to 1 is hack to avoid platform detection

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)

 

# Initialize library.

disp.begin()

 

# Clear display.

disp.clear()

disp.display()

 

# Create blank image for drawing.

# Make sure to create image with mode '1' for 1-bit color.

width = disp.width

height = disp.height

image = Image.new('1', (width, height))

 

# Get drawing object to draw on image.

draw = ImageDraw.Draw(image)

 

# Draw a black filled box to clear the image.

draw.rectangle((0, 0, width, height), outline=0, fill=0)

 

# Draw some shapes.

# First define some constants to allow easy resizing of shapes.

padding = -2

top = padding

bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.

x = 0

 

# Load default font.

font_led = ImageFont.load_default()




# load the recognition network
net = jetson.inference.imageNet(opt.network, sys.argv)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
font = jetson.utils.cudaFont()

# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	# classify the image
	class_id, confidence = net.Classify(img)

	# find the object description
	class_desc = net.GetClassDesc(class_id)

	# overlay the result on the image	
	font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)


	if net.GetClassDesc(class_id) == "three" :
		cnt = cnt+1

		if cnt > 100 :
			GPIO.output(12, True)
			GPIO.output(18, False)
			
			# Draw a black filled box to clear the image.
			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			draw.text((x,16), "Unlock", font=font_led, fill=255)

			# Display image.
			# Set the SSD1306 image to the PIL image we have made, then dispaly
			disp.image(image)
			disp.display()

			time.sleep(1.0)
			
			print("unlock")
			break
	else :
		cnt = 0
		GPIO.output(12, False)
		GPIO.output(18, True)





	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

	# print out performance info
	net.PrintProfilerTimes()

	#LED initial (12 : LOW, 18 : HIGH)
	GPIO.output(12, False)	#Lock - red on/ yellow off
	GPIO.output(18, True)

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break




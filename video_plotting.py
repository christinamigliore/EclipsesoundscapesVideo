"""
PURPOSE
-------
	This module calculates the average RGB (red, green, blue) pixel
	and the average x intensities for every x position and the average 
	y intensities for every y position for every frame and plots them
	with the different functions.
"""
from moviepy.editor import *
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import seaborn as sns

import video_analysis as va

def RGB_line_plot(filename):
	"""
	PURPOSE
	--------

		Function calculates the average RGB pixel hues for every frame 
		and plots a line plot.
		>>> RGB_line_plot('filename.mov')

	PARAMETERS
	------------

	    filename:
	      The name of the video file. Moviepy uses ffmpeg which supports the 
	      video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	RETURNS
	--------
		
		A saved RGB line plot to the directory where this code is stored.
	"""
	red_array, green_array, blue_array = va.find_RGB_Hues(filename, save=False, fps=1)
	time = np.arange(0, len(red_array))
	plt.plot(time, red_array, label='R', color='r')
	plt.plot(time, green_array, label='G', color='g')
	plt.plot(time, blue_array, label='B', color='b')
	plt.title("Plot of RGB Hues for One Frame")
	plt.xlabel("Time (Seconds)")
	plt.ylabel("RGB Hue")
	plt.legend()
	plt.savefig("RGB_plot_"+filename[0:-4])

def RGB_bar_plot(filename):
	"""
	PURPOSE
	--------

		Function calculates the average RGB (red, green, blue) pixel
		hues for every frame and plots a bar plot.
		>>> RGB_bar_plot('filename.mov')

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	    	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	RETURNS
	--------
		
		A saved RGB bar plot to the directory where this code is stored.

	"""
	red_array, green_array, blue_array = va.find_RGB_Hues(filename, save=False, fps=1)
	time = np.arange(0, len(red_array))
	plt.subplot(3, 1, 1)
	plt.bar(time, red_array, color='r')
	plt.title("Average RGB Color for Each Frame of Video")
	plt.subplot(3, 1, 2)
	plt.bar(time, green_array, color='g')
	plt.ylabel("Color Hue")
	plt.subplot(3, 1, 3)
	plt.bar(time, blue_array, color='b')
	plt.xlabel("Time (sec)")
	plt.savefig("RGB_barplot_"+filename[0:-4])

def RGB_animation(filename, height, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average RGB (red, green, blue) pixel
		hues for every frame and saves an animation of the RGB line plot.
		>>> RGB_animation('filename.mov', 1500)

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.
		
		height: 
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved RGB line plot animation to the directory where this code is stored.

	"""
	red_array, green_array, blue_array = va.find_RGB_Hues(filename, save=False, fps=1)
	x = np.arange(0, len(red_array))
	y = red_array
	y1 = green_array
	y2 = blue_array
	max_val_r = np.max(red_array)
	max_val_g = np.max(green_array)
	max_val_b = np.max(blue_array)

	axis_font = {'fontname':'Arial', 'size':'30'}
	fig, ax = plt.subplots()
	line1, = ax.plot(x, y, color='r', lw=10, label='red')
	line2, = ax.plot(x, y1, color='g', lw=10, label='green')
	line3, = ax.plot(x, y2, color='b', lw=10, label='blue')

	DPI = fig.get_dpi()
	fig.set_size_inches(height/float(DPI), width/float(DPI))

	line = [line1, line2, line3]
	ax.set_xlabel("Time (seconds)", **axis_font)
	ax.set_ylabel("RGB Hue", **axis_font)
	ax.set_title("Average RGB Hue per Second",**axis_font)
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(25)

	plt.tight_layout()
	def update(num, x, y, y1, y2, line):
		line[0].set_data(x[:num], y[:num])
		line[1].set_data(x[:num], y1[:num])
		line[2].set_data(x[:num], y2[:num])
		line[0].axes.axis([0, x[-1] , 0, max_val_r+10])
		line[1].axes.axis([0, x[-1] , 0, max_val_g+10])
		line[2].axes.axis([0, x[-1] , 0, max_val_b+10])
		return line

	ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, y1, y2, line],
                              interval=950, blit=True, repeat=False)
	ani.save("RGB_animation_"+filename[0:-4]+".mp4", fps=1)

def y_line_animation(filename, height, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average y intensities for every y position 
		for every frame and saves an animation of the y intensities per frame.
		>>> y_line_animation('filename.mov', 1500)

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.
		
		height: 
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved y line plot animation to the directory where this code is stored.

	"""
	y_total_array = va.find_xy_intensities(filename, save=False, fps=1)[1]
	fig, ax = plt.subplots()
	y = np.arange(0, len(y_total_array[0]))
	line, = ax.plot(y, y_total_array[0])
	axis_font = {'fontname':'Arial', 'size':'18'}
	ax.set_xlabel("Y Position", **axis_font)
	ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
	ax.set_title("Average Intensity per Second",**axis_font)
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(15)

	DPI = fig.get_dpi()
	fig.set_size_inches(height/float(DPI), width/float(DPI))

	plt.tight_layout()

	def animate(i):
	    line.set_ydata(y_total_array[i])  # update the data
	    return line,

	# Init only required for blitting to give a clean slate.
	def init():
		line.set_ydata(np.ma.array(y, mask=True))
		line.axes.axis([0, y[-1] , 0, 255])
		return line,

	ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y_total_array)), init_func=init,
                              interval=960, blit=True, repeat=False)
	ani.save("y_line_animation_"+filename[0:-4]+".mp4", fps=1)

def x_line_animation(filename, height, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average x intensities for every x position 
		for every frame and saves an animation of the x intensities per frame.
		>>> x_line_animation('filename.mov', 1500)

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.
		
		height: 
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved y line plot animation to the directory where this code is stored.

	"""
	x_total_array = va.find_xy_intensities(filename, save=False, fps=1)[0]
	fig, ax = plt.subplots()
	x = np.arange(0, len(x_total_array[0]))
	line, = ax.plot(x, x_total_array[0])
	axis_font = {'fontname':'Arial', 'size':'18'}
	ax.set_xlabel("X Position", **axis_font)
	ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
	ax.set_title("Average Intensity per Second",**axis_font)
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(15)

	DPI = fig.get_dpi()
	fig.set_size_inches(height/float(DPI), width/float(DPI))

	plt.tight_layout()

	def animate(i):
	    line.set_ydata(x_total_array[i])  # update the data
	    return line,

	# Init only required for blitting to give a clean slate.
	def init():
		line.set_ydata(np.ma.array(x, mask=True))
		line.axes.axis([0, x[-1] , 0, 255])
		return line,

	ani = animation.FuncAnimation(fig, animate, np.arange(1, len(x_total_array)), init_func=init,
                              interval=960, blit=True, repeat=False)
	ani.save("x_line_animation_"+filename[0:-4]+".mp4", fps=1)

def y_bar_animation(filename, height, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average y intensities for every y position 
		for every frame and saves an animation of the y intensities per frame 
		barplots.
		>>> y_bar_animation('filename.mov', 1500)

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.
		
		height: 
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved y line bar animation to the directory where this code is stored.

	"""
	y_total_array = va.find_xy_intensities(filename, save=False, fps=1)[1]
	fig, ax = plt.subplots()

	y = np.arange(0, len(y_total_array[0]))
	barcollection = plt.bar(y, y_total_array[0], width=1, edgecolor = "none")

	axis_font = {'fontname':'Arial', 'size':'18'}
	ax.set_xlabel("Y Position", **axis_font)
	ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
	ax.set_title("Average Intensity per Second",**axis_font)
	ax.set_xlim([0, y[-1]])
	ax.set_ylim([0, 255])

	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(15)

	DPI = fig.get_dpi()
	fig.set_size_inches(height/float(DPI), width/float(DPI))

	plt.tight_layout()

	def animate(i):
		x = y_total_array[i]
		for i, b in enumerate(barcollection):
			b.set_height(x[i])

	ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y_total_array)),
                              interval=960, blit=False, repeat=False)
	ani.save("y_bar_animation_"+filename[0:-4]+".mp4", fps=1)

def x_bar_animation(filename, height, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average x intensities for every x position 
		for every frame and saves an animation of the x intensities per frame 
		barplots.
		>>> x_bar_animation('filename.mov', 1500)

	PARAMETERS
	------------

	    filename:
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.
		
		height: 
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved x line bar animation to the directory where this code is stored.

	"""
	x_total_array = va.find_xy_intensities(filename, save=False, fps=1)[0]
	fig, ax = plt.subplots()

	x = np.arange(0, len(x_total_array[0]))
	barcollection = plt.bar(x, x_total_array[0], width=1, edgecolor = "none")

	axis_font = {'fontname':'Arial', 'size':'18'}
	ax.set_xlabel("X Position", **axis_font)
	ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
	ax.set_title("Average Intensity per Second",**axis_font)
	ax.set_xlim([0, x[-1]])
	ax.set_ylim([0, 255])

	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(15)

	DPI = fig.get_dpi()
	fig.set_size_inches(height/float(DPI), width/float(DPI))

	plt.tight_layout()

	def animate(i):
		y = x_total_array[i]
		for i, b in enumerate(barcollection):
			b.set_height(y[i])

	ani = animation.FuncAnimation(fig, animate, np.arange(1, len(x_total_array)),
                              interval=960, blit=False, repeat=False)
	ani.save("x_bar_animation_"+filename[0:-4]+".mp4", fps=1)

def radius_animation(filename, radius, compressed=False, compress=5, height=1500, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average pixel for every degree, 0
		to 360, as a function of specified radii.
		>>> radius_animation('filename.mov', 1000)

	PARAMETERS
	------------

	    filename: string
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    compressed: boolean (optional)
			If true, then the data is compressed to desired amount.

		compress: integer (optional)
			If compressed is true, then the data will be compressed by this amount.
		
		height: integer (optional)
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: integer (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: integer (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved radial animation to the directory where this code is stored.

	"""
	if compressed == True:
		intensity_tot = va.find_radius_intensity_compressed(filename, radius, compress, fps)
	else:
		intensity_tot = va.find_radius_intensity(filename, radius, fps)

    fig, ax = plt.subplots()
    
    p = np.arange(1, 350)
    barcollection = plt.bar(p, intensity_tot[0], width=1, edgecolor = "none")
    
    axis_font = {'fontname':'Arial', 'size':'18'}
    ax.set_xlabel("Position from Center", **axis_font)
    ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
    ax.set_title("Average Intensity per Second as a Function of Radial Distance",**axis_font)
    ax.set_ylim([0, 255])
    ax.set_xlim([1, radius])
    
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(15)
    
    plt.tight_layout()

    DPI = fig.get_dpi()
    fig.set_size_inches(height/float(DPI), width/float(DPI))
    
    def animate(i):
        y = intensity_tot[i]
        for i, b in enumerate(barcollection):
            b.set_height(y[i])
    
    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(intensity_tot)),
                              interval=960, blit=False, repeat=False)
    ani.save("radial_"+filename[0:-4]+".mp4", fps=1)

def angle_animation(filename, radius, compressed=False, compress=2, height=900, width=400, fps=1):
	"""
	PURPOSE
	--------

		Function calculates the average pixel value over specified radius 
		as a function of degrees, 0 to 360.
		>>> angle_animation('filename.mov', 1000)

	PARAMETERS
	------------

	    filename: string
	    	The name of the video file. Moviepy uses ffmpeg which supports the 
	     	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    compressed: boolean (optional)
			If true, then the data is compressed to desired amount.

		compress: integer (optional)
			If compressed is true, then the data will be compressed by this amount.
		
		height: integer (optional)
			The saved animation height in pixels. Useful when combining video
			and animation together into one video.

		width: integer (optional)
			The saved animation width in pixels. Useful when combining video
			and animation together into one video. Default is set to 400 pixels,
			which gives a very narrow plot.

		fps: integer (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	RETURNS
	--------
		
		A saved angular animation to the directory where this code is stored.

	"""
	if compressed == True:
		intensity_tot_angle = va.find_angle_intensity_compressed(filename, radius, compress, fps)
	else:
		intensity_tot_angle = va.find_angle_intensity(filename, radius, fps)

    fig, ax = plt.subplots()
    
    p = np.arange(0, 360)
    barcollection = plt.bar(p, intensity_tot_angle[0], width=1, edgecolor = "none")
    
    axis_font = {'fontname':'Arial', 'size':'18'}
    ax.set_xlabel("Angle (Degrees)", **axis_font)
    ax.set_ylabel("Intensity (RGB Hue)", **axis_font)
    ax.set_title("Average Intensity per Second as a Function of Angular Distance",**axis_font)
    ax.set_ylim([0, 255])
    ax.set_xlim([0, 360])
    
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(15)
    
    plt.tight_layout()

    DPI = fig.get_dpi()
    fig.set_size_inches(height/float(DPI), width/float(DPI))
    
    def animate(i):
        y = intensity_tot_angle[i]
        for i, b in enumerate(barcollection):
            b.set_height(y[i])
    
    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(intensity_tot_angle)),
                              interval=960, blit=False, repeat=False)
    ani.save("angular_"+filename[0:-4]+".mp4", fps=1)
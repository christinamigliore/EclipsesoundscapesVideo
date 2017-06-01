"""
Purpose
-------
	This module calculates and saves the animations for the RGB, x and y intensities
	positions, radial and angular intensities of the inputted eclipse video.
	It is used with the module: video_plotting. 
"""
from moviepy.editor import *
import numpy as np
import datetime
import progressbar
import time
import cv2

def find_center_circle_pos(filename, fps=1):
	"""
	Purpose
	-------
		This function uses OpenCV to circle detect and save the most 
		prominent circle's center x and y positions.
		>>> find_center_circle_pos("filename.mov")

	Parameters
	----------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	Returns
	-------

		coords: array
			1D array of the each circle's center x and y positions for each frame.

	"""
	clip = VideoFileClip(filename)
	length = clip.duration
    bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
	frame_num = 0
	coords = []
	for frame in clip.iter_frames(fps):
		frame_num += 1
		time.sleep(0.1)
        bar.update(frame_num)

		cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,1000,
                                param1=30,param2=73)
		if circles != None:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(cimg,(i[0],i[1]),i[2],(255,255,255),2)
			coords.append([i[0],i[1]])
	return coords

def find_RGB_Hues(filename, save=True, fps=1):
	"""
	Purpose
	--------

		Function calculates the average RGB (red, green, blue) pixel
		hues for every frame.
		>>> red, green, blue = find_RGB_Hues('filename.mov', save=False)

	Parameters
	------------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    save: boolean (optional)
	      	If True, the red_array, green_array, and blue_array will be saved
	      	as a textfile to directory where this code is. Default is set to True.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	Returns
	--------

		red_array: array
			1D array of the average red pixel hue for each frame

		green_array: array
			1D array of the average green pixel hue for each frame

		blue_array: array
			1D array of the average blue pixel hue for each frame
	"""
	clip = VideoFileClip(filename)
	red_array = []
	green_array = []
	blue_array = []
	for frame in clip.iter_frames(fps=1):
		a = frame[:,:,:]
		b = a.mean(axis=0)
		RGB_values = b.mean(axis=0)
		average = RGB_values.mean(axis=0)
		red_array.append(RGB_values[0])
		green_array.append(RGB_values[1])
		blue_array.append(RGB_values[2])
	if save == True:
		np.savetxt("red_array_"+filename[0:-4], red_array, fmt='%1.4f')
		np.savetxt("green_array_"+filename[0:-4], green_array, fmt='%1.4f')
		np.savetxt("blue_array_"+filename[0:-4], blue_array, fmt='%1.4f')
	return red_array, green_array, blue_array

def find_xy_intensities(filename, save=True, fps=1):
	"""
	Purpose
	--------
		Function calculates the average x intensities for every x position
		and the average y intensities for every y position for every frame.
		>>> y_array = find_xy_intensities('filename.mp4')[1]

	Parameters
	------------

	    filename: string
	      The name of the video file. Moviepy uses ffmpeg which supports the 
	      video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    save: boolean (optional)
	      If True, the red_array, green_array, and blue_array will be saved
	      as a textfile to directory where this code is. Default is set to True.

	    fps: integer (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	Returns
	--------

		x_total_array: array
			2D array of  the average x intensities for every y position
			for each frame

		y_total_array: array
			2D array of the average y intensities for every x position
			for each frame

		x_position_array: array
			1D array of the x position values

		y_position_array: array
			1D array of the y position values
	"""
	time_start = datetime.datetime.now()
	clip = VideoFileClip(filename)
	length = clip.duration
	bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
	x_total_array = []
	y_total_array = []
	frame_num = 0
	for frame in clip.iter_frames(fps):
		y_array_one_frame = []
		x_array_one_frame = []
		y_len, x_len = frame[:,:,:].shape[0], frame[:,:,:].shape[1]
		for i in range(0, y_len):
			a = frame[i,:,:]
			b = a.mean(axis=0)
			c = b.mean(axis=0)
			y_array_one_frame.append(c)
		for j in range(0, x_len):
			d = frame[:, j, :]
			e = d.mean(axis=0)
			f = e.mean(axis=0)
			x_array_one_frame.append(f)
		y_total_array.append(y_array_one_frame)
		x_total_array.append(x_array_one_frame)
		frame_num += 1
		time.sleep(0.1)
		bar.update(frame_num)
	x_position_array = np.arange(0, len(x_total_array[0]))
	y_position_array = np.arange(0, len(y_total_array[0]))
	time_end = datetime.datetime.now()
	delta_time = (time_end - time_start).total_seconds()
	print "loop time: "+str(delta_time)
	if save == True:
		np.savetxt("x_array_"+filename[0:-4], x_total_array, fmt='%1.0f')
		np.savetxt("y_array_"+filename[0:-4], y_total_array, fmt='%1.0f')
	return x_total_array, y_total_array, x_position_array, y_position_array

def find_xy_intensities_compressed(filename, compress=4, save=True, fps=1):
	"""
	Purpose
	--------
		Function calculates the average x intensities for every x position
		and the average y intensities for every y position for every frame.
		>>> y_array = find_xy_intensities('filename.mp4')[1]

	Parameters
	------------

	    filename: string
	      The name of the video file. Moviepy uses ffmpeg which supports the 
	      video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    save: boolean (optional)
	      If True, the red_array, green_array, and blue_array will be saved
	      as a textfile to directory where this code is. Default is set to True.

	    fps: integer (optional)
	      The frames per second user wants to analysis video. Default is set to 1.

	Returns
	--------

		x_total_array: array
			2D array of  the average x intensities for every y position
			for each frame

		y_total_array: array
			2D array of the average y intensities for every x position
			for each frame

		x_position_array: array
			1D array of the x position values

		y_position_array: array
			1D array of the y position values
	"""
	clip = VideoFileClip(filename)
	length = clip.duration
	bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
	x_total_array = []
	y_total_array = []
	frame_num = 0
	for frame in clip.iter_frames(fps=1):
		y_array_one_frame = []
		x_array_one_frame = []
		y_len, x_len = frame[:,:,:].shape[0], frame[:,:,:].shape[1]
		for i in range(0, y_len):
			if i%compress == 0:
				a = frame[i,:,:]
				b = a.mean(axis=0)
				c = b.mean(axis=0)
				y_array_one_frame.append(c)
		for j in range(0, x_len):
			if j%compress == 0:
				d = frame[:, j, :]
				e = d.mean(axis=0)
				f = e.mean(axis=0)
				x_array_one_frame.append(f)
		y_total_array.append(y_array_one_frame)
		x_total_array.append(x_array_one_frame)
		frame_num += 1
		time.sleep(0.1)
		bar.update(frame_num)
	x_position_array = np.arange(0, len(x_total_array[0]))
	y_position_array = np.arange(0, len(y_total_array[0]))
	if save == True:
		np.savetxt("x_array_"+filename[0:-4], x_total_array, fmt='%1.0f')
		np.savetxt("y_array_"+filename[0:-4], y_total_array, fmt='%1.0f')
	return x_total_array, y_total_array, x_position_array, y_position_array

def find_angle_intensity(filename, radius, fps=1, save=False):
	"""
	Purpose
	--------
		Function calculates the light intensity average over a specified
		radius as a function of angle
		>>> intensity_tot_angle = find_angle_intensity('filename.mp4', coords, 1000)

	Parameters
	------------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	    save: boolean (optional)
	    	If True, the data array will be saved as a textfile to directory where 
	    	this code is. Default is set to False.

	Returns
	--------

		intensity_tot_angle: array
			2D array of the averaged radius light intensities as a function of
			angle.
	"""
    clip = VideoFileClip(filename)
    length = clip.duration
    bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
    frame_num = 0
    intensity_tot_angle = []
    coords = find_center_circle_pos(filename, fps=1)
    for frame in clip.iter_frames(fps=1):
        x = int(coords[frame_num][0])
        y = int(coords[frame_num][1])
        frame_intensity = []
        for i in range(0, 360):
            intensity = []
            degree = math.radians(i)
            for r in range(1, radius):
                x_new = x + int(r*math.cos(degree))
                y_new = y + int(r*math.sin(degree))
                if y_new >= clip.get_frame(0).shape[0]:
                    y_new = clip.get_frame(0).shape[0]-1
                data = frame[y_new,x_new,:]
                intensity_data = data.mean(axis=0)
                intensity.append(intensity_data)
            avg = sum(intensity)/len(intensity)
            frame_intensity.append(avg)
        intensity_tot_angle.append(frame_intensity)
        frame_num += 1
        time.sleep(0.1)
        bar.update(frame_num)
    if save == True:
		np.savetxt("angular"+filename[0:-4], intensity_tot_angle, fmt='%1.0f')
    return intensity_tot_angle

def find_radius_intensity(filename, radius, fps=1, save=False):
	"""
	Purpose
	--------
		Function calculates the light intensity average over angle 0 to 360
		as a function of radius
		>>> intensity_tot = find_radius_intensity('filename.mp4', coords, 1000)

	Parameters
	------------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	    save: boolean (optional)
	    	If True, the data array will be saved as a textfile to directory where 
	    	this code is. Default is set to False.

	Returns
	--------

		intensity_tot: array
			2D array of the averaged angle light intensities as a function of
			radius.
	"""
    clip = VideoFileClip(filename)
    length = clip.duration
    bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
    frame_num = 0
    intensity_tot = []
    coords = find_center_circle_pos(filename, fps=1)
    for frame in clip.iter_frames(fps=1):
        x = int(coords[frame_num][0])
        y = int(coords[frame_num][1])
        frame_intensity = []
        for r in range(1, radius):
            intensity = []
            for i in range(0, 360):
                degree = math.radians(i)
                x_new = x + int(r*math.cos(degree))
                y_new = y + int(r*math.sin(degree))
                if y_new >= clip.get_frame(0).shape[0]:
                    y_new = clip.get_frame(0).shape[0]-1
                data = frame[y_new,x_new,:]
                intensity_data = data.mean(axis=0)
                intensity.append(intensity_data)
            avg = sum(intensity)/len(intensity)
            frame_intensity.append(avg)
        intensity_tot.append(frame_intensity)
        frame_num += 1
        time.sleep(0.1)
        bar.update(frame_num)
    if save == True:
		np.savetxt("radial"+filename[0:-4], intensity_tot, fmt='%1.0f')
    return intensity_tot

def find_angle_intensity_compressed(filename, radius, compress=2, fps=1, save=False):
	"""
	Purpose
	--------
		Function calculates the light intensity average over a specified
		radius as a function of angle compressed to desired amount.
		>>> intensity_tot_angle = find_angle_intensity_compressed('filename.mp4', coords, 1000)

	Parameters
	------------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    compress: integer
	      	Number by which to compress the data.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	    save: boolean (optional)
	    	If True, the data array will be saved as a textfile to directory where 
	    	this code is. Default is set to False.

	Returns
	--------

		intensity_tot_angle: array
			2D array of the averaged radius light intensities as a function of
			angle.
	"""
    clip = VideoFileClip(filename)
    length = clip.duration
    bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
    frame_num = 0
    intensity_tot_angle = []
    coords = find_center_circle_pos(filename, fps=1)
    for frame in clip.iter_frames(fps=1):
        x = int(coords[frame_num][0])
        y = int(coords[frame_num][1])
        frame_intensity = []
        for i in range(0, 360):
            if i%compress == 0:
                intensity = []
                degree = math.radians(i)
                for r in range(1, radius):
                    x_new = x + int(r*math.cos(degree))
                    y_new = y + int(r*math.sin(degree))
                    if y_new >= clip.get_frame(0).shape[0]:
                        y_new = clip.get_frame(0).shape[0]-1
                    data = frame[y_new,x_new,:]
                    intensity_data = data.mean(axis=0)
                    intensity.append(intensity_data)
                avg = sum(intensity)/len(intensity)
                frame_intensity.append(avg)
        intensity_tot_angle.append(frame_intensity)
        frame_num += 1
        time.sleep(0.1)
        bar.update(frame_num)
    if save == True:
    	np.savetxt("angular"+filename[0:-4], intensity_tot_angle, fmt='%1.0f')
    return intensity_tot_angle

def find_radius_intensity_compressed(filename, radius, compress=5, fps=1, save=False):
	"""
	Purpose
	--------
		Function calculates the light intensity average over angle 0 to 360
		as a function of radius compressed to desired amount.
		>>> intensity_tot = find_radius_intensity_compressed('filename.mp4', coords, 1000)

	Parameters
	------------

	    filename: string
	      	The name of the video file. Moviepy uses ffmpeg which supports the 
	      	video extensions: .mp4, .mpeg, .avi, .mov, .gif.

	    radius: integer
	    	The maximum radius to calculate to, this is dependent on the radius
	    	of the eclipse.

	    compress: integer
	      	Number by which to compress the data.

	    fps: integer (optional)
	      	The frames per second user wants to analysis video. Default is set to 1.

	    save: boolean (optional)
	    	If True, the data array will be saved as a textfile to directory where 
	    	this code is. Default is set to False.

	Returns
	--------

		intensity_tot: array
			2D array of the averaged angle light intensities as a function of
			radius.
	"""
    clip = VideoFileClip(filename)
    length = clip.duration
    bar = progressbar.ProgressBar(max_value=int(length*fps)+1)
    frame_num = 0
    intensity_tot = []
    coords = find_center_circle_pos(filename, fps=1)
    for frame in clip.iter_frames(fps=1):
        x = int(coords[frame_num][0])
        y = int(coords[frame_num][1])
        frame_intensity = []
        for r in range(1, radius):
            if r%compress == 0:
                intensity = []
                for i in range(0, 360):
                    degree = math.radians(i)
                    x_new = x + int(r*math.cos(degree))
                    y_new = y + int(r*math.sin(degree))
                    if y_new >= clip.get_frame(0).shape[0]:
                        y_new = clip.get_frame(0).shape[0]-1
                    data = frame[y_new,x_new,:]
                    intensity_data = data.mean(axis=0)
                    intensity.append(intensity_data)
                avg = sum(intensity)/len(intensity)
                frame_intensity.append(avg)
        intensity_tot.append(frame_intensity)
        frame_num += 1
        time.sleep(0.1)
        bar.update(frame_num)
    if save == True:
		np.savetxt("radial"+filename[0:-4], intensity_tot, fmt='%1.0f')
    return intensity_tot
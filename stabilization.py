"""
PURPOSE:
--------
    The purpose of this code is to stabilize the imported 
    video. It is specifically designed for eclipse videos 
    to keep the ratio of the area of the eclipse and the 
    background the same. Additionally the region of interest
    box, radius, and center of the circle are saved in a text
    file called "circle_coords.txt"

INPUTS
------
    filename: string
        The name of the video file. Moviepy uses ffmpeg which supports the 
        video extensions: .mp4, .mpeg, .avi, .mov, .gif.

    out_filename: string
        The name of the output saved video file. Moviepy uses ffmpeg which 
        supports the video extensions: .mp4, .mpeg, .avi, .mov, .gif.

OUTPUTS
-------
    circle_coords: array
        1D array, [x position of center of circle, y position of center of circle,
        radius of detected circle].

    'out_filename.mp4': video
        Saved video of stabalized eclipse video.
"""
import cv2
import sys 
import numpy as np
import progressbar
import time

filename = sys.argv[1]
out_filename = sys.argv[2]

cap = cv2.VideoCapture(filename)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 1)
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
print "Frames per second: "+str(fps)
circle_coords = []
frame_num = 0
#fourcc = cv2.cv.CV_FOURCC(*'MJPG')
#out = cv2.VideoWriter(out_filename, fourcc, fps, (width, height))

number_of_frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

while(cap.isOpened()):

    ret, frame = cap.read()
    #frame = cv2.medianBlur(frame,5)

    if ret == True:
        cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,60,
                                param1=73,param2=73,minRadius=0,maxRadius=0)

        if circles != None: 
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                #i[0] = x coordinate of center
                #i[1] = y coordinate of center
                #i[2] = radius of detected circle
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(255,0,0),2)
                # draw the center of the circle
                #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
                radius = i[2]
                coord = [i[0], i[1], i[2]]
                circle_coords.append(coord)
        else:
            if len(circle_coords) == 0:
                coord = [680, 630, 280]
                radius = coord[2]
            else:
                coord = circle_coords[-1]
                radius = coord[2]
                circle_coords.append(coord)
        #cv2.line(frame, (coord[0], coord[1]), (coord[0]+350, coord[1]), (0,0,255), 8)

        frame_num += 1
        print frame_num
        #rect = cv2.rectangle(frame, (-1*radius-100+coord[0], -1*radius-100+coord[1]), (radius+100+coord[0], radius+100+coord[1]), (255,0,0))
        x = -1*radius-100+coord[0]
        y = -1*radius-100+coord[1]
        w = radius+100+coord[0]-(-1*radius-100+coord[0])
        h = radius+100+coord[1]-(-1*radius-100+coord[1])
        if y < 0:
            y = 0
        if x < 0:
            x = 0
        mask = np.zeros(frame.shape, np.uint8)
        mask[y:y+h,x:x+w] = frame[y:y+h,x:x+w]
        cv2.imshow("Eclipse Video", cimg)
    else:
        np.savetxt("circle_coords.txt", circle_coords)
        break

    #out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()
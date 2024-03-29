from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import subprocess

def videoToFrames(vidFile):
	fileList = []												    				    #init empty list to store file names and track order
	maxWidth = 160													    	    		#specify max width of resized frames
	global sourceFPS													    	    	#access global variable storing video FPS
	vidcap = cv2.VideoCapture(vidFile)										    	    #access the source video file
	sourceFPS = vidcap.get(cv2.CAP_PROP_FPS)				    				    	#determine the FPS of the video file
	success, image = vidcap.read()								    				    #read the first frame of the video
	count = 0														        			#initialize a counter to track frame numbers
	while success:														        		#while successfully reading frames
		width, height, _ = image.shape										        	#get the frame dimensions
		shrinkRatio = width/maxWidth											        #Get the ratio to shrink by to make it the max Width
		image = cv2.resize(image, (int(height/shrinkRatio), int(width/shrinkRatio)))	#resize the frame
		#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	    						#convert frame to greyscale
		cv2.imwrite("frame%d.jpg" % count, image)     		        					#save frame as JPEG file
		fileList.append("frame%d.jpg" % count)					        				#append filename to list
		success, image = vidcap.read()								        			#read the next frame
		print("Frame " + str(count) + " successfully read")				        		#print to console
		count += 1															        	#increment the counter
	return (fileList)

def generateFrameConversionData(imgPath):
    #Take a colour image
    #Take image, shrink and convert to colour and greyscale
    #Return list of tuple with ascii basey on gray value, and colour pix value for EACH pixel
    divisor = 3.642857142857143
    maxWidth = 160
    imgData = []
    #Dictionary to convert from Greyscale to ASCII characters
    greyscaleChars = {
		"70" : "$","69" : "@","68" : "B","67" : "%","66" : "8","65" : "&","64" : "W","63" : "M","62" : "#","61" : "*","60" : "o","59" : "a","58" : "h","57" : "k","56" : "b","55" : "d","54" : "p","53" : "q","52" : "w",
		"51" : "m","50" : "Z","49" : "O","48" : "0","47" : "Q","46" : "L","45" : "C","44" : "J","43" : "U","42" : "Y","41" : "X","40" : "z","39" : "c","38" : "v","37" : "u","36" : "n","35" : "x","34" : "r","33" : "j",
		"32" : "f","31" : "t","30" : "/","29" : "\\","28" : "|","27" : "(","26" : ")","25" : "1","24" : "{","23" : "}","22" : "[","21" : "]","20" : "?","19" : "-","18" : "_","17" : "+","16" : "~","15" : "<","14" : ">",
		"13" : "i","12" : "!","11" : "l","10" : "I","9" : ";","8" : ":","7" : ",","6" : "\"","5" : "^","4" : "`","3" : "'","2" : ".","1" :  " "	,"0" :  " "
        }
    #Dictionary to convert from Greyscale to ASCII characters reverse colour
    greyscaleCharsRev = {
        "0" : "$","1" : "@","2" : "B","3" : "%","4" : "8","5" : "&","6" : "W","7" : "M","8" : "#","9" : "*","10" : "o","11" : "a","12" : "h","13" : "k","14" : "b","15" : "d","16" : "p","17" : "q","18" : "w",
        "19" : "m","20" : "Z","21" : "O","22" : "0","23" : "Q","24" : "L","25" : "C","26" : "J","27" : "U","28" : "Y","29" : "X","30" : "z","31" : "c","32" : "v","33" : "u","34" : "n","35" : "x","36" : "r","37" : "j",
        "38" : "f","39" : "t","40" : "/","41" : "\\","42" : "|","43" : "(","44" : ")","45" : "1","46" : "{","47" : "}","48" : "[","49" : "]","50" : "?","51" : "-","52" : "_","53" : "+","54" : "~","55" : "<","56" : ">",
        "57" : "i","58" : "!","59" : "l","60" : "I","61" : ";","62" : ":","63" : ",","64" : "\"","65" : "^","66" : "`","67" : "'","68" : ".","69" :  " "	,"70" :  " "
        }
    
    img = Image.open(imgPath)
    img = img.convert("RGB")
    gImg = img.convert("L")
    size = gImg.size															#Get the size
    shrinkRatio = size[0]/maxWidth											    #Get the ratio to shring by to make it the max Width
    gImg = gImg.resize((int(size[0]/shrinkRatio), int(size[1]/shrinkRatio)))	#Resize the image
    img = img.resize((int(size[0]/shrinkRatio), int(size[1]/shrinkRatio)))	    #Resize the image
    size = gImg.size
    for y in range (0, size[1]):												#For every row
        for x in range (0, size[0]):											#For every column
            pix = gImg.getpixel((x, y))											#Get the pixel shade (0 - 255)
            pixColour = img.getpixel((x, y))                                    #Get the pixel colour
            #pix = brightnessAdjust(pix, brightnessAdjustment)					#adjust the brightness of the individual pixel
            pix = int(pix/divisor)											    #assign pixel shade to an ascii character
            asciiChar = greyscaleChars[str(pix)]						        #Create the output string
            imgData.append((asciiChar, pixColour))
        asciiChar = "\n"
        pixColour = (0, 0, 0)
        imgData.append((asciiChar, pixColour))
    print("Conversion data generated:\t" + imgPath)
    return (generateColourAsciiFrame(imgData, "a_" + imgPath))

def generateColourAsciiFrame(data, newFileName):
	global horiMultiplyer
	global vertMultiplyer
	x = 0
	y = 0
	stringData = ""
	stringList = []
	for s in data:
		s, _ = s
		stringData = stringData + s
		stringList = stringData.split("\n")
	horChars = len(stringList[0])
	vertChars = len(stringList) - 1                                         #Minus 1 because the last character is "\n"
	imgHeight = vertChars * vertMultiplyer
	imgWidth = horChars * horiMultiplyer
    #print("Row Length:\t" +  str(len(stringList[0])))
    #print("Total Rows:\t" + str(len(stringList)- 1))
	img = Image.new("RGB", (imgWidth, imgHeight))
	draw = ImageDraw.Draw(img)												#Crete a draw object
	#font = ImageFont.truetype("cour.ttf", 16)
	font = ImageFont.truetype("courbd.ttf", 16)
	for d in data:
		pix, col = d
		if pix == "\n":
			y = y + vertMultiplyer
			x = 0
		else:
			draw.text((x, y), str(pix), fill = col, font = font, align = "left")
			x = x + horiMultiplyer
	newWidth = int(imgWidth*0.5)
	newHeight = int(imgHeight*0.5)
	img = img.resize((newWidth,newHeight))
	img.save(newFileName)
	print("\tAscii Frame Generated:\t" + newFileName)
	return (newFileName)

def imagesToMovie(fileList, videoname):
    global sourceFPS
    frameRate = sourceFPS
    frame = cv2.imread(fileList[0])                             #Read the first frame to get the height and width
    height, width, layers = frame.shape
    video = cv2.VideoWriter(videoname, cv2.VideoWriter_fourcc(*'DIVX'), frameRate, (width, height))
    for f in fileList:
        frame = cv2.imread(f)
        video.write(frame)
        print(f + " Written to video")
    video.release()

def has_audio(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=nb_streams", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return (int(result.stdout) - 1)

def transferAudioBetweenVideos(vidSrc, vidDst):
	audioFileName = "srcAudio.mp3"																														#file name for audio export
	p = subprocess.Popen(["ffmpeg", "-i", vidSrc, "-ab", "160k", "-ac", "2", "-ar", "44100", "-vn", audioFileName], stdout = subprocess.PIPE)			#create process for extracting audio
	print (p.communicate())																																#print output

	p = subprocess.Popen(["ffmpeg", "-i", vidDst, "-i", audioFileName, "-codec", "copy", "-shortest", ("audio_" + vidDst)], stdout = subprocess.PIPE)	#overlay new audio file on video to temp video file
	print (p.communicate())																																#print output

	os.remove(vidDst)																																	#remove video with no audio
	os.remove(audioFileName)																															#remove temp audio file
	os.rename(("audio_" + vidDst), vidDst)


#BUILD FUNCTION TO SHRINK FRAMES BEFORE MOVIE GENERATION
#TAKES TOO MUCH MEMORY.....CREATE FRAMES and DATA ON THE FLY... DONT SAVE TO LIST
sampleString = "asdfgh[],/porut"

horiMultiplyer = 14												#Pixel width for a single character
vertMultiplyer = 14                                             #Pixel height for a single character
sourceFPS = 0

vidContent = []                                                 #List of file names ASCII content

srcVideo = input("Enter name of source video:\t")
dstVideo = input("Enter name for new ascii video:\t")

#Convert video to many frames
srcFrames = videoToFrames(srcVideo)

#For each frame, generate the conversion data
for frame in srcFrames:
    vidContent.append(generateFrameConversionData(frame))

#Generate all the ascii frames and put file names into a list
#counter = 0
#for frame in vidContent:
#    newFrames.append(generateColourAsciiFrame(frame, ("asciiFrame" + str(counter) + ".jpg")))
#    counter = counter + 1
print("************************************")
imagesToMovie(vidContent, dstVideo)
print("ImagesToMovie done\n************************************")
if has_audio(srcVideo) == 1:
	transferAudioBetweenVideos(srcVideo, dstVideo)
else:
	print("This video does not have audio")

for f in srcFrames:
    os.remove(f)
for f in vidContent:
    os.remove(f)
print('#----------------------------#\n\tCode Completed')

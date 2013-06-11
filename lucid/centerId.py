# coding utf8
# Python libary with opencv for detection on structural biology loops


__author__ = "Etienne Francois"
__contact__ = "etienne.francois:esrf.fr"
__copyright__ = "2013, ESRF"


import opencv
import cv
import numpy
import pyFAI.splitBBox
import pylab
import scipy.ndimage
from toolbox import displayCv,white_detect,erode,dilate,open_image,smooth,imgInfo2cvImage
import meshGen


#================================================================================#
#          									 #
#                      Pretreatment for loop centering                           #
#   										 #
#================================================================================#


#Launch pretreatment of the image and the loop detection
def find_loop(imgInfo,showVisuals=False,zoom=0,testingProc = False,faceFindProc = False):
    
    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint
    :param faceFindProc: For face finding procedure
    :type faceFindProc: Boolean
    :param testingProc: For testing procedure.
    :type testingProc: Boolean

    :returns: Return from loop detection (label,x,y). If it is a testing procedure, the return format is different (imageWidth, imageHeight, [loop detection function common return])

    """

    #Test what type of image data has been given as argument "imgInfo"
    img = open_image("reference.png") 
    if isinstance(imgInfo,numpy.ndarray):       
        #Treatment with a numpy array
        numimg = numpy.fromstring(img.convert("L").tostring(),"uint8").astype("float32")    
        numimg2 = imgInfo
        numimg.shape = img.size[1],img.size[0]
        c =  imgInfo.shape[0]//2,imgInfo.shape[1]//2

    elif isinstance(imgInfo,str):
        #Treatment with the path of the image
        img2 = open_image(imgInfo)
        numimg = numpy.fromstring(img.convert("L").tostring(),"uint8").astype("float32")
        numimg2 = numpy.fromstring(img2.convert("L").tostring(),"uint8").astype("float32")
        numimg.shape = img.size[1],img2.size[0]
        numimg2.shape = img2.size[1],img2.size[0]
        c =  img2.size[1]//2,img.size[0]//2

    else:
        #Lauch TypeError exception if none type of image data supported is given
        raise TypeError("Unsupported type : Image path (str) or numpyarray (numpy.ndarray) needed")

    #Azimutal integration
    d0,d1 = numpy.ogrid[:img.size[1],:img.size[0]]
    d0-=c[0]
    d1-=c[1]
    r=numpy.sqrt(d0**2+d1**2)
    theta = numpy.arctan2(d1,d0)
    dtheta = abs(scipy.ndimage.sobel(theta))
    I,e0,e1,w,u=pyFAI.splitBBox.histoBBox2d(pos0=r,delta_pos0=numpy.ones(numimg.size),bins=(64,4),weights=numimg, pos1=theta, delta_pos1=dtheta)
    Iflat = I.max(axis=0)
    flat = numpy.interp(r.ravel(), e0, Iflat)
    flat.shape=numimg2.shape
    res = (255-numimg2)/(255-flat)
    res2 = (255*(res.max()-res)/(res.max()-res.min())).clip(0,255).astype("uint8")

    #Choose between differents ways of launching. Priority order : Normal, Face finding, TestCase procedure.
    if testingProc == False and faceFindProc == False:
        if zoom>0:
            return loop_detection(numimg2.astype("uint8"),showVisuals,zoom)
        else:
            return loop_detection(res2,showVisuals,zoom)
    elif faceFindProc == True:
        return face_detection(res2,0,zoom)
    else:
        #TestCase procedure launcher : return format is different (imageWidth, imageHeight, [function common return])
        if zoom>0:
            return (img2.size[0],img2.size[1],loop_detection(numimg2.astype("uint8"),zoom=zoom))
        else:
            return (img2.size[0],img2.size[1],loop_detection(res2,zoom=zoom))


# Explicit launcher for face finding with pretreatment of the image and the face detection
def find_face(imgInfo,showVisuals=False,zoom=0):
    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: Return from loop detection.

    """
    return find_loop(imgInfo,showVisuals=showVisuals,zoom=zoom,faceFindProc=True)


#================================================================================#
#          									 #
#                      Center identifier procedure                               #
#   										 #
#================================================================================#


#Detection of loops in image
def loop_detection(imgInfo,showVisuals=False,zoom=0):

    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: (label,x,y) result from loop_detection function

    """
    image=imgInfo2cvImage(imgInfo)
    image2=cv.CloneImage(image)

    #if zoom == 0:
    cv.AdaptiveThreshold(image2,image2,255,cv.CV_ADAPTIVE_THRESH_MEAN_C,cv.CV_THRESH_BINARY_INV,45,6)
    #else:
        #cv.Threshold(image2,image2,30,255,cv.CV_THRESH_BINARY)

    image3=cv.CloneImage(image2)
    cv.Zero(image3)
    storage = cv.CreateMemStorage()
    contours = cv.FindContours(cv.CloneImage    
    (image2),storage,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE,(0,0))

    cv.DrawContours(image3,contours,cv.RGB(255,255,255),cv.RGB (255,255,255),2,cv.CV_FILLED)
    cv.Smooth(image3,image3,cv.CV_MEDIAN,11)
    
    image4 = cv.CloneImage(image3)

    #check if the loop is in the image
    count = white_detect(image4[10:image4.height-10,10:image4.width-10])
    if count < 50:
        return ("No loop detected",-1,-1)
    
    #dilation and erosion if there is no zoom
    if zoom == 0:
        erode(image4,image4,11)
        dilate(image4,image4,11)

    count = white_detect(image4[10:image4.height-10,10:image4.width-10])
    if count < 50:
        (xcenter,ycenter) = find_approx_loop(image3)
        if showVisuals==1:
            cv.Line(image,(int(xcenter),int(0)),(int(xcenter),int(image.height)),cv.RGB(120.0,120.0,120.0))
            cv.Line(image,(int(0),int(ycenter)),(int(image.width),int(ycenter)),cv.RGB(120.0,120.0,120.0))
            displayCv(('Resultat',image),('ErosionDilation',image4),('AdaptiveThresh',image2),('FinalTreatmentVisualisation',image3))
            cv.WaitKey(0)
        return ('ApproxCoord',xcenter-15,ycenter)
    if zoom == 0:
        (xcenter,ycenter) = only_robot(image3)
        if xcenter > 0:
            if showVisuals:
                cv.Line(image,(int(xcenter),int(0)),(int(xcenter),int(image.height)),cv.RGB(120.0,120.0,120.0))
    	        cv.Line(image,(int(0),int(ycenter)),(int(image.width),int(ycenter)),cv.RGB(120.0,120.0,120.0))
                displayCv(('Resultat',image),('ErosionDilation',image4),('AdaptiveThresh',image2),('FinalTreatmentVisualisation',image3))
            return ("ArmRobot",xcenter,ycenter)
    clean_the_robot(image3,image4)
    adjust_detection(image3)
    if zoom == 0:
        (xcenter,ycenter) = calculate_center(image3,image3)
    else:
        (xcenter,ycenter) = calculate_center(image3,image3)
    if showVisuals:
        cv.Line(image,(int(xcenter),int(0)),(int(xcenter),int(image.height)),cv.RGB(120.0,120.0,120.0))
        cv.Line(image,(int(0),int(ycenter)),(int(image.width),int(ycenter)),cv.RGB(120.0,120.0,120.0))  
        displayCv(('Resultat',image),('ErosionDilation',image4),('AdaptiveThresh',image2),('FinalTreatmentVisualisation',image3))
        cv.WaitKey(0)
    return ("Coord",xcenter,ycenter)

#Detection of loop with the meshing systeme
def find_loop_mesh(imgInfo,showVisuals=False,zoom=0,virtCenter=(-1,-1)):
    
    """|
    
    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint
    :param virtCenter: A virtual center if reqal center use is not wanted
    :type virtCenter: Tuple (uint,uint)

    :returns: (label,x,y) result from loop_detection function

    """
    if showVisuals:
        (x,y,x2,y2),imageClone,image3,store,virtCenter = meshGen.generate_meshing_info(imgInfo,method=meshGen.LUCID_CENTER_PROC,showVisuals=showVisuals,zoom=zoom,virtCenter=virtCenter)
        cv.Rectangle(imageClone,(x,y),(x2,y2),cv.Scalar( 120, 120, 120 ))
    else:
        (x,y,x2,y2),image3 = meshGen.generate_meshing_info(imgInfo,method=meshGen.LUCID_CENTER_PROC,showVisuals=showVisuals,zoom=zoom,virtCenter=virtCenter)
   
    xres = x2-((x2-x)//2)
    yrestemp = -1
    yrestemp2 = -1
    yres = 0
    while y<y2 and (yrestemp < 0 or yrestemp2 < 0):
        y+=1
        y2-=1
        if image3[y,xres]>0:
            yrestemp = y
        if image3[y2,xres]>0:
            yrestemp2 = y2
    if y>=y2:
        yres = y2-((y2-y)//2)
    else:
        yres = yrestemp2 - ((yrestemp2-yrestemp)//2)
    if showVisuals:
        for num in range(len(store)):
             cv.Line( image3, virtCenter, store[num],cv.Scalar( 120, 120, 120 ),2,8 );
	cv.Line( imageClone, (xres-3,yres-3), (xres+3,yres+3),cv.Scalar( 120, 120, 120 ),2,8 );
	cv.Line( imageClone, (xres-3,yres+3), (xres+3,yres-3),cv.Scalar( 120, 120, 120 ),2,8 );

        cv.Line( imageClone, (virtCenter[0],virtCenter[1]-3), (virtCenter[0],virtCenter[1]+3),cv.Scalar( 120, 120, 120 ),2,8 );
	cv.Line( imageClone, (virtCenter[0]-3,virtCenter[1]), (virtCenter[0]+3,virtCenter[1]),cv.Scalar( 120, 120, 120 ),2,8 );
        #real center
        cv.Line( imageClone, ((659//2),(463//2)-15), ((659//2),(463//2)+15),cv.Scalar( 120, 120, 120 ),2,8 );
        cv.Line( imageClone, ((659//2)-15,(463//2)), ((659//2)+15,(463//2)),cv.Scalar( 120, 120, 120 ),2,8 );

        displayCv(('Resultat',imageClone),('RaysVisu',image3))
	cv.WaitKey(0)
    return "meshing",xres,yres
    
#Detection of degrees for the face's loop in image
def face_detection(imgInfo,showVisuals=False,zoom=0):
    
    """|
    
    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: (label,x,y) result from loop_detection function

    """ 

    image=imgInfo2cvImage(imgInfo)

    image2=cv.CloneImage(image)
    if zoom == 0:
        cv.AdaptiveThreshold(image2,image2,255,cv.CV_ADAPTIVE_THRESH_MEAN_C,cv.CV_THRESH_BINARY_INV,45,6)
    else:
        cv.AdaptiveThreshold(image2,image2,255,cv.CV_ADAPTIVE_THRESH_MEAN_C,cv.CV_THRESH_BINARY_INV,121,6)

    image3=cv.CloneImage(image2)
    cv.Zero(image3)

    storage = cv.CreateMemStorage()
    contours = cv.FindContours(cv.CloneImage    
    (image2),storage,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE,(0,0))

    cv.DrawContours(image3,contours,cv.RGB(255,255,255),cv.RGB (255,255,255),2,cv.CV_FILLED)
    cv.Smooth(image3,image3,cv.CV_MEDIAN,11)
    
    image4 = cv.CloneImage(image3)

    if zoom == 0:
        erode(image4,image4,9)
        dilate(image4,image4,9)
    else:
        erode(image4,image4,25)
        dilate(image4,image4,25)


    count = white_detect(image4)

    if showVisuals:  
        displayCv(('Resultat',image),('ErosionDilation',image4),('AdaptiveThresh',image2),('FinalTreatmentVisualisation',image3))
        cv.WaitKey(0)
    return count

#Clean the robot part and keep just the loop
def clean_the_robot(image,imageMask):
    """|
    
    :param image : The image to modify
    :type image : IplImage
    :param imageMask : Image with morphological mathematic too clear the robot part
    :type imageMask : IplImage

    """
    i=imageMask.width-1
    wbegin=0
    while i>=1:
        if white_detect(imageMask[:,i])>0:
            wbegin = 1
        else:
            if wbegin==1:
                cv.Set(image[:,0:i],0)
                return i
        i=i-1
    cv.Set(image[:,0:1],0)
    return -1

#Calculate the center of the loop with the threated image
def calculate_center(image,imageMask=None):
    """|

    :param image: treated image with just the loop for finding center
    :type image: IplImage

    :returns: Coordinates from the center in pixels (x,y)
    """
    i=0
    left=-1
    right=-1
    up=-1
    down=-1
    if imageMask is None:
        imageMask = image
    while i<imageMask.width:
        if white_detect(imageMask[:,i])>0:
              left = i
              break
        i=i+1

    while i<imageMask.width:
        if white_detect(imageMask[:,i])==0:
              right = i-1
              break
        i=i+1

    if right == -1:
        return (-1,-1)

    horizoncenter=right-round((right-left)/2.9)
    j=3
    
    while j<image.height:
        if image[j,horizoncenter]>0:
              up = j
              break
        j=j+1

    h=image.height-3
    while h>j:
        if image[h,horizoncenter]>0:
              down = h
              break
        h=h-1
    
    if down == -1:
        return (-2,-2)

    verticalcenter = down - round((down-up)/2)
    
    return (horizoncenter,verticalcenter)

#Approximate best coordinates for incomplete loops
def find_approx_loop(image):
    """|
    
    :param image : B/W Image with which is used for the approx
    :type image : IplImage
  
    """
    i=image.width-1
    while i>=0:
        if white_detect(image[:,i])>0:
            j=image.height-1
            while j>=0:
                if image[j,i]>0:
                    if white_detect(image[j-6:j+6,i-6:i+6])>17:
                        return i,j
                j=j-1
        i=i-1
    return -1,-1

#Search if it's only the robot arm on the image and if it is, give better coordinates
def only_robot(image3):
    """|

    :param image3 : B/W Image with which it is used
    :type image3 : IplImage

    """
    xcenter=image3.width
    ycenter=-1
    i=image3.height-1

    firstWhite = -1
    lastWhite = -1
    firstWhite2 = -1
    lastWhite2 = -1

    maxWhite=0
    while i>=0:
        count=white_detect(image3[i,:])
        if count>0:
            if firstWhite<0:
                firstWhite=i
            else:
                if lastWhite>0:
                    if firstWhite2<0:
                        firstWhite2=i
            if count>maxWhite:
                maxWhite=count
        else:
            if firstWhite>0:
                if lastWhite<0:
                    lastWhite=i+1
                else:
                    if firstWhite2>0:
                        if lastWhite2<0:
                            lastWhite2=i+1            
        i=i-1

    if maxWhite < (image3.width*90)//100:
        return (-1,-1)

    if firstWhite2==0 or (firstWhite2>0 and lastWhite2<0):
        lastWhite2=0
    if firstWhite==0 or (firstWhite>0 and lastWhite<0):
        lastWhite=0

    mid = (firstWhite+lastWhite)//2
    mid2 = (firstWhite2+lastWhite2)//2
    if mid2 <0:
        if mid > image3.height//2:
            ycenter = (mid+image3.height)//2
        else:
            ycenter = mid//2
    else:
        ycenter=(mid+mid2)//2

    return (xcenter,ycenter)


def adjust_detection(image):
    """|

    :param image : B/W Image with which it is used
    :type image : IplImage

    """
    max_loop_white=0    
    i=image.width-1
    while i>=0:
        up = -1
        down = -1
        j=0
        while j<image.height:
            if image[j,i]>0:
                up = j
                break
            j=j+1

        h=image.height-3
        while h>j:
            if image[h,i]>0:
              down = h
              break
            h=h-1
        if((down-up<max_loop_white-round(max_loop_white*0.20)) and down-up>0):
            #cv.Line(image,(int(i),int(0)),(int(i),int(image.height)),cv.RGB(120.0,120.0,120.0))        
            break
        if(down-up>max_loop_white):
            max_loop_white = down-up
        i=i-1
    while i>=0:
        up = -1
        down = -1
        j=0
        while j<image.height:
            if image[j,i]>0:
                up = j
                break
            j=j+1

        h=image.height-3
        while h>j:
            if image[h,i]>0:
              down = h
              break
            h=h-1
        if(down-up>max_loop_white):
            #cv.Line(image,(int(i),int(0)),(int(i),int(image.height)),cv.RGB(120.0,120.0,120.0))  
            return cv.Set(image[:,0:i],0)
        i=i-1
    return -1,-1

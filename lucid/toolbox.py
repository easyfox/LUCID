# coding utf8
#Python libary with opencv for detection on structural biology loops


__author__ = "Etienne Francois"
__contact__ = "etienne.francois:esrf.fr"
__copyright__ = "2013, ESRF"


import cv
import os
import Image
import numpy
import math


#================================================================================#
#          									 #
#                    Python, python libraries, os functions                      #
#   										 #
#================================================================================#


#Open an image from disk
def open_image(filename):
    return Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))

#Convert degrees to radian
def toRadians(degrees):
    return degrees * ((2 * math.pi) / 360)


#================================================================================#
#          									 #
#                           OpenCv linked functions                              #
#   										 #
#================================================================================#


#Convert disponible image information into an IplImage
def imgInfo2cvImage(imgInfo):
    """|

    :param imgInfo: Image or part of image
    :type imgInfo: String or Numpy array

    :returns: OpenCV IplImage

    """
    #Test what type of image data has been given as argument "imgInfo"
    if isinstance(imgInfo,numpy.ndarray):
        return cv.GetImage(cv.fromarray(imgInfo))
    elif isinstance(imgInfo,str):
        return cv.LoadImage(imgInfo,cv.CV_LOAD_IMAGE_GRAYSCALE)
    else:
        raise TypeError("Unsupported type : Image path (str) or numpyarray (numpy.ndarray) needed") 

#Display fonction for cvImage
def displayCv(*tupleDisplayable):
    """|

    :param *tupleDisplayable: Displayable tuples
    :type *tupleDisplayable: Multiples arguments : Tuples : (\"Window's name\",[cvImage])


    """
    for tp in list(tupleDisplayable):
        if isinstance(tp,tuple):
            try:
                cv.NamedWindow(tp[0], cv.CV_WINDOW_AUTOSIZE)
                cv.ShowImage(tp[0],tp[1])
                continue
            except Exception:
                print "An error occurs on displaying cv visuals. Please check your tuples in input. Format : (\"WindowName\",CvImage)"
                return None

#Detection of white pixel in a binary image (0/255)
def white_detect(cvImg):
    """|

    :param cvImg: Image or part of image
    :type cvImg: OpenCV IplImage or part of OpenCV IplImage (image[:,0:150] for example)

    :returns: The numbers of white pixels in b/w image

    """
    return (cv.Sum(cvImg))[0]/255

#Morphological mathematic erosion function with num for how many times the file might be treated
def erode(src,dest,num):
    """|
    
    :param src : Input image
    :type src : IplImage
    :param dest : Output image
    :type dest : IplImage
    :param num : How much time erosion have to be applied >0
    :type num : uint

    """
    i=0
    fich = cv.CloneImage(src)
    while i<num-1:
        cv.Erode(fich,fich)
        i = i+1
    cv.Erode(fich,dest)

#Morphological mathematic dilatation function with num for how many times the file might be treated
def dilate(src,dest,num):
    """|
    
    :param src : Input image
    :type src : IplImage
    :param dest : Output image
    :type dest : IplImage
    :param num : How much time dilatation have to be applied >0
    :type num : uint

    """
    i=0
    fich = cv.CloneImage(src)
    while i<num-1:
        cv.Dilate(fich,fich)
        i = i+1
    cv.Dilate(fich,dest)

#Smooth application on image with num for how many times the file might be treated
def smooth(src,dest,num):
    """|
    
    :param _src: Input image
    :type _src: IplImage
    :param _dest: Output image
    :type _dest: IplImage
    :param _num: How much time gaussian blur have to be applied >0
    :type _num: uint

    :returns: Output image

    """
    i=0
    fich = cv.CloneImage(src)
    while i<num-1:
        cv.Smooth(fich,fich)
        i = i+1
    cv.Smooth(fich,dest)
    return dest

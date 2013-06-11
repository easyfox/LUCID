Centering functions
===================

.. automodule:: lucid

    find_loop
    =========

    Launch detection with the pretreatment algorithm and a numpy array as input image
    
    The pretreat algorithm does a first work on the original image to light up the background and improve the recognition process. Blabla.

    .. autofunction:: lucid.find_loop

    find_loop_byimg
    ===============
    
    Launch detection with the pretreatment algorithm and a path for input image

    Pretreament algorithm explanations are available in find_loop function

    .. autofunction:: lucid.find_loop_byimg

    find_loop_byimg_testlauncher
    ============================
    
    Special launch for unittests

    .. autofunction:: lucid.find_loop_byimg_testlauncher

    loop_detection_array
    ====================

    Lauch detection of the loop with an array

    Convert numpy array to an IplImage (Opencv format) and lauch loop_detection


    .. autofunction:: lucid.loop_detection_array

    loop_detection_path
    ===================

    `Lauch detection of the loop with the image path`

    Load the image into an IplImage (Opencv format) and launch loop_detection
    
    |    

    .. autofunction:: lucid.loop_detection_path
    
    loop_detection
    ==============

    `Detection of loops in image`

    |

    The first treatment consist in a threshold amd a binarisation with local mean. The size of the windows is 45x45 pixels and the tolerence which is taken is six gray level difference. In fact, a window of 45x45 around the treated pixel is got. The mean of the gray levels of the area is calculated and it's give us the local average of gray level.  If the pixel gray level is lower (because we want to have the loop in white) at nearly 6 gray level than the local average of gray level in his area, then it become white, else black.

    It can be illustrate by the formula : 

    |formule|

    .. |formule| image:: images/adaptivethres.png
              :align: middle

    In pratice, with a image we obtain something like :

    .. figure:: presentation/base.png
          :align: center
          :height: 300
          :figclass: floatleft
          
          Input image

    .. figure:: presentation/afterthresh.png
          :align: center
          :height: 300

          Output image

    On exemple in the output image, the loop and some noise can be seen. First, delete the noise is needed. For this task, a median filter is used. It will be passed several time because more noise can appear in the image.

    |

    .. autofunction:: lucid.loop_detection

    

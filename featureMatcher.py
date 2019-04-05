import numpy
import cv2
from PIL import Image,ImageTk

from errorMessage import *

###############################################################################
# Image Matching
###############################################################################
class featureMatcher():
    def __init__(self,scannedImg, storedImg):
        self.scannedImg=scannedImg
        self.storedImg=storedImg

    def matchTemplate(self):

        img = self.scannedImg
        template = self.storedImg

        w, h = template.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = cv2.TM_CCOEFF_NORMED  # ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


        # Apply template Matching
        res = cv2.matchTemplate(img, template, methods)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        detectedImg = cv2.rectangle(img, top_left, bottom_right, (0, 255, 255), 2)

        return detectedImg



    def match_images(self):
        """Given two images, returns the matches"""
        sift_obj = cv2.xfeatures2d.SIFT_create() #SIFT object
        kp_matcher = cv2.BFMatcher(cv2.NORM_L2) #Basic brute-force matcher object

        matchedTemplate=self.matchTemplate()
        self.scannedImg=matchedTemplate
        """Detect keypoints"""
        kp1, desc1 = sift_obj.detectAndCompute(self.scannedImg, None)
        kp2, desc2 = sift_obj.detectAndCompute(self.storedImg, None)
        # print 'scannedImg - %d features, storedImg - %d features' % (len(kp1), len(kp2))

        """From the detected matches return the k number of best matches"""
        raw_matches = kp_matcher.knnMatch(desc1, trainDescriptors=desc2, k=2)  # 2
        kp_pairs = self.filter_matches(kp1, kp2, raw_matches)
        print "Facial"+str(len(kp_pairs))
        return kp_pairs


    def filter_matches(self,kp1, kp2, matches, ratio=0.75):
        """Further reduce the number of matches found based on ratio comparison"""
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append(kp1[m.queryIdx])
                mkp2.append(kp2[m.trainIdx])
        kp_pairs = zip(mkp1, mkp2)

        return kp_pairs


    ###############################################################################
    # Match Diplaying
    ###############################################################################

    def display_matches( self, kp_pairs, status=None, H=None):

        h1, w1 = self.scannedImg.shape[:2]#get image height,width
        h2, w2 = self.storedImg.shape[:2]
        vis = numpy.zeros((max(h1, h2), w1 + w2), numpy.uint8)#Return a new array of given shape and type, filled with zeros in unit8
        vis[:h1, :w1] = self.scannedImg
        print vis
        vis[:h2, w1:w1 + w2] = self.storedImg
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

        if H is not None:
            corners = numpy.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = numpy.int32(cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
            cv2.polylines(vis, [corners], True, (255, 255, 255))

        if status is None:
            status = numpy.ones(len(kp_pairs), numpy.bool_)
        p1 = numpy.int32([kpp[0].pt for kpp in kp_pairs])
        p2 = numpy.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)

        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)
        kp_color = (51, 103, 236)
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if inlier:
                col = kp_color
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2, y2), 2, col, -1)
            else:
                pass
        vis0 = vis.copy()
        # Rearrang the color channel
        b, g, r = cv2.split(vis)
        img = cv2.merge((r, g, b))

        # Convert the Image object into a TkPhoto object
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk


    def draw_matches(self,kp_pairs):
        """Draws the matches for """
        mkp1, mkp2 = zip(*kp_pairs)

        p1 = numpy.float32([kp.pt for kp in mkp1])
        p2 = numpy.float32([kp.pt for kp in mkp2])

        if len(kp_pairs) >= 100:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            # print '%d / %d  inliers/matched' % (numpy.sum(status), len(status))
        else:
            H, status = None, None
            #print '%d matches found, not enough for homography estimation' % len(p1)


        if len(p1):
            display_img=self.display_matches(kp_pairs, status, H)
            return display_img


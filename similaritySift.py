import cv2
import numpy as np

import math

'''
im = cv2.imread("redditImages/1.jpg")
bgr_planes = cv2.split(im)
hist_size = 256
histRange = (0,256)
accumulate = False

b_hist = cv2.calcHist(bgr_planes, [0], None, [hist_size], histRange, accumulate=accumulate)
g_hist = cv2.calcHist(bgr_planes, [1], None, [hist_size], histRange, accumulate=accumulate)
r_hist = cv2.calcHist(bgr_planes, [2], None, [hist_size], histRange, accumulate=accumulate)

hist_w = 512
hist_h = 400
bin_w = int(round( hist_w/hist_size ))
histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

cv2.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
cv2.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
cv2.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

for i in range(1, hist_size):
    cv2.line(histImage, ( bin_w*(i-1), hist_h - int(np.ceil(b_hist[i-1])) ),
            ( bin_w*(i), hist_h - int(np.ceil(b_hist[i])) ),
            ( 255, 0, 0), thickness=2)
    cv2.line(histImage, ( bin_w*(i-1), hist_h - int(np.ceil(g_hist[i-1])) ),
            ( bin_w*(i), hist_h - int(np.ceil(g_hist[i])) ),
            ( 0, 255, 0), thickness=2)
    cv2.line(histImage, ( bin_w*(i-1), hist_h - int(np.ceil(r_hist[i-1])) ),
            ( bin_w*(i), hist_h - int(np.ceil(r_hist[i])) ),
            ( 0, 0, 255), thickness=2)

cv2.imshow('Source image', im)
cv2.imshow('calcHist Demo', histImage)
cv2.waitKey()
'''
# templateImg is a list of images
def similarityScore(myImg, templateImg):
    best_scores = []
    best_images = []
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(myImg, None)


    for ind,im in enumerate(templateImg):
        print(ind)
        im = cv2.resize(im, (500,500))
        kp_2, desc_2 = sift.detectAndCompute(im, None)
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(desc_1, desc_2, k=2)
        good_points = []
        ratio = 0.8
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good_points.append(m)
        result = cv2.drawMatches(myImg, kp_1, im, kp_2, good_points, None)

        # Define how similar they are
        number_keypoints = 0
        if len(kp_1) <= len(kp_2):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)
        print("Keypoints 1ST Image: " + str(len(kp_1)))
        print("Keypoints 2ND Image: " + str(len(kp_2)))
        result = len(good_points) / number_keypoints
        if len(best_scores) < 3:
            best_scores.append(result)
            best_images.append(im)
        else:
            best = [index for index,notArray in enumerate(best_scores) if notArray == max(best_scores)]

            if result > max(best_scores):
                best_scores[best[0]] = result
                best_images[best[0]] = im

    for k in range(len(best_images)):
        best_images[k] = cv2.resize(best_images[k], (500,500))


    myImg = cv2.resize(myImg, (500, 500))
    cv2.imshow('Source image', myImg)
    cv2.imshow('Sorted in no order', np.hstack((best_images[0], best_images[1], best_images[2])))
    print(f"{best_scores[0]*100}, {best_scores[1]*100}, {best_scores[2]*100},")
    cv2.waitKey(0)
    mean_ = sum(best_scores)/3 * 100
    if mean_ < .001:
        print("Need a better picture")
    else:
        print("Nice Picture!")

    return mean_

imgs = []
for l in range(25):
    imgs.append(cv2.imread(f"redditImages/{l}.jpg"))
myImg = cv2.imread("mine.jpg")

print(similarityScore(myImg, imgs))
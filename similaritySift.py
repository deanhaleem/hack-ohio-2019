import cv2
import numpy as np

import math

# templateImg is a list of images
def SiftsimilarityScore(myImgPath, templateImgPath):
    myImg = cv2.imread(myImgPath)
    try:
        myImg = cv2.resize(myImg, (500, 500))
    except:
        print('empty')
    best_scores = []
    best_images = []
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(myImg, None)

    # iterate through template images
    for ind,im_path in enumerate(templateImgPath):
        # print(ind)
        
        im = cv2.imread(im_path)
        im = cv2.resize(im, (500, 500))

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
        #print("Keypoints 1ST Image: " + str(len(kp_1)))
        #print("Keypoints 2ND Image: " + str(len(kp_2)))
        result = len(good_points) / number_keypoints
        if len(best_scores) < 3:
            best_scores.append(result)
            best_images.append(im_path)
        else:
            worst = [index for index,notArray in enumerate(best_scores) if notArray == min(best_scores)]

            if result < min(best_scores):
                best_scores[worst[0]] = result
                best_images[worst[0]] = im_path

        # least to greatest
        for i,best_i in enumerate(best_scores):
            for j,best_j in enumerate(best_scores):
                if best_i < best_j:
                    best_scores[i], best_scores[j] = best_scores[j], best_scores[i]
                    best_images[i], best_images[j] = best_images[j], best_images[i]


    mean_ = sum(best_scores)/3
    

    return mean_, best_images, best_scores

# def show(myImgPath, best_images):
#     myImg = cv2.imread(myImgPath)
#     myImg = cv2.resize(myImg, (500,500))
#     bImgs = []
#     for l in best_images:
#         bImgs.append(cv2.resize(cv2.imread(l), (500,500)))

#     cv2.imshow("mine",myImg)
#     cv2.imshow("yours",np.hstack((bImgs[0], bImgs[1], bImgs[2])))
#     cv2.waitKey(0)


# imgs = []
# for l in range(25):
#     imgs.append(f"redditImages/{l}.jpg")
# myImg = "mine.jpg"
# mean_, best, best_scores = similarityScore(myImg, imgs)

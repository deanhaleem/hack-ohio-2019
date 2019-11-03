import cv2
import numpy as np
import math

# templateImg is a list of images
def similarityScore(myImg, templateImg):
    best_scores = []
    best_images = []
    histr = cv2.calcHist([myImg],[0],None,[256],[0,256])

    for im in templateImg:
        histg = cv2.calcHist([im], [0], None, [256], [0, 256])
        a = cv2.compareHist(histr, histg, cv2.HISTCMP_BHATTACHARYYA)

        if len(best_scores) < 3:
            best_scores.append(a)
            best_images.append(im)
        else:
            worst = [index for index,k in enumerate(best_scores) if k == min(best_scores)]

            if a < min(best_scores):
                best_scores[worst[0]] = a
                best_images[worst[0]] = im

    for k in range(len(best_images)):
        best_images[k] = cv2.resize(best_images[k], (500,500))


    myImg = cv2.resize(myImg, (500, 500))
    cv2.imshow('Source image', myImg)
    cv2.imshow('Sorted in no order', np.hstack((best_images[0], best_images[1], best_images[2])))
    print(f"{best_scores[0]}, {best_scores[1]}, {best_scores[2]},")
    cv2.waitKey(0)
    return sum(best_scores)/3

imgs = []
for l in range(25):
    imgs.append(cv2.imread(f"redditImages/{l}.jpg"))
myImg = cv2.imread("mine.jpg")

print(similarityScore(myImg, imgs))
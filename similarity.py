import cv2
import numpy as np

# templateImg is a list of images
def similarityScore(myImgP, templateImgPath):
    myImg = cv2.imread(myImgP)
    best_scores = []
    best_images = []
    histr = cv2.calcHist([myImg],[0],None,[256],[0,256])

    for imP in templateImgPath:
        im = cv2.imread(imP)
        histg = cv2.calcHist([im], [0], None, [256], [0, 256])
        a = cv2.compareHist(histr, histg, cv2.HISTCMP_BHATTACHARYYA)

        if len(best_scores) < 3:
            best_scores.append(a)
            best_images.append(imP)
        else:
            worst = [index for index,k in enumerate(best_scores) if k == max(best_scores)]

            if a < max(best_scores):
                best_scores[worst[0]] = a
                best_images[worst[0]] = imP

    # least to greatest
    for i, best_i in enumerate(best_scores):
        for j, best_j in enumerate(best_scores):
            if best_i > best_j:
                best_scores[i], best_scores[j] = best_scores[j], best_scores[i]
                best_images[i], best_images[j] = best_images[j], best_images[i]

    return sum(best_scores)/3, best_images, best_scores

def show(myImgPath, best_images):
    myImg = cv2.imread(myImgPath)
    myImg = cv2.resize(myImg, (500,500))
    bImgs = []
    for l in best_images:
        bImgs.append(cv2.resize(cv2.imread(l), (500,500)))

    cv2.imshow("mine",myImg)
    cv2.imshow("yours",np.hstack((bImgs[0], bImgs[1], bImgs[2])))
    cv2.waitKey(0)

'''
reddit = []
for l in range(25):
    reddit.append(f"redditImages/{l}.jpg")
m, b, b_s = similarityScore("mine.jpg", reddit)
show("mine.jpg", b)
print(m)
'''


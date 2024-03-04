import os
import cv2
import easyocr
import numpy as np
from PIL import Image

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def main(image_target):
    # Set image dimensions
    height = 450
    width = 450

    # Read input image
    img = cv2.imread(image_target + ".jpg")

    # Resize image for consistency
    img = cv2.resize(img, (width, height))

    # Preprocess the image for digit extraction
    imgThreshhold = preProcess(img)

    # Find contours in the preprocessed image
    contours, hierarchy = cv2.findContours(imgThreshhold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the biggest contour (assumed to be the Sudoku grid)
    biggest, maxArea = biggestContour(contours)

    # Reorder the corner points of the Sudoku grid
    biggest = reorder(biggest)

    # Perspective transformation to get a bird's-eye view of the Sudoku grid
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))

    # Split the warped image into individual cells
    boxes = splitBoxes(imgWarpColored)

    # Save each cell as a separate image for OCR
    saveCellImages(boxes, image_target)

    # Perform OCR on the saved cell images
    solved_puzzle = performOCR(image_target)

    return solved_puzzle


# Image preprocessing: convert to grayscale, apply Gaussian blur, and adaptive thresholding
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshhold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshhold


# Find the biggest contour in the image
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


# Reorder the corner points of the Sudoku grid
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


# Split the Sudoku grid into individual cells
def splitBoxes(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes


# Save each cell as a separate image for OCR
def saveCellImages(boxes, image_target):
    x = 0
    Supprimer_repertoire(os.getcwd() + "\\treating_1\\" + image_target)
    os.makedirs(os.getcwd() + "\\treating_1\\" + image_target)
    for box in boxes:
        imm = cv2.resize(box, (160, 160))
        imm = Image.fromarray(imm)
        imm.save(os.getcwd() + "\\treating_1\\" + image_target + "\\image_" + str(x) + ".jpeg")
        x += 1


# Perform OCR on the saved cell images
def performOCR(image_target):
    reader = easyocr.Reader(["fr"])
    M = []
    for i in range(81):
        path_image = os.getcwd() + "\\treating_1\\" + image_target + "\\image_" + str(i) + ".jpeg"
        image = Image.open(path_image)
        num = reader.readtext(image, detail=0, allowlist='0123456789')
        if num == []:
            M.append(0)
        else:
            M.append(int(num[0]))

    liste_final = []
    list_final_2 = []
    for i in range(81):
        liste_final.append(M[i])
        if len(liste_final) == 9:
            list_final_2.append(liste_final)
            liste_final = []

    solved_puzzle = solve(list_final_2)
    return solved_puzzle


# Remove directory if it exists
def Supprimer_repertoire(path_repertoire):
    import shutil
    try:
        shutil.rmtree(path_repertoire)
    except OSError as e:
        print("")
    else:
        print("Le répertoire est supprimé avec succès")


# Sudoku solver: backtracking algorithm
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False


# Check if a number is valid in a given position
def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


# Find empty cells in the Sudoku grid
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None


# Print the solved Sudoku puzzle
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" | ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


# Entry point of the program
if __name__ == "__main__":
    image_target = "sudoku_image"  # Change this to the name of your input image without the file extension
    solved_puzzle = main(image_target)
    print("Solved Sudoku Puzzle:")
    print_board(solved_puzzle)

# Project Title: Sudoku Solver Using Computer Vision and OCR

## Overview:
This project aims to develop a Python program capable of solving Sudoku puzzles from images. Sudoku is a popular puzzle game that involves filling a 9x9 grid with digits so that each row, each column, and each of the nine 3x3 subgrids contain all of the digits from 1 to 9. Leveraging computer vision techniques and optical character recognition (OCR), we can automate the process of solving Sudoku puzzles from images, demonstrating the integration of image processing, OCR, and algorithmic problem-solving techniques.

## Project Components:

### Image Preprocessing:
The input Sudoku puzzle image undergoes preprocessing to enhance its quality and prepare it for digit extraction. This includes converting the image to grayscale, applying Gaussian blurring to reduce noise, and adaptive thresholding to binarize the image.

### Digit Extraction with OCR:
After preprocessing, the Sudoku grid is segmented into individual cells, each containing a single digit. Optical character recognition (OCR) is then employed to recognize the digits within these cells. The OCR library used in this project is EasyOCR, which supports multiple languages and provides accurate text recognition.

### Sudoku Solver Algorithm:
Once the digits are extracted from the image, the Sudoku puzzle is solved using a backtracking algorithm. This algorithm recursively fills each empty cell with a digit from 1 to 9 and checks if the puzzle remains valid. If a valid solution is found, the algorithm returns True; otherwise, it backtracks and tries a different digit.

### Displaying the Solved Puzzle:
Finally, the solved Sudoku puzzle is printed to the console for visualization. The program iterates through the solved puzzle grid and displays each digit along with horizontal and vertical separators to represent the Sudoku grid structure.

## Project Implementation:

### Image Preprocessing: 
The `preProcess` function converts the input image to grayscale, applies Gaussian blur, and performs adaptive thresholding to prepare it for digit extraction.

### Digit Extraction with OCR:
The `splitBoxes` function segments the Sudoku grid into individual cells, which are then saved as separate images for OCR using the `saveCellImages` function. The EasyOCR library is utilized to perform OCR on these images and extract the digits.

### Sudoku Solver Algorithm:
The `solve` function implements a backtracking algorithm to solve the Sudoku puzzle. It recursively fills each empty cell with a digit and checks if the puzzle remains valid. If a valid solution is found, the algorithm returns True; otherwise, it backtracks and tries a different digit.

### Displaying the Solved Puzzle:
The `print_board` function prints the solved Sudoku puzzle to the console in a visually appealing format, with digits arranged in rows and columns and separators representing the grid structure.

## Conclusion:
This project demonstrates the use of computer vision and OCR techniques to solve Sudoku puzzles from images automatically. By leveraging image processing, OCR, and algorithmic problem-solving, we can efficiently solve Sudoku puzzles, showcasing the power of Python and its libraries for complex problem-solving tasks.

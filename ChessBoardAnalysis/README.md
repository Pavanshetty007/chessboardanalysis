# Chessboard Analyzer

The **Chessboard Analyzer** is a Python-based tool for detecting and annotating the black and white squares on a chessboard image. The tool allows the user to select four points on the chessboard, performs a homography transformation to correct the perspective, and counts the black and white squares.

## Features
- Allows the user to interactively select 4 points to define the chessboard region.
- Applies a homography transformation to straighten the chessboard.
- Automatically detects black and white squares using thresholding and grid analysis.
- Provides a visual annotation of the detected squares.
- Outputs the count of black and white squares.

---
## Approach

To solve the problem of detecting and annotating black and white squares on a chessboard, the following steps were implemented:

1. **Interactive Point Selection:**
   - A GUI allows the user to click and select four points defining the chessboard's corners. These points are used to create a bounding box for the board.

2. **Homography Transformation:**
   - The selected points are used to compute a homography matrix, which straightens the chessboard image by removing perspective distortion. 
   - The output of this step is a top-down, standardized view of the chessboard.

3. **Grid Division:**
   - The straightened image is divided into an 8x8 grid of squares, corresponding to the chessboard's layout.

4. **Thresholding and Color Detection:**
   - Each grid cell is analyzed to determine its color (black or white). This is achieved using average intensity values:
     - High intensity corresponds to a white square.
     - Low intensity corresponds to a black square.
   - Thresholding techniques are applied to ensure robust detection even in varying lighting conditions.

5. **Annotation:**
   - The detected squares are visually annotated on the output image, marking black and white squares distinctly.
   - The annotated image is saved to the specified output directory.

6. **Counting:**
   - The program calculates and displays the count of black and white squares detected on the chessboard.

This approach combines image processing techniques such as homography, thresholding, and grid analysis to achieve accurate detection and annotation of chessboard squares.

---
## Steps for Running the Program

### 1. Clone or Download the Project
Download the project files to your local machine and ensure all required files (Python script and images) are in the same directory.

### 2. Prepare Your Input Image
Ensure your input chessboard image:
- Is saved on your computer.
- Has sufficient contrast between black and white squares for proper detection.

### 3. Update the Python Script
In the script, locate the following line under the `if __name__ == "__main__":` block:

```python
image_path = r"C:\Users\pavan\Desktop\chess_testing_images\good_chess4.webp"
```
Replace the path with the full path to your input image. For example:
```python
image_path = r"C:\path\to\your\chessboard_image.jpg"
```
### 4. Run the Script
Run the Python script using any Python environment. For example:

```bash
python chessboard_analyzer.py
```
### 5. Select Points on the Image
- A window will open showing your input image.
- Select exactly 4 points by clicking on the corners of the chessboard in the following order:
- Top-left
- Top-right
- Bottom-left
- Bottom-right
- Press the q key once you've selected all 4 points.
### 6. View the Results
After selecting points, the script will:

- Straighten the chessboard using a perspective transformation.
- Detect and annotate the black and white squares.
- Display the annotated image.
- Save the annotated image to the specified output directory.
### 7. Check Output
The annotated image is saved to the following location:
```bash
C:\Users\pavan\Desktop\data_chess\result.png
```
The terminal will display the count of black and white squares.

## Example Workflow

### Input Image:
Before running the program, make sure your input image is well-prepared, like this example:

### Select Points:
A window will open, and you will be prompted to select four points (top-left, top-right, bottom-left, bottom-right). Use the mouse to click on these points in the image.

### Annotated Output:
Once you have selected the points and confirmed with the q key, the program will apply perspective transformation and display the annotated chessboard image, highlighting the black and white squares.

### Terminal Output:
After processing, the terminal will display the count of black and white squares.

```bash

Black squares detected: 32
White squares detected: 32
Annotated image saved to: C:\Users\pavan\Desktop\data_chess\result.png
```
## Directory Structure
Here is an example of how to organize the project:

```bash

ChessboardAnalyzer/
│
├── chessboard_analyzer.py   # Python script for processing
├── README.md                # Documentation (this file)
├── output/                  # Directory for documentation images
│   ├── annotated_example.jpg # Example output image
│
└── input_images/            # Directory for input chessboard images
    ├── good_chess4.jpg      # Example chessboard image
    └── another_chess.jpg    # Another example image
```

## Additional Notes
### Interactive Point Selection:
- Ensure you select the points carefully to avoid incorrect perspective transformations.
- If the wrong points are selected, restart the script and select the points again.
### Output Image Dimensions:
- By default, the output image is 400x400 pixels. You can adjust this size by modifying the width and height variables in the apply_homography() method.
### Handling Errors:
- If you encounter errors like "module not found," ensure the required libraries are installed.
- If points are not selected properly, ensure you're pressing q only after selecting exactly 4 points.
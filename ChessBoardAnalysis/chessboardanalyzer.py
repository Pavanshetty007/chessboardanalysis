import cv2
import numpy as np
import matplotlib.pyplot as plt
from config import PATH, PARAMETERS

class ChessboardAnalyzer:
    def __init__(self, image_path):
        """
        Initializes the ChessboardAnalyzer with the input image.

        Args:
            image_path (str): Path to the input chessboard image.
        """
        self.image_path = image_path
        self.image = cv2.imread(image_path)  # Load the input image
        self.temp_image = self.image.copy()  # Temporary copy for drawing points
        self.points = []  # List to store selected points

    def select_points(self):
        """
        Allows the user to select 4 points on the image by clicking on it.
        Points are collected via OpenCV's mouse callback.
        """
        def mouse_callback(event, x, y, flags, param):
            """
            Mouse callback function to collect points when the user clicks.
            """
            if event == cv2.EVENT_LBUTTONDOWN and len(self.points) < 4:
                self.points.append((x, y))
                print(f"Point selected: {x, y}")
                cv2.circle(self.temp_image, (x, y), 5, (0, 0, 255), -1)
                cv2.imshow("Select 4 Points", self.temp_image)

        # Display the image and set up the mouse callback
        cv2.imshow("Select 4 Points", self.temp_image)
        cv2.setMouseCallback("Select 4 Points", mouse_callback)

        print("Select 4 points on the image by clicking. Press 'q' after selecting.")
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") and len(self.points) == 4:
                break
            elif key == ord("q"):
                print(f"Please select 4 points. You have selected {len(self.points)} so far.")

        cv2.destroyAllWindows()

    @staticmethod
    def order_points(pts):
        """
        Orders the selected points in clockwise order: 
        top-left, top-right, bottom-left, bottom-right.

        Args:
            pts (list): List of 4 points (x, y).

        Returns:
            np.ndarray: Ordered points as a NumPy array.
        """
        sorted_pts = np.array(sorted(pts, key=lambda p: p[1]))  # Sort by y-coordinate (top to bottom)
        top_left, top_right = sorted(sorted_pts[:2], key=lambda p: p[0])  # Sort top row by x-coordinate
        bottom_left, bottom_right = sorted(sorted_pts[2:], key=lambda p: p[0])  # Sort bottom row by x-coordinate
        return np.array([top_left, top_right, bottom_left, bottom_right], dtype="float32")

    def apply_homography(self, src_points):
        """
        Applies a perspective transformation (homography) to the image.

        Args:
            src_points (np.ndarray): Source points selected on the image.

        Returns:
            np.ndarray: Warped image after perspective transformation.
        """
        width, height = PARAMETERS.HOMO_SHAPE # Desired output image dimensions
        dst_points = np.array([
            [0, 0], [width - 1, 0],
            [0, height - 1], [width - 1, height - 1]
        ], dtype="float32")

        # Compute the homography matrix
        homography_matrix, _ = cv2.findHomography(src_points, dst_points)

        # Warp the image
        warped_image = cv2.warpPerspective(self.image, homography_matrix, (width, height))
        return warped_image

    @staticmethod
    def detect_chessboard_boxes(image):
        """
        Detects and annotates black and white squares on the warped chessboard.

        Args:
            image (np.ndarray): Warped chessboard image.

        Returns:
            tuple: Annotated image, count of black squares, count of white squares.
        """
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray_equalized = clahe.apply(gray)

        # Apply Otsu's thresholding
        _, binary = cv2.threshold(gray_equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Grid dimensions (assuming an 8x8 chessboard)
        height, width = binary.shape
        grid_size = height // 8

        black_count, white_count = 0, 0
        grid_annotated_img = image.copy()

        # Loop through each grid cell
        for row in range(8):
            for col in range(8):
                y_start, y_end = row * grid_size, (row + 1) * grid_size
                x_start, x_end = col * grid_size, (col + 1) * grid_size
                square_roi = binary[y_start:y_end, x_start:x_end]

                # Calculate black pixel ratio
                black_pixels = np.sum(square_roi == 0)
                total_pixels = square_roi.size
                black_ratio = black_pixels / total_pixels

                # Classify as black or white
                if black_ratio > 0.5:
                    black_count += 1
                    color = (0, 0, 255)  # Red for black squares
                else:
                    white_count += 1
                    color = (0, 255, 0)  # Green for white squares

                # Draw the grid square
                cv2.rectangle(grid_annotated_img, (x_start, y_start), (x_end, y_end), color, 2)

        return grid_annotated_img, black_count, white_count

    def run(self):
        """
        Executes the complete chessboard analysis workflow: 
        point selection, homography, and square detection.
        """
        # Step 1: Select points
        self.select_points()

        # Step 2: Order the selected points
        src_points = self.order_points(self.points)

        # Step 3: Apply homography
        warped_image = self.apply_homography(src_points)

        # Step 4: Detect and annotate chessboard squares
        annotated_image, black_count, white_count = self.detect_chessboard_boxes(warped_image)

        # Step 5: Display and save results
        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
        plt.title("Annotated Chessboard Grid")
        plt.axis("off")
        plt.show()

        # Save the annotated image
        cv2.imwrite(PATH.OUTPUT_DIR, annotated_image)

        print(f"Black squares detected: {black_count}")
        print(f"White squares detected: {white_count}")
        print(f"Annotated image saved to: {PATH.OUTPUT_DIR}")


import cv2 as cv
import os
import logging
from datetime import datetime

# Configure logging
log_filename = f"image_annotation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Initialize global variables
drawing = False  # True if the mouse is being dragged
mode = True  # If True, draw rectangle; press 'm' to toggle to circle
ix, iy = -1, -1  # Initial mouse click coordinates
rectangles = []  # List to store all drawn rectangles

# Mouse callback function
def draw_annotation(event, x, y, flags, param):
    global ix, iy, drawing, mode, rectangles, img

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y  # Record the starting point

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img.copy()  # Use a temporary image for dynamic drawing
            if mode:
                cv.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv.circle(temp_img, (x, y), 5, (0, 0, 255), 2)
            cv.imshow('image', temp_img)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            # Finalize rectangle and save its coordinates
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
            rectangles.append(((ix, iy), (x, y)))  # Store rectangle coordinates
        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), 2)
        cv.imshow('image', img)


def crop_and_save(image, rectangles):
    # Check if the image is loaded correctly
    if image is None or image.size == 0:
        logging.error("The input image is empty or not loaded correctly.")
        return

    logging.info(f"Image dimensions: {image.shape}")

    for i, ((x1, y1), (x2, y2)) in enumerate(rectangles):
        try:
            # Ensure coordinates are sorted and valid
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            # print(f"Cropping rectangle {i+1}: {(x1, y1), (x2, y2)}")
            if x2 > x1 and y2 > y1 and x1 >= 0 and y1 >= 0 and x2 <= image.shape[1] and y2 <= image.shape[0]:
                # Crop the region
                cropped_img = image[y1:y2, x1:x2]
                # print(f"Cropped region size: {cropped_img.shape if cropped_img.size > 0 else 'Empty'}")
                logging.info(f"Cropped region size for rectangle {i + 1}: {cropped_img.shape if cropped_img.size > 0 else 'Empty'}")

                # Save the cropped image
                filename = f"cropped_region_{i+1}.jpg"
                if cv.imwrite(filename, cropped_img):
                    # print(f"Saved: {filename}")
                    logging.info(f"Successfully saved: {filename}")
                else:
                    # print(f"Failed to save: {filename}")
                    logging.error(f"Failed to save: {filename}")
            else:
                # print(f"Invalid rectangle coordinates: {(x1, y1), (x2, y2)}. Please re-annotate this rectangle.")
                logging.warning(f"Invalid rectangle coordinates: {(x1, y1), (x2, y2)}. Please re-annotate this rectangle.")
        except Exception as e:
            # print(f"An error occurred while processing rectangle {i+1}: {e}")
            logging.error(f"An error occurred while processing rectangle {i + 1}: {e}")
            # print(f"Please re-annotate rectangle {i+1}.")
            logging.error(f"An error occurred while processing rectangle {i + 1}: {e}")

if __name__ == "__main__":
    # Load the image
    img_path="data\img2.jpg"
    img = cv.imread(img_path)

    # Extract the original image name without extension
    original_image_name = os.path.splitext(os.path.basename(img_path))[0]
    # print(original_image_name)
    logging.info(f"Loaded image from {img_path}")

    # Check if the image was loaded successfully
    if img is None:
        raise FileNotFoundError("Image not found. Please check the file path.")

    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_annotation)

    while True:
        cv.imshow('image', img)
        cv.putText(img, 'Choose top left corner, and drag,?', (10, 10), cv.FONT_HERSHEY_SIMPLEX, 0.2, (255, 0, 0), 1)

        k = cv.waitKey(1) & 0xFF
        if k == ord('m'):  # Toggle between rectangle and circle drawing
            mode = not mode
        elif k == 13:  # Press 'Enter' to exit and save rectangles
            break

    # Save the cropped rectangles
    if rectangles:
        crop_and_save(img, rectangles)


    cv.destroyAllWindows()

import cv2
import numpy as np
import os


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute width
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = int(max(widthA, widthB))

    # compute height
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def process_image(input_path, output_path):
    # 1. Load and convert to grayscale
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error reading {input_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Edge detection and contour finding for document warp
    edged = cv2.Canny(gray, 75, 200)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    warped = gray  # default fallback

    if contours:
        doc_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(doc_contour) < 1000:
            print(f"Discarded tiny contour in {os.path.basename(input_path)}")
        else:
            peri = cv2.arcLength(doc_contour, True)
            approx = cv2.approxPolyDP(doc_contour, 0.02 * peri, True)

            if len(approx) == 4:
                warped = four_point_transform(gray, approx.reshape(4, 2))
                print(f"Applied perspective warp on {os.path.basename(input_path)}")
            else:
                print(f"Found contour but not 4 points in {os.path.basename(input_path)}")
    else:
        print(f"No contours found in {os.path.basename(input_path)}")

    # 3. Mild CLAHE (prevent over‑boosting shadows)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(warped)

    # 4. Adaptive threshold (patch‑wise)
    binary = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,  # block size (odd, 11–21 typical)
        9    # C: subtracted constant (3–10 typical)
    )

    # 5. Remove small noise using connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    min_area = 10  # tune: 5–20 depending on text size
    cleaned = np.zeros_like(binary)
    for label in range(1, num_labels):  # skip background (label 0)
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= min_area:
            cleaned[labels == label] = 255

    # Optional: light morphology (remove any remaining tiny specks)
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    # cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)  # optional

    # 6. Save
    cv2.imwrite(output_path, cleaned)
    print(f"Processed: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")


# --- Main execution ---
if __name__ == "__main__":
    input_dir = "./images"
    output_dir = "./fixed"

    os.makedirs(output_dir, exist_ok=True)

    extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(extensions):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, f"fixed_{filename}")
            process_image(input_file, output_file)

    print("Batch processing complete.")

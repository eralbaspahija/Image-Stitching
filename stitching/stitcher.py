import cv2
import numpy as np
from pathlib import Path

class PanoramaStitcher:
    def __init__(self, images_folder):
        self.images_folder = images_folder
        self.images = []
        self.load_images()

    def load_images(self):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []

        for ext in valid_extensions:
            image_files.extend(Path(self.images_folder).glob(f'*{ext}'))
            image_files.extend(Path(self.images_folder).glob(f'*{ext.upper()}'))

        image_files = sorted(set(image_files))

        for img_path in image_files:
            img = cv2.imread(str(img_path))
            if img is not None:
                self.images.append(img)

    def stitch(self):
        if len(self.images) < 2:
            return None, "Require at least two images to stitch"

        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        status, panorama = stitcher.stitch(self.images)

        if status != cv2.Stitcher_OK:
            return None, "Stitching failed"

        panorama = self.crop_black_borders(panorama)
        return panorama, None

    def crop_black_borders(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = gray > 0
        coords = np.column_stack(np.where(mask))

        if coords.size == 0:
            return img

        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)

        cropped = img[y_min:y_max+1, x_min:x_max+1]

        def trim(im, axis, threshold=0.98):
            while im.shape[axis] > 0:
                line = im[0] if axis == 0 else im[:, 0]
                if (line > 0).mean() >= threshold:
                    break
                im = im[1:] if axis == 0 else im[:, 1:]
            return im

        cropped = trim(cropped, 0)
        cropped = trim(cropped[::-1], 0)[::-1]
        cropped = trim(cropped, 1)
        cropped = trim(cropped[:, ::-1], 1)[:, ::-1]

        return cropped

import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog
from matplotlib import pyplot as plt

class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing App")

        self.label = Label(master, text="Загрузите изображение для обработки")
        self.label.pack()

        self.load_button = Button(master, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        self.process_button = Button(master, text="Обработать изображение", command=self.process_image, state='disabled')
        self.process_button.pack()

        self.image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.label.config(text="Изображение загружено. Нажмите 'Обработать изображение'")
            self.process_button.config(state='normal')

    def linear_contrast(self, image, alpha=1.0, beta=0):
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    def histogram_equalization(self, image):
        return cv2.equalizeHist(image)

    def display_images(self, original, contrasted, equalized):
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        plt.imshow(original, cmap='gray')
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(contrasted, cmap='gray')
        plt.title('Contrasted Image')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(equalized, cmap='gray')
        plt.title('Equalized Image')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    def process_image(self):
        if self.image is not None:
            contrasted_image = self.linear_contrast(self.image, alpha=1.5, beta=0)
            equalized_image = self.histogram_equalization(self.image)
            self.display_images(self.image, contrasted_image, equalized_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
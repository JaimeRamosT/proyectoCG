import numpy as np
import cv2
import matplotlib.pyplot as plt

def display_results(resized_image, input_mask, input_image, output_image):
    plt.figure(figsize=(17, 8))
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis('off')
    plt.subplot(1, 4, 2)
    plt.imshow(input_mask.squeeze(), cmap='gray')
    plt.title("Mask")
    plt.axis('off')
    plt.subplot(1, 4, 3)
    plt.imshow((input_image.squeeze() * 255).astype(np.uint8))
    plt.title("Masked Image")
    plt.axis('off')
    plt.subplot(1, 4, 4)
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.title("Output")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
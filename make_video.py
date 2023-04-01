import cv2
import os

# Prompt the user for the directory containing the images
img_dir = input("Enter the directory containing the images: ")

# Set the output video file name and frame rate
out_file = "output_video.mp4"
fps = 30

# Get the dimensions of the first image
img_path = os.path.join(img_dir, os.listdir(img_dir)[0])
img = cv2.imread(img_path)
height, width, channels = img.shape

# Create the video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(out_file, fourcc, fps, (width, height))

# Loop through the images and add them to the video
for img_name in sorted(os.listdir(img_dir)):
    img_path = os.path.join(img_dir, img_name)
    img = cv2.imread(img_path)
    out.write(img)

# Release the video writer object and close the video file
out.release()


import os
from PIL import Image, ImageOps

def resize_with_padding(input_path, output_path, expected_size=(1024, 1024)):
    img = Image.open(input_path)
    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    new_img = ImageOps.expand(img, padding)
    # Save the new image
    new_img.save(output_path)

def process_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resize_with_padding(input_path, output_path)
            print(f"Processed and saved: {output_path}")

input_directory = "C:/Users/Om Naik/Downloads/images_to_use/"
output_directory = "C:/Users/Om Naik/Downloads/mages_to2/"

process_images(input_directory, output_directory)

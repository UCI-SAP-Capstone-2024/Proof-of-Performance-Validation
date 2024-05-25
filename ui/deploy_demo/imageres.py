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


# def resize_and_pad_image(input_path, output_path, size=(1024, 1024)):
#     image = Image.open(input_path)
    
#     # Resize image to fit within the specified size while maintaining aspect ratio
#     image.resize(size, Image.LANCZOS)
    
#     # Create a new image with the specified size and white background
#     new_image = Image.new("RGB", size, (255, 255, 255))
    
#     # Calculate position to paste the resized image onto the new image
#     paste_x = (size[0] - image.size[0]) // 2
#     paste_y = (size[1] - image.size[1]) // 2
    
#     # Paste the resized image onto the new image
#     new_image.paste(image, (paste_x, paste_y))
    
#     # Save the new image
#     new_image.save(output_path)

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

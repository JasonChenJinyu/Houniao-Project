from PIL import Image
import numpy as np

def get_pixel_rgb(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Ensure the image is 8x8
    img = img.resize((8, 8))
    
    # Convert image to RGB mode
    img = img.convert("RGB")
    
    # Create a 3D array to store RGB values
    pixel_array = np.zeros((8, 8, 3), dtype=int)
    
    # Extract RGB values with thresholding
    for y in range(8):
        for x in range(8):
            r, g, b = img.getpixel((x, y))
            if r < 100 and g < 100 and b < 100:
                pixel_array[y][x] = (0, 0, 0)
           # elif r >= 200 and g >= 165 and b >= 60 and b <=80:
         #       pixel_array[y][x] = (255, 235, 0)
            else:
                pixel_array[y][x] = (r, g, b)
    
    return pixel_array

239,191,73
def format_for_cpp(array, i):
    cpp_formatted = f"int emoji7_{i}[8][8][3] = "
    cpp_formatted += "{\n "                                            
    for y in range(8):
        cpp_formatted += "    {"
        cpp_formatted += ", ".join(f"{{{r},{g},{b}}}" for r, g, b in array[y])
        cpp_formatted += "},\n"
    cpp_formatted += "};"
    return cpp_formatted

# Process multiple images
for i in range(1, 13):  
    image_path = f"/Users/jasonchen/Desktop/DCTO Apex G11/Moonshot 探月学校/Emoji Lighting/Applause/{i:02d}.jpg"  # Format filenames as 01.png, 02.png, ..., 09.png
    rgb_values = get_pixel_rgb(image_path)
    cpp_array = format_for_cpp(rgb_values, i)
    print(cpp_array)
    print("\n")

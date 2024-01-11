from PIL import Image
import os

def resize_image(input_path, output_path, scale_percent):
    # Read the original image
    image = Image.open(input_path)
    
    # Calculate new size based on ratio
    width = int(image.width * scale_percent / 100)
    height = int(image.height * scale_percent / 100)
    new_size = (width, height)
    
    # Resize image
    resized_image = image.resize(new_size)
    
    # Save new image
    resized_image.save(output_path)
    
# Example

def main():
    if os.path.exists("img/resize") == False: # tạo folder resize
        os.mkdir("img/resize")
    if os.path.exists("img/image-parse") == False: # tạo folder parse
        os.mkdir("img/image-parse")

    #Resize image and parsing
    for filename in os.listdir("img/model"): 

        resize_image("img/model/"+filename, "img/resize/" + filename, 50)
        input_path = "./img/resize/" + filename
        output_path = "./" + filename[:-4]

	#Run human parsing
        os.system("python exp/inference/inference.py --loadmodel ./inference.pth --img_path " + input_path + " --output_path ./img/image-parse --output_name " + output_path)

        # Resize parsed-image to original size
        resize_image("img/image-parse/"+filename[:-4]+".png", "img/image-parse/" + filename[:-4]+".png", 200) 
        
        # Delete unnecessary gray files
        os.remove("img/image-parse/" + filename[:-4] + "_gray.png")

main()
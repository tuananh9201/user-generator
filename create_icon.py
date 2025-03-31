from PIL import Image, ImageDraw, ImageFont
import os


def create_icon():
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)

    # Draw a colored rectangle
    draw.rectangle([20, 20, 236, 236], fill='#fc2c03')

    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    draw.text((25, 70), "VDC", fill='white', font=font)

    # Save as ICO file
    if not os.path.exists('resources'):
        os.makedirs('resources')

    image.save('resources/app_icon.ico', format='ICO', sizes=[(256, 256)])


if __name__ == '__main__':
    create_icon()

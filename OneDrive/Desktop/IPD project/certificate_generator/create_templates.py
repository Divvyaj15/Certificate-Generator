from PIL import Image, ImageDraw, ImageFont
import os

def create_template(template_name, width=1200, height=800):
    # Create a new image with a white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add a border
    draw.rectangle([(50, 50), (width-50, height-50)], outline='black', width=5)
    
    # Add a title
    title = "CERTIFICATE OF COMPLETION"
    font = ImageFont.truetype("arial.ttf", 60)
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    draw.text(((width - title_width) // 2, 150), title, font=font, fill='black')
    
    # Add decorative elements
    draw.line([(width//2 - 200, 250), (width//2 + 200, 250)], fill='black', width=2)
    
    # Save the template
    os.makedirs('static/images', exist_ok=True)
    image.save(f'static/images/{template_name}.png')

if __name__ == '__main__':
    # Create two different templates
    create_template('template1')
    create_template('template2') 
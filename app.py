from flask import Flask, render_template, redirect, url_for, send_from_directory
import random
import os
from PIL import Image
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

app = Flask(__name__)

IMAGE_FOLDER = "static/images"
CAT_FOLDER = os.path.join(IMAGE_FOLDER, "cat")
DRAGON_FOLDER = os.path.join(IMAGE_FOLDER, "dragon")

def get_random_image(folder):
    images = os.listdir(folder)
    return random.choice(images)

def create_pdf(image_path):
    output = "static/pdf_output/" + os.path.basename(image_path).replace('.jpg', '.pdf')

    # Open the image using Pillow
    img = Image.open(image_path)

    # Using ImageReader to wrap the image for ReportLab
    img_data = ImageReader(img)

    # Determine dimensions for the image on the PDF
    page_width, page_height = landscape(letter)  # Assuming letter is your desired pagesize
    aspect = img.width / img.height
    if page_width/page_height > aspect:
        width = page_height * aspect
        height = page_height
    else:
        width = page_width
        height = page_width / aspect

    # Create a canvas for the PDF
    c = canvas.Canvas(output, pagesize=landscape(letter))  # Setting to landscape mode due to most images being wider

    # Calculate the positions to center the image both vertically and horizontally
    x_position = (page_width - width) / 2
    y_position = (page_height - height) / 2

    # Drawing the image onto the canvas
    c.drawImage(img_data, x_position, y_position, width=width, height=height)
    c.showPage()  # This finalizes the current page, making it ready for the next page (or save if it's the last page)
    c.save()

    return output


# @app.route('/')
# def index(category):
#     return render_template('index.html')

@app.route('/')
def index():
    cat_image_file = get_random_image(CAT_FOLDER)
    dragon_image_file = get_random_image(DRAGON_FOLDER)

    cat_image_path = url_for('static', filename='images/cat/' + cat_image_file)
    dragon_image_path = url_for('static', filename='images/dragon/' + dragon_image_file)

    return render_template('index.html', cat_image_path=cat_image_path, dragon_image_path=dragon_image_path,cat_image_file=cat_image_file)




@app.route('/download/<category>/<image_file>')
def download_pdf(category, image_file):

    if category not in ["cat", "dragon"]:
        return redirect(url_for('index'))

    image_path = os.path.join(CAT_FOLDER if category == "cat" else DRAGON_FOLDER, image_file)
    print(image_path)
    pdf_path = create_pdf(image_path)

    return send_from_directory('static/pdf_output', os.path.basename(pdf_path), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
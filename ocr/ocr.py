from flask import Blueprint, render_template, request, current_app
from google.cloud import vision
import io
import os
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from PIL import Image

ocr_bp = Blueprint('ocr', __name__, url_prefix='/ocr')

client = vision.ImageAnnotatorClient.from_service_account_json("C:/Users/mohmd/OneDrive/Desktop/Programming/Projects/M_Tools/ocr/google_ocr_credentials.json")

def detect_text(path):

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    output = response.text_annotations[0].description
    word_list = output.split()
    word_count = len(word_list)

    return output, word_count

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)

    # Create directory for images if it does not exist
    os.makedirs('pdf_images', exist_ok=True)

    image_paths = []

    for i, image in enumerate(images):
        image_path = f'pdf_images/page_{i+1}.jpg'
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)

    return image_paths
    

@ocr_bp.route('/', methods=['GET', 'POST'])
def ocr_home():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join("C:/Users/mohmd/OneDrive/Desktop/Programming/Projects/M_Tools/ocr/uploads", filename)
            file.save(file_path)
            if file_path.lower().endswith('.pdf'):
                print("started")
                split_iamges = pdf_to_images(file_path)
                number_of_pages = len(split_iamges)
                print("done")
                word_count = 0
                total_text = ""
                for image in split_iamges:
                    image_text, image_word_count = detect_text(image)
                    word_count = word_count + image_word_count
                    total_text = total_text + image_text + "--------------\n"
            else:
                total_text, word_count = detect_text(file_path)
                number_of_pages = 1
                os.remove(file_path)
            return render_template('ocr/ocr.html', active_link='ocr', output_text=total_text, word_count=word_count, num_pages_processed=number_of_pages)
    return render_template('ocr/ocr.html', active_link='ocr')

# if __name__ == '__main__':
#     app.run(debug=True)
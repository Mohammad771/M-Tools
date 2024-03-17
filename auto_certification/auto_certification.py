# from flask import Flask, Blueprint, render_template, request
# import os
# from io import BytesIO
# from PIL import Image
# from PyPDF2 import PdfReader, PdfWriter
# from docx2pdf import convert
# import pythoncom

# auto_certification_bp = Blueprint('auto_certification', __name__, url_prefix='/auto_certification')

# def word_to_pdf(input_path, output_path):
#     # Convert Word to PDF using the docx2pdf library
#     pythoncom.CoInitialize()
#     convert(input_path, output_path)

# def merge_and_add_first_page(input_pdf, output_pdf, first_page_path):
#     # Create a PDF writer object
#     writer = PdfWriter()

#     # Add the specific first page
#     first_page_reader = PdfReader(first_page_path)
#     writer.add_page(first_page_reader.pages[0])

#     # Add the rest of the converted PDF
#     with open(input_pdf, 'rb') as f:
#         reader = PdfReader(f)
#         for page in reader.pages:
#             writer.add_page(page)

#     # Write the merged PDF to the output path
#     with open(output_pdf, 'wb') as f:
#         writer.write(f)

# @auto_certification_bp.route('/', methods=['GET', 'POST'])
# def auto_certification():
#     if request.method == 'POST':
#         uploaded_files = request.files.getlist('files')

#         # Filter and process the uploaded files
#         word_file = None
#         image_files = []
#         pdf_files = []

#         for file in uploaded_files:
#             filename = file.filename.lower()
#             if filename.endswith('.docx'):
#                 word_file = file
#             elif filename.endswith(('.jpg', '.jpeg', '.png')):
#                 image_files.append(file)
#             elif filename.endswith('.pdf'):
#                 pdf_files.append(file)

#         # Create temporary file paths for conversion and merging
#         temp_word_path = 'temp_word.docx'
#         temp_pdf_path = 'temp_pdf.pdf'
#         temp_merged_path = 'temp_merged.pdf'

#         if word_file:
#             # Save the Word file to a temporary path
#             word_file.save(temp_word_path)

#             # Convert Word file to PDF
#             word_to_pdf(temp_word_path, temp_pdf_path)

#         # Merge PDF and image files
#         if pdf_files or image_files:
#             # Create the merged PDF with the first page
#             specific_page_path = 'C:/Users/mohmd/OneDrive/Desktop/Programming/Projects/M_Tools/auto_certification/certification_page.pdf'

#             merge_and_add_first_page(temp_pdf_path, temp_merged_path, specific_page_path)
#         else:
#             # No need to merge, just rename the converted PDF
#             os.rename(temp_pdf_path, temp_merged_path)

#         # Clean up temporary files
#         if word_file:
#             os.remove(temp_word_path)
#         if pdf_files:
#             for pdf_file in pdf_files:
#                 pdf_file.close()  # Close the file handle before removing the temporary file
#                 os.remove(pdf_file.filename)
#         if image_files:
#             for image_file in image_files:
#                 image_file.close()  # Close the file handle before removing the temporary file
#                 os.remove(image_file.filename)

#         # Return the rendered template and the path of the merged PDF
#         return render_template('auto_certification/auto_certification.html', pdf_path=temp_merged_path), 200, {'Content-Type': 'text/html'}

#     return render_template('auto_certification/auto_certification.html')

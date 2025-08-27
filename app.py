from flask import Flask, render_template, request ,url_for
from google.cloud import storage
import os
from prompts import generate

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
GCS_BUCKET_NAME = 'visualize-you'  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def upload_to_gcs(file):
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file.filename)

    # Upload the file to GCS
    blob.upload_from_file(file)

    return blob.public_url

def mars_visualize_prompt(mars_visualize_input) :
    return f'I want to see myself {mars_visualize_input} on mars,Please dont change my outfit. Make sure my face is visible. This is my image:'

def see_me_as_prompt(see_me_as_input) :
    return f'I want to see myself as this profession : {see_me_as_input}, This is my image:'

def change_colour_prompt(change_colour_input) :
    return f'I want to change my shirt colour  as : {change_colour_input}, This is my image:'


@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    file_url = None
    
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        color = request.form.get('color')
        profession = request.form.get('profession')
        mars_visualize = request.form.get('mars_visualize')
        anyelse = request.form.get('anythingelse')
        if uploaded_file:
            file_url = upload_to_gcs(uploaded_file)
            if 'change_color' in request.form:
                text = change_colour_prompt(color)
                print(f'Added text to prompt {text}')
                img = generate(text,file_path)
                output = f"Change shirt color to {color} for file: {uploaded_file.filename}"
            elif 'see_me_as' in request.form:
                text = see_me_as_prompt(profession)
                output = f"See me as a {profession} with file: {uploaded_file.filename}"
                img = generate(text,file_path)
            elif 'mars_visualize' in request.form:
                text = mars_visualize_prompt(mars_visualize)
                img = generate(text,file_path)
                output = f"See me as a {mars_visualize} with file: {uploaded_file.filename}"
	    elif 'anythingelse' in request.form:
		text = anyelse_visualize_prompt(anyelse)
                img = generate(text,file_path)
                output = f"See me as a {anyelse} with file: {uploaded_file.filename}"
            if img and isinstance(img, bytes):
              print('Output is bytes image')
              img_data = base64.b64encode(img).decode('utf-8')
              img_type = imghdr.what(None, h=img) or 'png'
              mime_type = f'image/{img_type}'
              print(f'Image mime type is {mime_type}')

        try:
            if file_url : return render_template('index.html', output=output,file_url=file_url, img_data=img_data, mime_type=mime_type)
        except Exception as e:
          print(f'Unable to see file: {e}')
          # pass

    return render_template('index.html', output=output, file_url=file_url, img_data=img_data, mime_type=mime_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)


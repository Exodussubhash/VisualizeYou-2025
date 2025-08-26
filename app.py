from flask import Flask, render_template, request ,url_for
from google.cloud import storage
import os

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
GCS_BUCKET_NAME = 'visualize-you'  


def upload_to_gcs(file):
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file.filename)

    # Upload the file to GCS
    blob.upload_from_file(file)

    return blob.public_url


@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    file_url = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        color = request.form.get('color')
        profession = request.form.get('profession')
        mars_visualize = request.form.get('mars_visualize')
        if uploaded_file:
            file_url = upload_to_gcs(uploaded_file)
            if 'change_color' in request.form:
                output = f"Change shirt color to {color} for file: {uploaded_file.filename}"
            elif 'see_me_as' in request.form:
                output = f"See me as a {profession} with file: {uploaded_file.filename}"
            elif 'mars_visualize' in request.form:
                output = f"See me as a {mars_visualize} with file: {uploaded_file.filename}"
    
    try:
        if file_url : return render_template('index.html', output=output,file_url=file_url)
    except Exception as e:
        print(f'Unable to see file: {e}')
        pass

    return render_template('index.html', output=output)

if __name__ == '__main__':

    app.run(debug=True)

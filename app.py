from flask import Flask, render_template, request ,url_for
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'


@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        color = request.form.get('color')
        profession = request.form.get('profession')
        mars_visualize = request.form.get('mars_visualize')
        if uploaded_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            file_url = url_for('static', filename='uploads/' + uploaded_file.filename)
        if uploaded_file:
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
import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TODOWNLOAD_FOLDER'] = 'toget'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['TODOWNLOAD_FOLDER']):
    os.makedirs(app.config['TODOWNLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Files uploaded successfully!'
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        return send_from_directory(app.config['TODOWNLOAD_FOLDER'], filename, as_attachment=True)
    files = os.listdir(app.config['TODOWNLOAD_FOLDER'])
    return render_template('download.html', files=files)

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

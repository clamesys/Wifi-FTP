#modules required

import os
import socket
import webbrowser
from waitress import serve
from flask import Flask, request, render_template, send_from_directory, url_for

app = Flask(__name__, template_folder='templates')

# configs to assign timeout, upload folder name and download folder name

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TODOWNLOAD_FOLDER'] = 'toget'
app.config['TIMEOUT'] = 1200

# code to show the ip addr of the host pc to connect to

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
a=(sock.getsockname())
url="http://"+a[0]+"/"
sock.close()

# To automatically make the uploads dir if not present in the same dir as the app.py

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# To automatically make the toget dir if not present in the same dir as the app.py

if not os.path.exists(app.config['TODOWNLOAD_FOLDER']):
    os.makedirs(app.config['TODOWNLOAD_FOLDER'])

# Route to upload file to hosts pc

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Files uploaded successfully!'
    return render_template('index.html', download_url=url_for('download_file'))

# Route to download file from hosts pc

@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        return send_from_directory(app.config['TODOWNLOAD_FOLDER'], filename, as_attachment=True)
    files = os.listdir(app.config['TODOWNLOAD_FOLDER'])
    return render_template('download.html', files=files)

# To shutdown server

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    # sys.exit()
    os._exit(os.getpid())

# Development Server

# if __name__ == '__main__':
#     app.run(debug=true, host='0.0.0.0', port=80)

# Production server

if __name__ == "__main__":
    webbrowser.open_new_tab(url) 
    serve(app, host="0.0.0.0", port=80)
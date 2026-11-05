import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string

app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Storage Lokal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin: auto; }
        h2 { color: #0056b3; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }
        .upload-section { background: #e9ecef; padding: 20px; border-radius: 6px; margin-bottom: 20px; }
        input[type="file"] { margin-bottom: 10px; font-size: 16px; }
        button { background: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 15px; }
        button:hover { background: #0056b3; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; padding: 12px; margin-bottom: 8px; border: 1px solid #dee2e6; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        a.download-btn { background: #28a745; color: white; text-decoration: none; padding: 5px 10px; border-radius: 4px; font-size: 14px; font-weight: bold; }
        a.download-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📁 Cloud Storage Lokal Ubuntu</h2>
        
        <!-- Form Upload File -->
        <div class="upload-section">
            <h3>Unggah File Baru</h3>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file" required><br>
                <button type="submit">Upload ke Server</button>
            </form>
        </div>

        <!-- Daftar File di Server -->
        <h3>Daftar Berkas Tersimpan</h3>
        <ul>
            {% if files %}
                {% for file in files %}
                <li>
                    <span>{{ file }}</span>
                    <a class="download-btn" href="/download/{{ file }}">Download</a>
                </li>
                {% endfor %}
            {% else %}
                <p style="color: #6c757d;">Belum ada file yang diunggah.</p>
            {% endif %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
  
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect('/')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)

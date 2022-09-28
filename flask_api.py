import os
from flask import Flask,request,redirect,url_for, render_template, send_from_directory, jsonify
from gevent import pywsgi
import pathlib
folder_path = pathlib.Path(__file__).parent.absolute()
#UPLOAD_FOLDER = r"d:\work\python\test_flask\trainning_data"
UPLOAD_FOLDER = os.path.join(folder_path,'trainning_data')
DOWN_FOLDER = os.path.join(folder_path,'trainning_data')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWN_FOLDER'] = DOWN_FOLDER
@app.route('/', methods=['GET','POST'])
def root():
    return render_template('filename.html')
      
@app.route('/upload', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        return redirect(url_for('root',filename=file.filename, action="post"))
    return redirect('/')

@app.route('/download/<dirname1>/<filename>', methods=['GET','POST'])
def download_file(dirname1,filename):
    if dirname1 != '':
        path = os.path.join(app.config['DOWN_FOLDER'],dirname1)
        return send_from_directory(path,filename, as_attachment=True)
    return send_from_directory(app.config['DOWN_FOLDER'], as_attachment=True)


@app.route('/dir/<path:dirname>', methods=['GET','POST'])
def list_dir(dirname):
    files = []
    for file_name in os.listdir('{}\{}'.format(app.config['DOWN_FOLDER'],dirname)):
        path = os.path.join(app.config['DOWN_FOLDER'],dirname,file_name)
        files.append(file_name)
     
    return jsonify(files)  
    
@app.route('/files')
def list_files():
    files = []
    dir = []
    for file_name in os.listdir(app.config['DOWN_FOLDER']):
        path = os.path.join(app.config['DOWN_FOLDER'],file_name)
        if os.path.isfile(path):
            files.append(file_name)
        else:
            dir.append(file_name)
    return jsonify(files,dir)

if __name__ == '__main__':
    app.run(debug=True)
    

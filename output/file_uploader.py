import os
import pathlib
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware

UPLOAD_FOLDER = 'C:/Harish/Investment_work/EPG_Analytics/output/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'html', '.log'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
files_uploaded = []


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("***Upload method invoked")
    global files_uploaded
    if request.method == 'POST':
        file_to_upload = ""
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_to_upload = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)
            print("filename>>>>>>>>", filename)
            tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("Tmp path =>>>", tmp_path)
            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            get_list_of_files()
            print("file saved>>>", files_uploaded)
            return redirect(url_for("uploaded_file",
                                    filename=filename))
    return render_template('upload.html')


def get_list_of_files():
    global files_uploaded
    files_uploaded = []
    for currentFile in pathlib.Path(UPLOAD_FOLDER).iterdir():
        tmp_str = str(currentFile)
        print(">>>>tmp_str=====", tmp_str)
        temp_len = tmp_str.count("\\")
        print(">>>>count= ====", temp_len)
        assert isinstance(temp_len, object)
        tmp_str = tmp_str.split("\\", temp_len)
        tmp_filename = tmp_str[temp_len]
        print("$$$$$tmp_filename>>>", tmp_filename)
        files_uploaded.append(tmp_filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    global files_uploaded
    # print("file saved list sent to web page!!>>>", files_uploaded)
    print(">>Uploaded file name is ", filename)
    return render_template("template.html", filename=filename, files_uploaded=files_uploaded)


def clean_up_folder():
    file_list = [f for f in os.listdir(UPLOAD_FOLDER)]
    for f in file_list:
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    print(">>All Files deleted!!!")


@app.route('/exec', methods=['GET', 'POST'])
def parse(name=None):
    clean_up_folder()
    print("all files deleted")
    upload_file()
    return render_template('template.html', clear_page="None")


@app.route('/getlist')
def get_file_list(name=None):
    print(">>>Get list of files")
    get_list_of_files()
    print(">>>>>>>>>>>>>>display list of files")
    upload_file()
    var_is_empty = False
    global files_uploaded
    if len(files_uploaded) == 0:
        var_is_empty = True
    return render_template('upload.html', files_uploaded=files_uploaded, clear_page="None", is_empty=var_is_empty)
    # return redirect(url_for("upload_file", files_uploaded=files_uploaded))


@app.route('/result')
def result_display():
    import sample_import
    sample_import.__init__()
    print("result display")
    return render_template('stat_index.html', clear_page="None")


@app.route('/graph', methods=['GET', 'POST'])
def graph_display():
    print("result display")
    return render_template('result.html', clear_page="None")


if __name__ == "__main__":
    print("File  load start!!!!!!")
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_TYPE'] = 'filesystem'

app.run(debug=True)

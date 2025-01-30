import qrcode
import os
from io import BytesIO
from flask import Flask, send_file, request, render_template_string, render_template

app = Flask(__name__)

def load(file):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{path}/webpage/{file}") as f:
        return f.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        qrtype = request.form.get('type')  
    elif request.method == 'GET':
        qrtype = request.args.get('type') 
    else:
        qrtype = "LINK"

    if qrtype == "LINK":
        form = f"""
        <h2>Enter Url:</h2>
         <form action="" method="get" enctype="multipart/form-data" id="uploadForm">
            <input type="hidden" name="type" value="LINK">
            <input type="text" name="link" id="link" />
            <br><br>
            <input type="submit" value="Upload" id="submitButton" />
            <p id="error" style="color: red; display: none;">File size must be below !MAXFILESIZEHERE! MB.</p>
         </form>
        """
    elif qrtype == "MAIL":
        form = f"""
        <h2>Enter Email:</h2>
         <form action="" method="get" enctype="multipart/form-data" id="uploadForm">
            <input type="hidden" name="type" value="EMAIL">
            <input type="text" name="link" id="link" />
            <br><br>
            <input type="submit" value="Upload" id="submitButton" />
            <p id="error" style="color: red; display: none;">File size must be below !MAXFILESIZEHERE! MB.</p>
         </form>
        """
    else:
        form = f"""
        <h2>Enter Telephone:</h2>
         <form action="" method="get" enctype="multipart/form-data" id="uploadForm">
            <input type="hidden" name="type" value="TEL">
            <input type="text" name="link" id="link" />
            <br><br>
            <input type="submit" value="Upload" id="submitButton" />
            <p id="error" style="color: red; display: none;">File size must be below !MAXFILESIZEHERE! MB.</p>
         </form>
        """
    
    if request.method == 'POST':
        qrtype = request.form.get('type')  
    elif request.method == 'GET':
        qrtype = request.args.get('type') 
    
    codeimg = "<h2> fill out info to generate qr code </h2>"
    if qrtype and request.args.get('link') != None:
        print(qrtype)
        try:
            if qrtype == "LINK":
                codeimg = f'<img src="qrcode?link={request.args.get('link')}"'
            elif qrtype == "EMAIL":
                codeimg = f'<img src="qrcode?link=MAILTO:{request.args.get('link')}">'
            elif qrtype == "TEL":
                codeimg = f'<img src="qrcode?link=TEL:{request.args.get('link')}" width="400" height="400">'
        except:
            print("nocontent")
            codeimg = "<h2> fill out info to generate qr code </h2>"
    else:
        codeimg = "<h2> fill out info to generate qr code </h2>"
    print(codeimg)
    return render_template("home.html", form=form, codeimg=codeimg)
    

@app.route('/qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    if request.method == 'POST':
        link = request.form.get('link')  
    else:
        link = request.args.get('link') 

    if not link:
        return "No link provided", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    return send_file(buffered, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

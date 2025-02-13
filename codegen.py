import qrcode
import os
from io import BytesIO
from flask import Flask, send_file, request, render_template_string, render_template
from urllib.parse import quote

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
    elif qrtype == "WIFI":
        form = f"""
        
         <form action="" method="get" enctype="multipart/form-data" id="uploadForm">
            <input type="hidden" name="type" value="WIFI">
            <input type="hidden" name="link" value="asd">
            <h3>Enter Wifi Name:</h3>
            <input type="text" name="NAME" id="NAME" />
            <select name="security" id="security">
                <option value="WPA">wpa</option>
                <option value="WEP">wep</option>
            </select>
            <h3>Enter Wifi Password (if aplicable):</h3>
            <input type="text" name="password" id="password" />
            <br><br>
            <input type="submit" value="Upload" id="submitButton" />
            <p id="error" style="color: red; display: none;">File size must be below !MAXFILESIZEHERE! MB.</p>
         </form>
        """
    elif qrtype == "VCARD":
        form = f"""
        <a href="Vcard"> <h1> Configure </h1> </a>
        """
    else:
        form = f"""
        <h2>Enter Telephone:</h2>
         <form action="" method="get" enctype="multipart/form-data" id="uploadForm">
            <input type="hidden" name="type" value="TEL">
            <input type="text" name="link" id="link" />
            <br><br>
            <input type="submit" value="Upload" id="submitButton" />
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
                codeimg = f'<img src="qrcode?link={request.args.get('link')}" width="400" height="400">'
            elif qrtype == "EMAIL":
                codeimg = f'<img src="qrcode?link=MAILTO:{request.args.get('link')}" width="400" height="400">'
            elif qrtype == "TEL":
                codeimg = f'<img src="qrcode?link=TEL:{request.args.get('link')}" width="400" height="400">'
            elif qrtype == "WIFI":
                codeimg = f'<img src="qrcode?link=WIFI:S:{request.args.get('NAME')};T:{request.args.get('security')};P:{request.args.get('password')};;" width="400" height="400">'
            elif qrtype == "VCARD":
                codeimg = ""
                if request.args.get('FNAME') and request.args.get('LNAME'):
                    codeimg += f"FN:{request.args.get('FNAME')} {request.args.get('LNAME')} \nN;CHARSET=UTF-8:{request.args.get('LNAME')};{request.args.get('FNAME')};;;\n"
                if request.args.get('Gender'):
                    codeimg += f"GENDER:{request.args.get('Gender')}\n"
                if request.args.get('MEMAIL'):
                    codeimg += f"EMAIL:{request.args.get('MEMAIL')}\n"
                if request.args.get('CELLPHONE'):
                    codeimg += f"TEL;TYPE=CELL:{request.args.get('CELLPHONE')}\n"
                if request.args.get('HOMEPHONE'):
                    codeimg += f"TEL;TYPE=HOME,VOICE:{request.args.get('HOMEPHONE')}\n"
                codeimg = f"""
BEGIN:VCARD
VERSION:3.0
{codeimg}END:VCARD
"""             
                encoded_vcard = quote(codeimg)
                print(codeimg)
                codeimg = f'<img src="qrcode?link={codeimg}" width="400" height="400">'
        except:
            print("nocontent")
            codeimg = "<h2> fill out info to generate qr code </h2>"
    else:
        codeimg = "<h2> fill out info to generate qr code </h2>"
    print(codeimg)
    return render_template("home.html", form=form, codeimg=codeimg)
    
@app.route('/Vcard', methods=['GET', 'POST'])
def vcard():
    return render_template("Vcardconf.html")
    
    
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
    app.run(host='0.0.0.0', port=8060, debug=True)


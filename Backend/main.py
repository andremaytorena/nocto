from flask import (
  Flask,
  request,
  send_file
)
from check_license import check_license

app = Flask(__name__, static_folder=".",
static_url_path="", template_folder=".")

@app.route("/version", methods=["GET"])
def checkVersion():
  return "0.3.3"####
 
@app.route("/download", methods=["GET"])
def download():
  return send_file('noctotools.exe')

@app.route("/authorize_license", methods=["GET"])
def checklicensekey():
  license_key = request.headers.get('api_key')
  authorized = check_license(license_key)
  return authorized

@app.route("/chrome_version", methods=["GET"])
def checkChromeVersion():
  return "111.0.5563.64"

@app.route("/revolut_personal_version", methods=["GET"])
def checkRevolutPersonalVersion():
  return "9.10.1"###

@app.route("/revolut_personal_useragent", methods=["GET"])
def checkRevolutPersonalUseragent():
  return "Revolut/com.revolut.revolut 9.10.1 901001804 (ASUS_Z01QD; Android 7.1.2; sp:GPS; cf:07266AACA93B3FAA8A535C3D7AEC4C1F)"###

if __name__ == "__main__":
  app.run(port=3333)

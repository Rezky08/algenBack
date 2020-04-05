from flask import Flask,request,jsonify
from flask_cors import CORS
from handle import handle

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return "hello"
@app.route('/kelompok',methods=['POST'])
def kelompok():
    hd = handle(request.get_json())
    response_json = jsonify(hd.kelompok())
    return response_json
@app.route('/dosen',methods=['POST'])
def dosen():
    hd = handle(request.get_json())
    response_json = jsonify(hd.dosen())
    return response_json,200
@app.route('/jadwal',methods=['POST'])
def jadwal():
    hd = handle(request.get_json())
    response_json = jsonify(hd.jadwal())
    return response_json,200


if __name__=="__main__":
    app.run(debug=True,threaded=True)
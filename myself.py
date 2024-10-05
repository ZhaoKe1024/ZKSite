#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 17:47
# @Author: ZhaoKe
# @File : myself.py
# @Software: PyCharm
from flask import Flask, render_template, jsonify, request, url_for
from gevent import pywsgi
from zkmusic_sql import sqlalchemy_test, add_new_items

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'


@app.route('/')
def index():
    return render_template("./myself.html")


@app.route('/all_music')
def get_music_list():
    data = sqlalchemy_test()
    print(data)
    return jsonify(response={"data": data})


@app.route("/getitems", methods=["POST"])
def add_new_items_http():
    print(request.form)
    form_data = request.form
    song_list = []
    for key in form_data:
        if key == "code":
            if form_data.get("code") == "ran0307":
                continue
            else:
                return jsonify(response={"msg": "Error Code"})

        else:
            print(key, ":", form_data.get(key).split(','))
            song_list.append(form_data.get(key).split(','))
    print("get data...")
    print(song_list)
    print("get data...")
    if len(song_list) == 0:
        msg = "length of form data is 0!"
    else:
        msg = add_new_items(song_list)
    #for key in form_data:
    #   print(key)
    #   print(form_data.get(key))
    return jsonify(response={"msg": msg})

@app.route('/zkmusic')
def go_music():
    # return redirect(url_for('./zkmusiclist.html'))
    return render_template('./zkmusiclist.html')


if __name__ == '__main__':
    print("ZKworkhome Runing...")
    http_server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()

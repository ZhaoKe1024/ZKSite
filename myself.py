#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 17:47
# @Author: ZhaoKe
# @File : myself.py
# @Software: PyCharm
from flask import Flask, render_template, jsonify, request, url_for
from gevent import pywsgi
from zkmusic_sql import sqlalchemy_test

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


@app.route("/getitems")
def add_new_items_http():
    form_data = request.form
    for key in form_data:
        print(key)
        print(form_data.get(key))

@app.route('/zkmusic')
def go_music():
    # return redirect(url_for('./zkmusiclist.html'))
    return render_template('./zkmusiclist.html')


if __name__ == '__main__':
    print("ZKworkhome Runing...")
    http_server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()

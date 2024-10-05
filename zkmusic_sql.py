#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 13:20
# @Author: ZhaoKe
# @File : zkmusic_sql.py
# @Software: PyCharm
import json
import pandas as pd
from flask import Flask
from sqlalchemy import create_engine, select, Column, text as sql_text
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__, static_folder='static', static_url_path='/static')

Base = declarative_base()


class Playlist(Base):
    __tablename__ = 'playlists'
    list_id = Column(Integer,
                     primary_key=True)  # primary key, id  # Even if this field is not used, it must be explicitly defined, otherwise it cannot be mapped to the data table.
    list_name = Column(String(32))
    list_expr = Column(String(255))

    # from_device = Column(DateTime)  # 采集设备？这个其实是开集识别了  # 自然数

    def __repr__(self):
        return "<Item(list_name='%s', list_expr='%s'>" % (self.list_name, self.list_expr)


class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer,
                     primary_key=True)  # primary key, id  # Even if this field is not used, it must be explicitly defined, otherwise it cannot be mapped to the data table.
    song_name = Column(String(64))
    playlist = Column(String(16))
    singer = Column(String(16))
    composer = Column(String(16))
    lyrics = Column(String(16))
    arrangement = Column(String(16))
    tags = Column(String(256))
    album = Column(String(32))
    released_date = Column(Date)

    # from_device = Column(DateTime)  # 采集设备？这个其实是开集识别了  # 自然数

    def __repr__(self):
        return "<Item(song_name='%s', singer='%s', playlist='%s'>" % (self.song_name, self.singer, self.playlist)


with open("./private/act.json", 'r', encoding='utf_8') as fp:
    json_str = fp.read()
json_data = json.loads(json_str)
pwd = json_data["pwd"]
basename = json_data["usr"]


def sqlalchemy_test():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/{basename}")
    # 查询2021年9月30日之后的所有item
    # sql =
    # sql = "DELETE FROM songs WHERE song_id=8;"
    # pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
    # # print(df)
    #
    # sql = "ALTER TABLE songs ADD album VARCHAR(64);"
    # pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
    # # print(df)
    #
    # sql = "ALTER TABLE songs ADD released_date datetime;"
    # pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))

    sql = "select * from songs;"
    df = pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
    df = df.where(pd.notnull(df), None)
    res = []
    for item in df.itertuples():
        tmp = []
        for j in range(2, 10):
            if item[j] is not None:
                tmp.append(item[j])
            else:
                tmp.append("")
        tmp.append(str(item[10])[:11])
        res.append(tmp)
    # print(df.iloc[:, [0, 1, 3, 2]])
    # print(res)
    return res


def add_new_items(song_list):
    if len(song_list) == 0:
        return "Error! Empty List to Save!"
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/{basename}")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        data_to_save = []
        for item in song_list:
            data_to_save.append(Song(song_name=item[0],
                                     playlist=item[1],
                                     singer=item[2],
                                     composer=item[3],
                                     lyrics=item[4],
                                     arrangement=item[5],
                                     tags=item[6],
                                     album=item[7],
                                     released_date=item[8]))
        session.add_all(data_to_save)
        session.commit()
        print("Data insert into database zkmusic table songs successfully!")
        sql = "select * from playlists;"
        df = pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
        print(df)
        return "Insert Successfully!"
    except Exception as e:
        print(e)


def add_new_playlist_input():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/{basename}")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        session.add_all(
            [Playlist(list_name="华语伤感", list_expr='悲伤的心情')
             ])
        session.commit()
        print("????????????????????????????????????????")
        print("Data insert into database cough_schema table cough_main successfully!")

        sql = "select * from playlists;"
        df = pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
        print(df)

    except Exception as e:
        print(e)

# ==================================================================================

def test_insert():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/{basename}")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        fast_input = [
            "，，，，，，，，", ]
        all_item = []
        for item in fast_input:
            fast_input_parts = item.split('，')
            if fast_input_parts[0] == "":
                continue
            all_item.append(Song(song_name=fast_input_parts[0],
                                 playlist=fast_input_parts[1],
                                 singer=fast_input_parts[2],
                                 composer=fast_input_parts[3],
                                 lyrics=fast_input_parts[4],
                                 arrangement=fast_input_parts[5],
                                 tags=fast_input_parts[6],
                                 album=fast_input_parts[7],
                                 released_date=fast_input_parts[8]))
        if len(all_item) == 0:
            return
        session.add_all(all_item)
        session.flush()
        session.commit()
        print("Data insert into database [zkmusic] table [songs] successfully!")
        sql = "select * from songs;"
        df = pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
        print(df.iloc[:, [0, 1, 3, 2]])
    except Exception as e:
        print(e)
        sqlalchemy_test()


# def sqlalchemy_test1():
#     ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/inbreed")
#     Base.metadata.create_all(ENGINE)
#     Session = sessionmaker(bind=ENGINE)
#     session = Session()
#     try:
#         session.execute(select(accounts))
#         print("Data insert into database cough_schema table cough_main successfully!")
#         # sqlalchemy_test()
#     except Exception as e:
#         print(e)


if __name__ == '__main__':
    # add_new_table()
    # test_insert()
    sqlalchemy_test()

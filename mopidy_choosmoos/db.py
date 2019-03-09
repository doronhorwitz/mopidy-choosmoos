from peewee import Model, SqliteDatabase, TextField, UUIDField


db = SqliteDatabase('choosmoos.db')


class BaseModel(Model):
    class Meta(object):
        database = db


class Playlist(BaseModel):
    id = UUIDField(primary_key=True)
    uri = TextField()

    class Meta(object):
        table_name = 'playlists'


def init():
    db.create_tables([Playlist])


def stop():
    db.close()

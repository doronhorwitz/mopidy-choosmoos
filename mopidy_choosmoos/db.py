from peewee import Model, SqliteDatabase, TextField, UUIDField


db = SqliteDatabase('choosmoos.db')


class BaseModel(Model):
    class Meta:
        database = db


class Playlist(BaseModel):
    id = UUIDField(primary_key=True)
    uri = TextField()


def init():
    db.create_tables([Playlist])
    db.connect()

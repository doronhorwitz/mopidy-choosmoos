from peewee import Model, SqliteDatabase, TextField, UUIDField


_db = SqliteDatabase("/home/pi/choosmoos.db")


class BaseModel(Model):
    class Meta:
        database = _db


class Playlist(BaseModel):
    tag_uuid = UUIDField(primary_key=True)
    playlist_uri = TextField()

    class Meta:
        table_name = "playlists"


class _DbWrapper:
    @staticmethod
    def init():
        _db.create_tables([Playlist])

    @staticmethod
    def close():
        _db.close()

    @staticmethod
    def get_all_playlists():
        return list(Playlist.select())

    @staticmethod
    def assign_playlist_uri_to_tag_uuid(tag_uuid, playlist_uri):
        Playlist.replace(tag_uuid=tag_uuid, playlist_uri=playlist_uri).execute()


db = _DbWrapper

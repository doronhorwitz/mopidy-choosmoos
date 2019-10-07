from peewee import Model, SqliteDatabase, TextField, UUIDField


_db = SqliteDatabase('choosmoos.db')


class BaseModel(Model):
    class Meta(object):
        database = _db


class Playlist(BaseModel):
    id = UUIDField(primary_key=True)
    uri = TextField()

    class Meta(object):
        table_name = 'playlists'


class _DbWrapper(object):
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
    def assign_playlist_id_to_tag(playlist_id, tag_uuid):
        Playlist.replace(id=tag_uuid, uri=playlist_id).execute()


db = _DbWrapper

from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from flask_app.main.models import Song
from flask_app import app
from flask_app.main.resources.schemas.song import SongSchema

class SongIDAPI(Resource):
    """Single song through id"""

    def get(self, id):
        try:
            song = Song.query.get(id)
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['SONG_NOT_FOUND'].format(id))

        return SongSchema().dump(song).data


class SongNameAPI(Resource):
    """list of songs using a name"""

    def get(self, songName):
        """Get songs with name"""
        try:
            actualSongName = songName.replace('+', ' ')
            songs = Song.query.filter_by(name=actualSongName)
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['SONG_NOT_FOUND'].format(actualSongName))

        return SongSchema().dump(songs, many=True).data

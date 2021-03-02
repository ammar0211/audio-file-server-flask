"""Data models."""
from marshmallow import Schema, fields, validates
from . import db

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)

    def __init__(self, name, duration, upload_time, file_name):
        self.name = name
        self.duration = duration
        self.upload_time = upload_time
        self.file_name = file_name

# podcast Class/Model
class Podcast(db.Model):
    __tablename__ = 'podcasts'

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(1030), nullable=True)
    file_name = db.Column(db.String(100), nullable=False)

    def __init__(self, name, duration, upload_time, host, participants, file_name):
        self.name = name
        self.duration = duration
        self.upload_time = upload_time
        self.host = host
        self.participants = participants
        self.file_name = file_name


# audiobooks Class/Model
class Audiobook(db.Model):
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)

    def __init__(self, title, author, narrator, duration, upload_time, file_name):
        self.title = title
        self.author = author
        self.narrator = narrator
        self.duration = duration
        self.upload_time = upload_time
        self.file_name = file_name


# Table Schema
class SongSchema(Schema):
    id = fields.Int(strict=True, required=True, validate=(lambda x: x>0))
    name = fields.String(required=True, validate=(lambda x: len(x)<=100))
    duration = fields.Int(strict=True, required=True)
    upload_time = fields.DateTime(strict=True, required=True)

class PodcastSchema(Schema):
    id = fields.Int(strict=True, required=True, validate=(lambda x: x>0))
    name = fields.String(required=True, validate=(lambda x: len(x)<=100))
    duration = fields.Int(strict=True, required=True)
    upload_time = fields.DateTime(strict=True, required=True)
    host = fields.String(required=True, validate=(lambda x: len(x)<=100))
    participants = fields.String(required=False, validate=(lambda x: len(x)<=1030))
    # participants = fields.List(fields.String(validate=(lambda x: len(x)<=100)),validate=(lambda x: len(x)<=10))

class AudiobookSchema(Schema):
    id = fields.Int(strict=True, required=True, validate=(lambda x: x>0))
    title = fields.String(required=True, validate=(lambda x: len(x)<=100))
    author = fields.String(required=True, validate=(lambda x: len(x)<=100))
    narrator = fields.String(required=True, validate=(lambda x: len(x)<=100))
    duration = fields.Int(strict=True, required=True)
    upload_time = fields.DateTime(strict=True, required=True)

# Init schema
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

audiobook_schema = AudiobookSchema()
audiobooks_schema = AudiobookSchema(many=True)

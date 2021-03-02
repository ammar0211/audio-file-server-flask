from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validates
from werkzeug.utils import secure_filename
import os, datetime, ast
from flask import current_app as app
from .models import db, Song, Audiobook, Podcast, song_schema, songs_schema, podcast_schema, podcasts_schema, audiobook_schema, audiobooks_schema


#CREATE ROUTE
@app.route('/create', methods=['POST'])
def create():
    try:
        audioFileType=request.form['audioFileType']
        audioFileMetadata=request.form['audioFileMetadata']
        audioFileMetadata=ast.literal_eval(audioFileMetadata)
        uploadedFile=request.files['audioFile']

        if audioFileType.lower()=='song':
            try:
                name=audioFileMetadata['name']
                duration=audioFileMetadata['duration']
            except:
                return "The request is invalid: 400 bad request",400

            #VALIDATION
            if len(name)>100 or not str(duration).isdigit() :
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./song/"+fileName
            uploadedFile.save(filePath)

            new_song = Song(name,duration,uploadTime,fileName)
            db.session.add(new_song)
            db.session.commit()

        elif audioFileType.lower()=='podcast':
            try:
                name=audioFileMetadata['name']
                duration=audioFileMetadata['duration']
                host=audioFileMetadata['host']
            except:
                return "The request is invalid: 400 bad request",400
            try:
                participants=audioFileMetadata['participants']
                if len(participants)>10 or any(len(participants) > 100 for participant in participants):
                    return "The request is invalid: 400 bad request",400
            except:
                participants=None

            #VALIDATION
            if len(name)>100 or len(host)>100 or not str(duration).isdigit():
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./podcast/"+fileName
            uploadedFile.save(filePath)

            new_podcast = Podcast(name,duration,uploadTime,host,str(participants),fileName)
            db.session.add(new_podcast)
            db.session.commit()

        elif audioFileType.lower()=='audiobook':
            try:
                title=audioFileMetadata['title']
                duration=audioFileMetadata['duration']
                author=audioFileMetadata['author']
                narrator=audioFileMetadata['narrator']
            except:
                return "The request is invalid: 400 bad request",400

            #VALIDATION
            if len(title)>100 or len(author)>100 or len(narrator)>100 or not str(duration).isdigit():
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./audiobook/"+fileName
            uploadedFile.save(filePath)

            new_podcast = Audiobook(title, author, narrator, duration, uploadTime, fileName)
            db.session.add(new_podcast)
            db.session.commit()

        else:
            return "The request is invalid: 400 bad request",400

        return "Action is successful: 200 OK",200
    except Exception as e:
        print (e)
        return "500 internal server error", 500


#GET ROUTE
@app.route('/get/<audioFileType>',defaults={'audioFileID': None} ,methods=['GET'])
@app.route('/get/<audioFileType>/<audioFileID>', methods=['GET'])
def get(audioFileType,audioFileID):
    # try:
        if audioFileID==None:
            if audioFileType=='song':
                all_files=Song.query.all()
                result = songs_schema.dump(all_files)
                return jsonify(result),200
            elif audioFileType=='audiobook':
                all_files=Audiobook.query.all()
                result = audiobooks_schema.dump(all_files)
                return jsonify(result),200
            elif audioFileType=='podcast':
                all_files=Podcast.query.all()
                result = podcasts_schema.dump(all_files)
                return jsonify(result),200
            else:
                return "The request is invalid: 400 bad request", 400
        else:
            if audioFileType=='song':
                all_files=Song.query.get(audioFileID)
                if all_files==None:
                    return "The request is invalid: 400 bad request", 400
                result = song_schema.dump(all_files)
                return jsonify(result),200
            elif audioFileType=='audiobook':
                all_files=Audiobook.query.get(audioFileID)
                if all_files==None:
                    return "The request is invalid: 400 bad request", 400
                result = audiobook_schema.dump(all_files)
                return jsonify(result),200
            elif audioFileType=='podcast':
                all_files=Podcast.query.get(audioFileID)
                if all_files==None:
                    return "The request is invalid: 400 bad request", 400
                result = podcast_schema.dump(all_files)
                return jsonify(result),200
            else:
                return "The request is invalid: 400 bad request", 400
    # except:
    #     return "500 internal server error", 500


#UPDATE ROUTE
@app.route('/update/<audioFileType>/<audioFileID>', methods=['PUT'])
def update(audioFileType,audioFileID):
    try:

        audioFileMetadata=request.form['audioFileMetadata']
        audioFileMetadata=ast.literal_eval(audioFileMetadata)
        uploadedFile=request.files['audioFile']

        if audioFileType.lower()=='song':
            try:
                update_file=Song.query.get(audioFileID)

                name=audioFileMetadata['name']
                duration=audioFileMetadata['duration']
            except:
                return "The request is invalid: 400 bad request",400

            #VALIDATION
            if len(name)>100 or not str(duration).isdigit() :
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./song/"+fileName
            os.remove("./song/"+update_file.file_name)

            #UPDATING DATA
            update_file.name = name
            update_file.duration = duration
            update_file.upload_time = uploadTime
            update_file.file_name = fileName
            uploadedFile.save(filePath)

            db.session.commit()

        elif audioFileType.lower()=='podcast':
            try:
                update_file=Podcast.query.get(audioFileID)

                name=audioFileMetadata['name']
                duration=audioFileMetadata['duration']
                host=audioFileMetadata['host']
            except:
                return "The request is invalid: 400 bad request",400
            try:
                participants=audioFileMetadata['participants']
                if len(participants)>10 or any(len(participants) > 100 for participant in participants):
                    return "The request is invalid: 400 bad request",400
            except:
                participants=None

            #VALIDATION
            if len(name)>100 or len(host)>100 or not str(duration).isdigit():
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./podcast/"+fileName
            os.remove("./podcast/"+update_file.file_name)

            #UPDATING DATA
            update_file.name = name
            update_file.duration = duration
            update_file.host = host
            update_file.participants = str(participants)
            update_file.upload_time = uploadTime
            update_file.file_name = fileName
            uploadedFile.save(filePath)

            db.session.commit()

        elif audioFileType.lower()=='audiobook':
            try:
                update_file=Audiobook.query.get(audioFileID)

                title=audioFileMetadata['title']
                duration=audioFileMetadata['duration']
                author=audioFileMetadata['author']
                narrator=audioFileMetadata['narrator']
            except:
                return "The request is invalid: 400 bad request",400

            #VALIDATION
            if len(title)>100 or len(author)>100 or len(narrator)>100 or not str(duration).isdigit():
                return "The request is invalid: 400 bad request",400

            uploadTime=datetime.datetime.utcnow()
            fileName = secure_filename(uploadedFile.filename)
            filePath = "./audiobook/"+fileName
            os.remove("./audiobook/"+update_file.file_name)

            #UPDATING DATA
            update_file.title = title
            update_file.duration = duration
            update_file.author = author
            update_file.narrator = narrator
            update_file.upload_time = uploadTime
            update_file.file_name = fileName
            uploadedFile.save(filePath)

            db.session.commit()

        else:
            return "The request is invalid: 400 bad request",400

        return "Action is successful: 200 OK",200
    except:
        return "500 internal server error", 500


#DELETE ROUTE
@app.route('/delete/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete(audioFileType,audioFileID):
    try:
        if audioFileType.lower()=='song':
            try:
                delete_file=Song.query.get(audioFileID)
                db.session.delete(delete_file)
            except:
                return "The request is invalid: 400 bad request",400

        elif audioFileType.lower()=='podcast':
            try:
                delete_file=Podcast.query.get(audioFileID)
                db.session.delete(delete_file)
            except:
                return "The request is invalid: 400 bad request",400

        elif audioFileType.lower()=='audiobook':
            try:
                delete_file=Audiobook.query.get(audioFileID)
                db.session.delete(delete_file)
            except:
                return "The request is invalid: 400 bad request",400
        else:
            return "The request is invalid: 400 bad request",400

        db.session().commit()
        return "Action is successful: 200 OK",200

    except:
        return "500 internal server error", 500

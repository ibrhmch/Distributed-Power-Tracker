#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
import base64
import io
import json
import sys
import os
import redis
import uuid
import platform
import time, shutil
from minio import Minio
# python3 rest-server.py
# Initialize the Flask application
app = Flask(__name__)

minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"

client = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

# bucketname="queue"
files_to_add=[ "minio-storage.py", "minio-config.yaml"]

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.DEBUG)

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

# redisHost = "localhost"
# redisPort = 6379

# redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
redisData = redis.StrictRedis(host=redisHost, port=redisPort, decode_responses=True)



@app.route('/newdata/<float:loc_id>/<int:timestamp>', methods=['POST'])
def separate():
    r = request
    id = uuid.uuid4()
    print(id)
    # print(r.data)
    # response = {'sum' : str( a + b)}
    try:    
        song = json.loads(r.data)
        store = json.dumps(song['callback'])
        songname = song['callback']['data']['mp3'].split('/')[-1]
        # print(songname)
        songdata = base64.b64decode(song['mp3'])
        
        # filename = "%s/%s" % str(id), str(songname)
        filename = "%s/%s" % (str(id), songname)
        f = open(songname, 'w+b')
        f.write(songdata)
        # file_stat = sys.getsizeof(songdata)
        f.close()
        try:
            print("NAME OF MP3", filename)
            redisData.lpush('queue', filename)
            client.fput_object(bucketname[0], str(filename), f"./{songname}")
            # print(client.fput_object(bucketname[0], "rest-server.py", f"./rest-server.py"))
            # print(client.fput_object(bucketname, filename+'-f', songname))
            os.remove(songname)
        except:
            print("File put failed")
        
        
        # client.fput_object(bucketname, songname, f"./{songname}")
        # print(filename)
        # for bucket in buckets:
        #     print(f"Bucket {bucket.name}, created {bucket.creation_date}")
        #     try:    
        #         print(f"Objects in {bucket} are originally:")
        #         for thing in client.list_objects(bucket, recursive=True):
        #             print(thing.object_name)
        #     except:
        #         print("Nothing in bucket", bucket)
        response = {'status' : 'got song data', 'uid' : str(id)}
        try:
            # print(redisData.lpush('request:data', 'mp3:%s test:other' % song['callback']['data']['mp3']))
            found = False
            time.sleep(1)
            for thing in client.list_objects(bucketname[0], recursive=True):
                # print("Here ",thing.object_name)
                if str(id) in thing.object_name:
                    found = True
            if found == True:
                print(redisData.lpush('request', '%s' % store))
            else:
                print("Data not put into minio correct!!")
            # print(store)
            # print(redisData.json().set('request', '$', data))
            # print(redisData.rpush('QUEUE', *song['callback']))
            #  print(redisData.lpush('request:data', 'mp3:%s' % song['callback']['data']['mp3']))
        except:
            print("Error pushing callback data")
        # test = redisData.rpop('Callback')
        # print(test)

    except:
        response = {'status' : 'error getting song data'}
    response_pickled = jsonpickle.encode(response)
    
    for bucket in buckets:
        # print(f"Bucket {bucket.name}, created {bucket.creation_date}")
        try:    
            print(f"Objects in {bucket} are:")
            for thing in client.list_objects(bucket, recursive=True):
                print(thing.object_name)
        except:
            # print("Nothing in bucket", bucket)
            pass
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/newdata/getUID/<float:lat>/<float:lon>', methods=['GET'])
def queue():
    r = request
    try:
        # response = {'status' : 'got a queue request' , 'data' : redisData.lpop('request:data')}
        # print(redisData.rpop('QUEUE'))
        # data = json.loads(redisData.lpop('request'))
        # response = {'status' : 'got a queue request' , 'queue' : data}
        queue = redisData.lrange( "queue", 0, -1 )
        response = {'status' : 'got a queue request' , 'queue' : queue}
        print(queue)
        # print('test')
    except:
        response = {'status' : 'error getting out of redis'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/<float:lat>/<float:lon>/<int:timestamp>', methods=['GET'])
def returndata(UID, tracktype):
    print("%s/%s" % (UID, tracktype))
    filepath = "%s/%s.mp3" % (UID, tracktype)
    found = False
    for thing in client.list_objects(bucketname[1], recursive=True):
        # print(thing.object_name)
        if filepath == thing.object_name:
            found = True
    if found:
        try:
            client.fget_object(bucketname[1], filepath, filepath)
            response = {"status" : "Found requested file",
                        "filename" : "%s" % filepath.split('/')[-1] ,
                        "mp3": base64.b64encode( open(filepath, "rb").read() ).decode('utf-8')}
            shutil.rmtree(UID)

        except:
            print("Could not OPEN file from minio")
            response = {"status" : "Could not OPEN requested file"}
    else:
        response = {"status" : "Could not FIND requested file"}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

    print("To send data back")
# start flask app
# print(redisData.set('TEST' , 'testdata'))
# print(redisData.get('TEST'))   

bucketname=["queue", "output"]
# while True:
for i in bucketname:
    if not client.bucket_exists(i):
        print(f"Create bucket {i}")
        client.make_bucket(i)

buckets = client.list_buckets()

for bucket in buckets:
    print(f"Bucket {bucket.name}, created {bucket.creation_date}")
    try:    
        print(f"Objects in {bucket} are originally:")
        for thing in client.list_objects(bucket, recursive=True):
            print(thing.object_name)
    except:
        print("Nothing in bucket", bucket)
    
# try:
#     for filename in files_to_add:
#         print(f"Add file {filename} as object {filename}")
#         client.fput_object(bucketname, filename, f"./{filename}")
# except:
#     print("Error when adding files the first time")
#     # print(err)

# print(f"Objects in {bucketname} are now:")
# for thing in client.list_objects(bucketname, recursive=True):
#     print(thing.object_name)

sys.stdout.flush()
app.run(host="0.0.0.0", port=5000)
# time.sleep(10)
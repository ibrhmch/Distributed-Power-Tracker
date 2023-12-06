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
import csv
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

c_year = 0
c_month = 1
c_day = 2
c_hour = 3
c_minute = 4
c_generation = 5
c_capacity = 6


@app.route('/newdata/<int:loc_id>', methods=['POST'])
def add_data(loc_id):
    r = request
    data = json.loads(r.data)
    new_time_data = data['year'] +","+data['month'] +","+data['day']+ ","+data['hour']+"," + data['minute'] + "," + data['generation'] + "," + data['capacity'] + "\n"#setup the csv line. 
    print("PUT: ", new_time_data)
    filename = "%s/data.csv" % (str(loc_id))
    print("FILE: ", filename)
    response = ""
    found = False
    for thing in client.list_objects(bucketname[0], recursive=True):
        print("File: ", thing.object_name)
        if filename == thing.object_name:
            found = True
            # 
            try:
                client.fget_object(bucketname[0], filename, filename)
                client.remove_object(bucketname[0], filename, None)
                response = {"status" : "OK"}
                
                f = open(filename, "a")
                f.write(new_time_data)
                f.close()
                
                client.fput_object(bucketname[0], str(filename), str(filename))
                shutil.rmtree(str(loc_id))
            except:
                response = {"status" : "Failure in minio"}
            break
    if found == False:
        try:
            f = open("data.csv", 'a')
            f.write(new_time_data)
            f.close()
            client.fput_object(bucketname[0], str(filename), f"./data.csv")
            response = {"status" : "Made new"}
        except:
            response = {"status" : "Failure creating file in minio"}
            print("Could not make file in minio")
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

#DONE 12/5 will take in location data and give back a UID and push to redis queue named 'mapping'
@app.route('/newdata/getUID/<float:lat>/<float:lon>', methods=['GET'])
def queue(lat, lon):
    r = request
    UID = uuid.uuid4()
    print(UID)
    response = ""
    try:
        # response = {'status' : 'got a queue request' , 'data' : redisData.lpop('request:data')}

        current = redisData.lrange( "mapping", 0, -1 ) #searches redis queue
        for entry in current:
            print("Found: ", entry)
            splits = entry.split('/')
            print("Broken: ", splits)
            if lat == float(splits[2]) and lon == float(splits[1]):
                response = {'status' : 'Location already exists', 'UID' : splits[0]}
                break
        if response == "":
            response = {'status' : 'Location will be added' , 'UID' : int(UID)}
            redisData.lpush("mapping", "%d/%f/%f" % (UID, lon, lat))
        print(queue)
        # print('test')
    except:
        response = {'status' : 'Error seeing redis entries'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/pulldata/<int:UID>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>', methods=['GET'])
def returndata(UID, year, month, day, hour, minute):
    # print("%s/%s" % (UID, tracktype))
    filepath = "%s/data.csv" % (UID)
    found = False
    for thing in client.list_objects(bucketname[0], recursive=True):
        # print(thing.object_name)
        if filepath == thing.object_name:
            found = True
    if found:
        try:
            client.fget_object(bucketname[0], filepath, filepath)
            # response = {"status" : "Found requested file",
            #             "filename" : "%s" % filepath.split('/')[-1] ,
            #             "mp3": base64.b64encode( open(filepath, "rb").read() ).decode('utf-8')}
            with open(filepath, "r") as file:
                reader = csv.reader(file, delimiter=',')
                found = False
                for row in reader:
                    # print(row[c_year], year)
                    if row[c_year] == str(year):
                        if row[c_month] == str(month):
                            if row[c_day] == str(day):
                                if int(row[c_hour]) == (hour):
                                    if int(row[c_minute]) == (minute):
                                        response = {'status' : 'OK', 'data' : row}
                                        found = True
                                        break
                if found == False:
                    response = {'status' : 'Not found', 'data' : '' }
            shutil.rmtree(str(UID))

        except:
            print("Could not OPEN file from minio")
            response = {"status" : "Could not OPEN requested file"}
    else:
        response = {"status" : "Could not FIND this System"}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

    print("To send data back")
# start flask app
# print(redisData.set('TEST' , 'testdata'))
# print(redisData.get('TEST'))   

@app.route('/pulldata/getUID/<float:lat_min>/<float:lat_max>/<float:lon_min>/<float:lon_max>', methods=['GET'])
def returnuid(lat_min,lat_max,lon_min, lon_max):

    nodes = redisData.lrange( "mapping", 0, -1 )
    output = []
    for node in nodes:
        node = str(node)
        parts = node.split('/')
        UID = parts[0]
        lon = float(parts[1])
        lat = float(parts[2])
        if lon > lon_min and lon < lon_max:
            if lat > lat_min and lat < lat_max:
                output.append(node)
    response = { 'status' : "OK", 'nodes' : output}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

bucketname=["location-data"]
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
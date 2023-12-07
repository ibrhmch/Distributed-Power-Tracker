# Solar Data REST server

This server manages accessing and adding solar data and getting it to be viewed

## To get a UID for a new solar array

Make a request GET /newdata/getUID/<float:lat>/<float:lon>, which will send back json data:
    status: <status>
    UID : <UID>

## Add new time data for a certain array

Make a request POST /newdata/<int:loc_id>, which will send back json data:
    status: <status>

## To get a set of UIDs within a rectangular area

Make a request GET '/pulldata/getUID/<float:lat_min>/<float:lat_max>/<float:lon_min>/<float:lon_max>, which will send back json data:
    status: <status>
    nodes: <array of UIDs in rectangle>

## To get data from a solar array using UID

Make a request GET /pulldata/<int:UID>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>, which will send back json data:
    status: <status>
    data: <row from csv [year,month,day,hour,minute,generation(kw),capacity(kw)]>
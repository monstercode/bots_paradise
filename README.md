This is basically a honeypot that listents to all requests coming to the webserver hitting any URI, and then saves the request data in MongoDB. 
It supports uploads, which are saved in a folder which is not retrievable from the webserver.
The root page has a counter to know how many records are saved up to the moment

To run it:

```docker-compose up -d```

To connect to mongo:

```docker exec -it bots_paradise-master-mongo-1 mongosh```

To make a backup of the mongo collection

```
docker exec -it bots_paradise-master-mongo-1 mongodump
docker cp bots_paradise-master-mongo-1:/dump/main_database/bots_collection.bson .
```

the databse name is hardcoded to main_database and collection is bots_collection

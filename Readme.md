## `Store Application`
This Application Performs CURD Operations like `GET`, `PUT`, `POST`, `UPDATE`
and `DELETE` using RESTAPI
## Prerequisites
* MongoDB 4.4.1
* Python 3.4+
* Kafka 2.12-2.3.0
* zookeeper-3.6.0
## Configuration
#### Mongodb
```
host: localhost 
port: 27017
database: demodb
```
### Kafka
```
host : localhost
port : 9092
```
### Sample JSON GET request
```
http://localhost:8080/products
[{
    "_id" : ObjectId("5f6ed76769bd0cf9f8faface"),
    "product_id" : 3,
    "product_description" : "watch",
    "product_name" : "Sonata",
    "product_price": 26
},
{
    "_id" : ObjectId("5f6ed76769bd0cf9f8faface"),
    "product_id" : 2,
    "product_description" : "artsupplies",
    "product_name" : "Apsara"
}]
```
### Sample JSON POST request
```
http://localhost:8080/products
{
    "product_id" : 3,
    "product_description" : "watch",
    "product_name" : "Sonata"
}
```
### Sample JSON PUT request
```
http://localhost:8080/product/3
{"$set": {"product_name": "Fast track"}}
```
### Sample JSON DELETE request
```
http://localhost:8080/product/3
"product deleted"
```
### Sample Kafka POST request
```
http://localhost:8080/post/topic_name
{
   "product_id" : "1",
   "product_price" : 60
}
```

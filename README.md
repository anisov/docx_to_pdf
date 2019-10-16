# Converter docx -> pdf  

Docker aiohttp microservice for convert docx documents to pdf.
Nginx configured with a load balancer.

Setup
-----

1. Create **docker-compose.yml** based on **docker-compose.yml.sample**. 
2. Create **config/nginx.conf** based on **config/nginx.conf.sample**.
3. Create a **logs** folder in the root of the project.
4. Call: 
```
docker-compose build
docker-compose up -d
----
or
----
docker-compose up -d --build
```

Configuration
-----
You can changed count of load balancer in **nginx config** and **docker-compose.yml**.

docker-compose.yml:
```
converter1:
    build:
      context: .
    restart: on-failure
    networks:
      converter-net:
    volumes:
      - ./logs:/code/logs
```
nginx:
```
upstream converter_balancer {
    server converter1:7777;
    ...
```
You can changed default port:
```
  balancer:
    image: "nginx:1.17.4"
    ports:
      - "7777:80"
```


Example client
-------
You can find test example in **test_client/client.py**. Create **test_client/input.docx** for testing.

Dev run service
-------

For dev run service exec the command in the project directory:
```
python -m code
```
Create **code/logs** folder.

Author
-------
**Anisov Dmitriy**
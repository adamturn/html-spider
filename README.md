# HTML Spider
## Route Description
1. The spider spawns a new requests session, then sends a get request to https://sample.route.wall/
2. To bypass the disclaimer, the spider spoofs a button click with another get request to https://sample.route.wall/bypass/
3. Finally, the spider manually reroutes to the target page at https://sample.route.target/

## Validation Description
1. Parsed names data must get only one regex match each on both aggregate entry and exit flow names.
2. Parsed values data must all match a regex checking for float format.

## Quickstart
After cloning this repository, create a /utils directory at the project root and copy in your config.properties file. Then return to the project root and submit the following commands:

[root@serv]$ sudo docker build --tag spider:1.0 .

[root@serv]$ sudo docker run --name peter spider:1.0

## Docker Clean Up
Use the following command to delete all unused Docker images and containers:

[root@serv]$ sudo docker system prune -a

## gitignore
Ignores pycache, vscode settings, and secrets (config.properties) in /utils.
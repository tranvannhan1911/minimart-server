docker run -it -e MYSQL_NAME=supermarket \
    -e MYSQL_USER=supermarket \
    -e MYSQL_PASSWORD=supermarket \
    -e MYSQL_HOST=127.0.0.1 \
    -e MYSQL_PORT=3306 \
    --network="host" \
    tranvannhan1911/supermarket
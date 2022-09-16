docker run -d -p 8000:8000 \
    -e MYSQL_NAME=$MYSQL_NAME \
    -e MYSQL_USER=$MYSQL_USER \
    -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
    -e MYSQL_HOST=$MYSQL_HOST \
    -e MYSQL_PORT=$MYSQL_PORT \
    --restart on-failure:5 \
    $DOCKER_REPOSITORY_TAG
#!/bin/bash

if [ $BASH != '/bin/bash' ]; then
    echo 'Что-то пошло не так - у вас тут не bash.'
    exit
fi

if [ `lsb_release -s -i` == 'Ubuntu' ]; then

    function check_package {
        if ! dpkg -l | grep -q $1; then
            echo 'installing package' $1
            sudo apt-get install $1 -y
        fi
    }

    sudo apt-get update

    check_package make
    check_package openssl
    check_package apt-transport-https
    check_package ca-certificates
    check_package curl
    check_package software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    sudo apt-get update

    check_package docker-ce

    sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

fi


if [[ ! -f `pwd`'/.env' ]]; then

    function get_random {
        echo `openssl rand -base64 16`
    }

    touch `pwd`'/.env'
    echo "SECRET_KEY=$(get_random)
POSTGRES_DB=$(get_random)
POSTGRES_USER=$(get_random)
POSTGRES_PASSWORD=$(get_random)
POSTGRES_HOST=db
POSTGRES_PORT=5432" > `pwd`'/.env'
fi


if [[ ! -f `~/.ssh/id_rsa.pub` ]]; then
ssh-keygen
ssh-agent /bin/bash
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
fi

echo 'Done.'
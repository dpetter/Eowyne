#!/bin/bash

mysql -u root <<EOF
create database eowyne;
create user 'theoden'@'localhost' identified by 'king';
grant all on eowyne.* to theoden;
exit
EOF

#!/bin/bash

mysql -u root <<EOF
drop database eowyne;
create database eowyne;
grant all on eowyne.* to theoden;
exit
EOF

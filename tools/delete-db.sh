#!/bin/bash

mysql -u root <<EOF
drop database eowyne;
drop user theoden@localhost;
exit
EOF

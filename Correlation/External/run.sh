#!/bin/bash
declare -a list=('cpython' 'httpd' 'memcached' 'openssl' 'redis')

for i in "${list[@]}"
do
	./CountError_2.py $i
done

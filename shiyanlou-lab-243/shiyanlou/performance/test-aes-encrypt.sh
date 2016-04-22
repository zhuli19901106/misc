#/usr/bin/env sh
for i in {1..1000}
do
    openssl enc -aes-128-cbc -in message.txt -out message.aes -k 123456
done


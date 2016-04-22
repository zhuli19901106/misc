#/usr/bin/env sh
for i in {1..1000}
do
    openssl rsautl -decrypt -in message.enc -inkey mykey.pem -out message_decryped.txt
done


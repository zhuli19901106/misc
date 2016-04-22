#/usr/bin/env sh
for i in {1..1000}
do
    openssl rsautl -encrypt -in message.txt -pubin -inkey mypubkey.pem -out message.enc
done


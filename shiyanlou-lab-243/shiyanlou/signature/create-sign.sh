#！/usr/bin/env sh
openssl genrsa -des3 -out myrsaCA.pem 1024
openssl rsa -in myrsaCA.pem -pubout -out myrsapubkey.pem
openssl dgst -sha256 -out example.sha256 -sign myrsaCA.pem example.txt

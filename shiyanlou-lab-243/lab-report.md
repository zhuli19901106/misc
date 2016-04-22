# Advanced OS Lab 9: Public Key Encryption and PKI
### Visit the lab page: [公钥加密与PKI](https://www.shiyanlou.com/courses/243 "公钥加密与 PKI")
(Note: This topic is self-selected from a specified catagory. List of all available labs is [here](https://www.shiyanlou.com/courses/?course_type=all&tag=%E4%BF%A1%E6%81%AF%E5%AE%89%E5%85%A8&page=1).)

---

#### Student Name: Zhu Li
#### Student ID: 2015210959
#### Major: Computer Science, Tsinghua University
#### Organization: Institute of High Performance Computing
#### Instructor: Prof. Jiwu Shu

---

## What's the experiment about?
This lab is about PKI (Public Key Infrastructure) and a basic walk-through of asymmetric data encryption.

---

## Environment setup?
The **Shiyanlou** website provided a web-based virtual machines with Linux OS (the first time I saw such a thing, it was a website called "Koding", pretty cool). Both GUI and plain-text are available, fancy :)

But I supposed it would be easier to do this locally. So I did my homework in my own Ubuntu 14.04 (x64), host installation (i.e. not a virtual machine).

---

## Walk me through the details.
Since the experiment is mostly carried out in text mode, I'd avoid pasting a whole lot of screen captures.

Now I'll paste the **input and output** of each operation down here, one code block at a time.

### Lab 1： Make yourself a "Certificate Authority", of course only locally

1.install **openssl** and **openssl development libs**:

Frist run apt-get update, just to make sure the software source is up to date.

```
zl@vm590lb5500:~$ sudo apt-get update
[sudo] password for zl:

...

Hit http://us.archive.ubuntu.com trusty/multiverse i386 Packages               
Hit http://us.archive.ubuntu.com trusty/main Translation-en                    
Hit http://us.archive.ubuntu.com trusty/multiverse Translation-en              
Hit http://us.archive.ubuntu.com trusty/restricted Translation-en              
Hit http://us.archive.ubuntu.com trusty/universe Translation-en                
Ign http://us.archive.ubuntu.com trusty/main Translation-en_US                 
Ign http://us.archive.ubuntu.com trusty/multiverse Translation-en_US           
Ign http://us.archive.ubuntu.com trusty/restricted Translation-en_US           
Ign http://us.archive.ubuntu.com trusty/universe Translation-en_US             
Fetched 5,348 kB in 1min 9s (77.4 kB/s)                                        
Reading package lists... Done
```

Now install libssl-dev:

```
zl@vm590lb5500:~$ sudo apt-get install libssl-dev
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  account-plugin-windows-live libupstart1 linux-headers-3.16.0-30
  linux-headers-3.16.0-30-generic linux-image-3.16.0-30-generic
  linux-image-extra-3.16.0-30-generic linux-signed-image-3.16.0-30-generic
Use 'apt-get autoremove' to remove them.
The following NEW packages will be installed:
  libssl-dev
0 upgraded, 1 newly installed, 0 to remove and 71 not upgraded.
Need to get 0 B/1,071 kB of archives.
After this operation, 6,325 kB of additional disk space will be used.
Selecting previously unselected package libssl-dev:amd64.
(Reading database ... 255918 files and directories currently installed.)
Preparing to unpack .../libssl-dev_1.0.1f-1ubuntu2.18_amd64.deb ...
Unpacking libssl-dev:amd64 (1.0.1f-1ubuntu2.18) ...
Setting up libssl-dev:amd64 (1.0.1f-1ubuntu2.18) ...
```

2.install bless, a hexadecimal editor:
```
zl@vm590lb5500:~$ sudo apt-get install bless
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  account-plugin-windows-live libupstart1 linux-headers-3.16.0-30
  linux-headers-3.16.0-30-generic linux-image-3.16.0-30-generic
  linux-image-extra-3.16.0-30-generic linux-signed-image-3.16.0-30-generic
Use 'apt-get autoremove' to remove them.
The following NEW packages will be installed:
  bless
0 upgraded, 1 newly installed, 0 to remove and 71 not upgraded.
Need to get 0 B/463 kB of archives.
After this operation, 1,086 kB of additional disk space will be used.
Selecting previously unselected package bless.
(Reading database ... 255929 files and directories currently installed.)
Preparing to unpack .../archives/bless_0.6.0-4_all.deb ...
Unpacking bless (0.6.0-4) ...
Processing triggers for gnome-menus (3.10.1-0ubuntu2) ...
Processing triggers for desktop-file-utils (0.22-1ubuntu1) ...
Processing triggers for bamfdaemon (0.5.1+14.04.20140409-0ubuntu1) ...
Rebuilding /usr/share/applications/bamf-2.index...
Processing triggers for mime-support (3.54ubuntu1.1) ...
Processing triggers for man-db (2.6.7.1-1ubuntu1) ...
Setting up bless (0.6.0-4) ...
```

3.establish a local Certificate Authority (CA) with the following file layout:


```
zl@vm590lb5500:~$ mkdir shiyanlou
zl@vm590lb5500:~$ cd shiyanlou
zl@vm590lb5500:~/shiyanlou$ mkdir demoCA
zl@vm590lb5500:~/shiyanlou$ ln -s /usr/lib/ssl/openssl.cnf openssl.cnf
zl@vm590lb5500:~/shiyanlou$ cd demoCA/
zl@vm590lb5500:~/shiyanlou/demoCA$ mkdir certs
zl@vm590lb5500:~/shiyanlou/demoCA$ mkdir crl
zl@vm590lb5500:~/shiyanlou/demoCA$ touch index.txt
zl@vm590lb5500:~/shiyanlou/demoCA$ mkdir newcerts
zl@vm590lb5500:~/shiyanlou/demoCA$ echo "1234" > serial
zl@vm590lb5500:~/shiyanlou/demoCA$ cd ..
zl@vm590lb5500:~/shiyanlou$ tree
.
├── demoCA
│   ├── certs
│   ├── crl
│   ├── index.txt
│   ├── newcerts
│   └── serial
└── openssl.cnf -> /usr/lib/ssl/openssl.cnf

4 directories, 3 files
```

4.generate a certificate for your local CA

```
zl@vm590lb5500:~/shiyanlou$ openssl req -new -x509 -keyout ca.key -out ca.crt -config openssl.cnf
Generating a 2048 bit RSA private key
.......................+++
..........................................................................................+++
writing new private key to 'ca.key'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
zl@vm590lb5500:~/shiyanlou$ tree
.
├── ca.crt
├── ca.key
├── demoCA
│   ├── certs
│   ├── crl
│   ├── index.txt
│   ├── newcerts
│   └── serial
└── openssl.cnf -> /usr/lib/ssl/openssl.cnf

4 directories, 5 files
```

The password is 123456, other infos are left blank.

Now a pair of key and crt files are generated for the local authority.

### Lab 2: Generate certificate for "PKILabServer.com"
1.Generate public/private key pair

```
zl@vm590lb5500:~/shiyanlou$ openssl genrsa -des3 -out server.key 1024
Generating RSA private key, 1024 bit long modulus
..............................................................++++++
......++++++
e is 65537 (0x10001)
Enter pass phrase for server.key:
Verifying - Enter pass phrase for server.key:
zl@vm590lb5500:~/shiyanlou$ find -cmin -1
.
./server.key
zl@vm590lb5500:~/shiyanlou$ cat server.key
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,FDBEA28798ED0231

7LL2MYadYg44KHcmSrVZsLkgstjXCyo4S/rrZ5m0aqgOBdSvOZogUq2FfkaTTSrC
/Wz8/mKFtjv3Ksf7Z783+boFmk15yez0pthRu8OFEuuCC6sTBAAj/8TrjQXa5TH3
YSwJ2MbvsNl0xRDcNr+hvkmvfcknC7bsLSpmnqQCcmZeHYCh5Ego/2pge/MxnAql
YqYfoJ3jpnR8fQzqevKAxd2IFR7x6Zeghx6EftZm2DXSqM0kP+KkAn5zWIjmc+ZL
CrG1EDdPXQKVf/i+lXnCejwhVm6keNcmZGD9kF9pVzV8hnDfwZ6dchxzJcAO708X
TKGmdOl++i+b3EtOSOZ1XKYfORaqxBJ/JdK56BLcHJ65i8Qq84Ln7Y+iUJrOvB+6
tqXTULFoAJQfUWONgugno0iW91PmyJndWa5MVrzM7zN/KayWvgmgQVRdM0vgWCZH
fNA9+34xi8aROENXhrD32p3sDF9x7FuRft62oWoKE28y4rbLU+9IqVJeKbv2m8rk
4u54FtktiCIpYdK98CHCuDmwq69Sb8x3B+ij40mmUGQPLFEAJC+tDgPnhnWKM9bT
uRlp67MuvNmK6RfSMpjqejMEZYK6h+2p8MDFP4Sq1XVb7BLZWSqpVdN9BGtiZee6
avAY/dh9UrUZZKqWUx0s57KEU2f7n0U6kSp2QZTxyfiUY3h7uiiAKw5T/Xc4Gw40
snP1CuJQyDZmStlyf8yKemNQ+/Pt4aQMf3icR2l4v1PZORu6ydQWLyMmR+KEM1O1
80eWZCQXq5cBDBj7S0yisnnlEaaT78S+osGvfokr7yPSVqTtOqU/eg==
-----END RSA PRIVATE KEY-----
```
The newly generated server.key contains the private key for the server. The "find" command finds out the files that has been modified within the last 2 minutes.

The password is 123456, no surprise.

2.Generate Certificate Signature Request (CSR)

```
zl@vm590lb5500:~/shiyanlou$ openssl req -new -key server.key -out server.csr -config openssl.cnf
Enter pass phrase for server.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:PKILabServer.com
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
zl@vm590lb5500:~/shiyanlou$ find -cmin -1
.
./server.csr
zl@vm590lb5500:~/shiyanlou$ cat server.csr
-----BEGIN CERTIFICATE REQUEST-----
MIIBoDCCAQkCAQAwYDELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUx
ITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEZMBcGA1UEAwwQUEtJ
TGFiU2VydmVyLmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAzyjYLWBW
+a52H4RpbfHI908xcj6O6EyVTYYO55sonmhv93OyVfq4t1iOUQWhSKiFAc9gHpAu
F5y1rV0mu0OeyYvnaB0upmzzT+dvZWg7itWlO8Nek42iTJOrBpcQHrHYMBT7DosK
1HKkSwKPM7KUR9suqGboChFSEgBW6Bga3iECAwEAAaAAMA0GCSqGSIb3DQEBCwUA
A4GBAABSv4HtumaaTk/5X8/4oDsNwk5978tdbpEj1UtopOdQcYnac0yHFjttf6py
1/s2LqcRefqlpuaPhV13Ud6LxiFvfXhEGdAcC5ltcqNNuM9vScCkma/0XQ5dA23v
OWtK1wLDf3TArrI08yx1P+l2f17K51BXBGGXBb4uEv29yoDe
-----END CERTIFICATE REQUEST-----
```

The diffenrence is that this time the "**Common Name**" is set to "PKILabServer.com", which will be used later in identity verification.

3.Generate the certificate for this domain name.

```
zl@vm590lb5500:~/shiyanlou$ openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key -config openssl.cnf
Using configuration from openssl.cnf
Enter pass phrase for ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4660 (0x1234)
        Validity
            Not Before: Apr 22 13:22:09 2016 GMT
            Not After : Apr 22 13:22:09 2017 GMT
        Subject:
            countryName               = AU
            stateOrProvinceName       = Some-State
            organizationName          = Internet Widgits Pty Ltd
            commonName                = PKILabServer.com
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                E6:B6:E4:BA:16:73:30:BD:20:AF:97:1F:65:32:43:95:FE:E0:47:C3
            X509v3 Authority Key Identifier:
                keyid:C5:54:E1:57:91:C6:54:AB:FC:6A:BF:51:FE:4F:84:34:B6:6A:C0:07

Certificate is to be certified until Apr 22 13:22:09 2017 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated
zl@vm590lb5500:~/shiyanlou$ find -cmin -1
.
./demoCA
./demoCA/serial.old
./demoCA/newcerts
./demoCA/newcerts/1234.pem
./demoCA/index.txt
./demoCA/serial
./demoCA/index.txt.attr
./demoCA/index.txt.old
./server.crt
zl@vm590lb5500:~/shiyanlou$ cat server.crt
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 4660 (0x1234)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=AU, ST=Some-State, O=Internet Widgits Pty Ltd
        Validity
            Not Before: Apr 22 13:22:09 2016 GMT
            Not After : Apr 22 13:22:09 2017 GMT
        Subject: C=AU, ST=Some-State, O=Internet Widgits Pty Ltd, CN=PKILabServer.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (1024 bit)
                Modulus:
                    00:cf:28:d8:2d:60:56:f9:ae:76:1f:84:69:6d:f1:
                    c8:f7:4f:31:72:3e:8e:e8:4c:95:4d:86:0e:e7:9b:
                    28:9e:68:6f:f7:73:b2:55:fa:b8:b7:58:8e:51:05:
                    a1:48:a8:85:01:cf:60:1e:90:2e:17:9c:b5:ad:5d:
                    26:bb:43:9e:c9:8b:e7:68:1d:2e:a6:6c:f3:4f:e7:
                    6f:65:68:3b:8a:d5:a5:3b:c3:5e:93:8d:a2:4c:93:
                    ab:06:97:10:1e:b1:d8:30:14:fb:0e:8b:0a:d4:72:
                    a4:4b:02:8f:33:b2:94:47:db:2e:a8:66:e8:0a:11:
                    52:12:00:56:e8:18:1a:de:21
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                E6:B6:E4:BA:16:73:30:BD:20:AF:97:1F:65:32:43:95:FE:E0:47:C3
            X509v3 Authority Key Identifier:
                keyid:C5:54:E1:57:91:C6:54:AB:FC:6A:BF:51:FE:4F:84:34:B6:6A:C0:07

    Signature Algorithm: sha256WithRSAEncryption
         36:81:d6:d1:15:de:c1:d8:c6:46:af:ec:79:cc:1b:95:20:1c:
         22:c5:d7:0a:73:a8:01:bc:c4:05:a3:0c:bb:d2:75:af:32:f4:
         ec:c3:3e:94:20:7d:0c:98:e3:66:36:00:c2:e0:b1:d2:a4:e1:
         e6:fc:47:3c:55:1d:9c:b6:57:6d:1d:ac:48:96:d4:3e:0b:d8:
         eb:38:ed:18:05:e8:2d:21:6c:78:d7:95:e6:ac:ac:d7:22:68:
         72:68:aa:09:da:7e:e5:fd:e3:1e:0e:86:74:36:4b:e3:0f:7a:
         67:38:ea:f6:3d:2e:e6:8d:1a:11:09:ea:fd:cb:d3:b8:a8:77:
         3a:e4:c5:70:4a:30:f6:67:99:37:7b:7b:b8:36:ed:02:12:e4:
         a8:7f:09:51:7c:2f:e1:97:e2:2c:e2:f4:36:32:9d:15:62:69:
         90:bd:9b:14:7c:14:8f:f1:39:0f:1a:ef:64:bb:74:be:4d:c0:
         1f:61:3e:84:8d:46:74:e4:30:a0:da:de:29:e4:f8:27:de:d9:
         da:6e:cb:58:c4:4d:a8:e0:76:47:b7:1f:0e:e0:23:24:86:df:
         00:cd:8d:27:72:bd:37:56:8e:9f:d2:d6:0e:62:be:f2:4a:71:
         6d:fc:da:63:7e:60:d1:c8:73:08:b4:18:26:b0:08:01:7f:7a:
         4c:65:a7:0e
-----BEGIN CERTIFICATE-----
MIIDGDCCAgCgAwIBAgICEjQwDQYJKoZIhvcNAQELBQAwRTELMAkGA1UEBhMCQVUx
EzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMg
UHR5IEx0ZDAeFw0xNjA0MjIxMzIyMDlaFw0xNzA0MjIxMzIyMDlaMGAxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQxGTAXBgNVBAMMEFBLSUxhYlNlcnZlci5jb20wgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBAM8o2C1gVvmudh+EaW3xyPdPMXI+juhMlU2G
DuebKJ5ob/dzslX6uLdYjlEFoUiohQHPYB6QLhecta1dJrtDnsmL52gdLqZs80/n
b2VoO4rVpTvDXpONokyTqwaXEB6x2DAU+w6LCtRypEsCjzOylEfbLqhm6AoRUhIA
VugYGt4hAgMBAAGjezB5MAkGA1UdEwQCMAAwLAYJYIZIAYb4QgENBB8WHU9wZW5T
U0wgR2VuZXJhdGVkIENlcnRpZmljYXRlMB0GA1UdDgQWBBTmtuS6FnMwvSCvlx9l
MkOV/uBHwzAfBgNVHSMEGDAWgBTFVOFXkcZUq/xqv1H+T4Q0tmrABzANBgkqhkiG
9w0BAQsFAAOCAQEANoHW0RXewdjGRq/secwblSAcIsXXCnOoAbzEBaMMu9J1rzL0
7MM+lCB9DJjjZjYAwuCx0qTh5vxHPFUdnLZXbR2sSJbUPgvY6zjtGAXoLSFseNeV
5qys1yJocmiqCdp+5f3jHg6GdDZL4w96Zzjq9j0u5o0aEQnq/cvTuKh3OuTFcEow
9meZN3t7uDbtAhLkqH8JUXwv4ZfiLOL0NjKdFWJpkL2bFHwUj/E5DxrvZLt0vk3A
H2E+hI1GdOQwoNreKeT4J97Z2m7LWMRNqOB2R7cfDuAjJIbfAM2NJ3K9N1aOn9LW
DmK+8kpxbfzaY35g0chzCLQYJrAIAX96TGWnDg==
-----END CERTIFICATE-----
```

This time we get a lot of output. This is because a new entry is written to the database of the local CA. Notice the new file is "server.crt", while a lot of files in "demoCA" is modified.

### Lab 3: Use your certificates on websites
1.Add the domain name "PKILabServer.com" to your **hosts**

```
zl@vm590lb5500:~/shiyanlou$ sudo vi /etc/hosts
```
```
1 127.0.0.1   localhost
2 127.0.1.1   vm590lb5500
3 127.0.0.1   PKILabServer.com
```

After adding a new domain name, restart the network.

```
zl@vm590lb5500:~/shiyanlou$ sudo /etc/init.d/networking restart
```

2.Create a certified web server with the following commands

Piece the public and private key together into a file called "server.pem".

Start the a web server with openssl with secure connection.

```
zl@vm590lb5500:~/shiyanlou$ cat server.key >> server.pem
zl@vm590lb5500:~/shiyanlou$ cat server.crt >> server.pem
zl@vm590lb5500:~/shiyanlou$ openssl s_server -cert server.pem -www
Enter pass phrase for server.pem:
Using default temp DH parameters
Using default temp ECDH parameters
ACCEPT
```

After running the command, the terminal will be used for log output, i.e. it is hanged up.

So we'll start a new tab in the terminal.

3.See what happens when visiting https://PKILabServer.com:4433/

Now we'll visit website, just as expected, we're blocked and warned of possible risk of being eavesdropped.

![visit-without-being-certified](./visit-without-being-certified.png)


4.Import the local CA's certificate into the browser you're using, see if it works

Now we'll add the CA certificate as instructed.

![adding-certificate-for-the-local-authority](./adding-certificate-for-the-local-authority.png)

Nothing changes after adding the CA certificate. **Turned out it doesn't work on Firefox.**

**Now we do the same on Chrome, it did worked.** The details are similar and will be omitted for simplicity.

![visit-after-being-certified](./visit-after-being-certified.png)

5.What if you change the domain name to "localhost" or simply "127.0.0.1"?

Again, we're blocked and warned. This is because **we don't have a certificate for "localhost" at the local CA**. The same with "127.0.0.1".

![visit-with-a-different-name](./visit-with-a-different-name.png)

I think this policy is especially important for the **security of an private cluster**. If you intercept the IP of a machine (hacking or whatever), you still won't be able to visit it if you don't know the certified domain name (which is often kept confidential).

That's why an attempt visit simply by the IP will usually be rejected, as long as you're directing this attempt from an untrusted client.

### Lab 4: Establish secure TCP connection to PKILabServer.com with PKI
1.Download the client-server demo program from the given URL and try it.

As I already got the ZIP archive from the given URL, now let's try it.

```
zl@vm590lb5500:~/shiyanlou$ ll demo_openssl_api.zip
-rw-rw-r-- 1 zl zl 11603 Apr 22 09:27 demo_openssl_api.zip
zl@vm590lb5500:~/shiyanlou$ unzip demo_openssl_api.zip
Archive:  demo_openssl_api.zip
   creating: demo_openssl_api/
  inflating: demo_openssl_api/ca.crt  
  inflating: demo_openssl_api/cli.cpp  
  inflating: demo_openssl_api/client.crt  
  inflating: demo_openssl_api/client.key  
  inflating: demo_openssl_api/Makefile  
  inflating: demo_openssl_api/README  
  inflating: demo_openssl_api/serv.cpp  
  inflating: demo_openssl_ahe password entered are server and client accordingly.pi/server.crt  
  inflating: demo_openssl_api/server.key  
zl@vm590lb5500:~/shiyanlou$ tree demo_openssl_api
demo_openssl_api
├── ca.crt
├── cli.cpp
├── client.crt
├── client.key
├── Makefile
├── README
├── serv.cpp
├── server.crt
└── server.key

0 directories, 9 files
zl@vm590lb5500:~/shiyanlou$ cd demo_openssl_api/
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ cat README
1. The password for the server side is ``server'' (without quote)
2. The password for the client side is ``client'' (without quota)
```

Now let's run the client and server demo. The order should be server first and client second. (Otherwise the client will fail to connect to any server and exit with error.)

```
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ make
g++ -I/usr/local/ssl/include/ -L/usr/local/ssl/lib/ cli.cpp -o cli -lssl -lcrypto -ldl -fpermissive
cli.cpp: In function ‘int main()’:
cli.cpp:46:31: warning: invalid conversion from ‘const SSL_METHOD* {aka const ssl_method_st*}’ to ‘SSL_METHOD* {aka ssl_method_st*}’ [-fpermissive]
   meth = SSLv23_client_method();
                               ^
g++ -I/usr/local/ssl/include/ -L/usr/local/ssl/lib/ serv.cpp -o serv -lssl -lcrypto -ldl -fpermissive
serv.cpp: In function ‘int main()’:
serv.cpp:59:31: warning: invalid conversion from ‘const SSL_METHOD* {aka const ssl_method_st*}’ to ‘SSL_METHOD* {aka ssl_method_st*}’ [-fpermissive]
   meth = SSLv23_server_method();
                               ^
serv.cpp:101:66: error: cannot convert ‘size_t* {aka long unsigned int*}’ to ‘socklen_t* {aka unsigned int*}’ for argument ‘3’ to ‘int accept(int, sockaddr*, socklen_t*)’
   sd = accept (listen_sd, (struct sockaddr*) &sa_cli, &client_len);
                                                                  ^
serv.cpp:106:43: warning: format ‘%lx’ expects argument of type ‘long unsigned int’, but argument 2 has type ‘in_addr_t {aka unsigned int}’ [-Wformat=]
    sa_cli.sin_addr.s_addr, sa_cli.sin_port);
                                           ^
make: *** [all] Error 1
```

After running "make", there seems to be an error, so let's correct it:

```
100   client_len = sizeof(sa_cli);
101   sd = accept (listen_sd, (struct sockaddr*) &sa_cli, &client_len);                                                                        
102   CHK_ERR(sd, "accept");
```

Look at the "&client_len" parameter, it should be change to "(socklen_t *)&client_len", actually it's about type casting.

Although "socklen_t" and "size_t" are both "unsigned int" for most of the time, but implicit conversion is not possible.

After correction, it looks like this:

```
100   client_len = sizeof(sa_cli);
101   sd = accept (listen_sd, (struct sockaddr*) &sa_cli, (socklen_t *) &client_len);                                                          
102   CHK_ERR(sd, "accept");
```

Now let's make again.

```
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ make clean
rm -rf *~ cli serv
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ make
g++ -I/usr/local/ssl/include/ -L/usr/local/ssl/lib/ cli.cpp -o cli -lssl -lcrypto -ldl -fpermissive
cli.cpp: In function ‘int main()’:
cli.cpp:46:31: warning: invalid conversion from ‘const SSL_METHOD* {aka const ssl_method_st*}’ to ‘SSL_METHOD* {aka ssl_method_st*}’ [-fpermissive]
   meth = SSLv23_client_method();
                               ^
g++ -I/usr/local/ssl/include/ -L/usr/local/ssl/lib/ serv.cpp -o serv -lssl -lcrypto -ldl -fpermissive
serv.cpp: In function ‘int main()’:
serv.cpp:59:31: warning: invalid conversion from ‘const SSL_METHOD* {aka const ssl_method_st*}’ to ‘SSL_METHOD* {aka ssl_method_st*}’ [-fpermissive]
   meth = SSLv23_server_method();
                               ^
serv.cpp:106:43: warning: format ‘%lx’ expects argument of type ‘long unsigned int’, but argument 2 has type ‘in_addr_t {aka unsigned int}’ [-Wformat=]
    sa_cli.sin_addr.s_addr, sa_cli.sin_port);
                                           ^
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ find -cmin -2
.
./serv
./cli
```

Now run the server and client demo:

```
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ ./serv
Enter PEM pass phrase:
Connection from 100007f, port 8d86
SSL connection using AES256-GCM-SHA384
Client certificate:
	 subject: /C=US/ST=New York/L=Syracuse/O=SEED Labs Inc./OU=PKI Lab/CN=PKILabClient.com/emailAddress=admin@PKILabClient.com
	 issuer: /C=US/ST=New York/L=Syracuse/O=SEED Labs Inc./OU=PKI Lab/CN=PKILabCA.com/emailAddress=admin@PKILabCA.com
Got 12 chars:'Hello World!'
```

```
zl@vm590lb5500:~/shiyanlou/demo_openssl_api$ ./cli
Enter PEM pass phrase:
SSL connection using AES256-GCM-SHA384
Server certificate:
	 subject: /C=US/ST=New York/L=Syracuse/O=SEED Labs Inc./OU=PKI Lab/CN=PKILabServer.com/emailAddress=admin@PKILabServer.com
	 issuer: /C=US/ST=New York/L=Syracuse/O=SEED Labs Inc./OU=PKI Lab/CN=PKILabCA.com/emailAddress=admin@PKILabCA.com
Got 11 chars:'I hear you.'
```

The password entered are "server" and "client" accordingly.

The server program was hanged up at startup. When the client program started, both programs exited successfully with a message.

Server got greeted by the client: Hello World!

Client got responded by the server: I hear you.

### Lab 5: Performance comparison between RSA and AES
1.Prepare a "message.txt" with 16 bytes of data.

```
zl@vm590lb5500:~/shiyanlou$ mkdir performance
zl@vm590lb5500:~/shiyanlou$ cd  performance/
zl@vm590lb5500:~/shiyanlou/performance$ echo "abcdefghijklmno" > message.txt
zl@vm590lb5500:~/shiyanlou/performance$ ll
total 12
drwxrwxr-x 2 zl zl 4096 Apr 22 11:58 ./
drwxrwxr-x 5 zl zl 4096 Apr 22 11:58 ../
-rw-rw-r-- 1 zl zl   16 Apr 22 11:58 message.txt
```

Normally Linux text file ends with a LINE FEED, so there are only 15 letters here.

2.Encrypt it with public key.

Generate private key:

```
zl@vm590lb5500:~/shiyanlou/performance$ openssl genrsa -out mykey.pem 1024
Generating RSA private key, 1024 bit long modulus
..............................................................++++++
................................................................++++++
e is 65537 (0x10001)
zl@vm590lb5500:~/shiyanlou/performance$ find -cmin -1
.
./mykey.pem
zl@vm590lb5500:~/shiyanlou/performance$ cat mykey.pem
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDyoFnj4hE3nkbhuOyZiZpM/GTqh7Doxfo3P3A5QzCDZbXMW8Ss
5iozbyIUHUtRddQj0hVu5q3rYugi4TyOOg75CFsHWXuMbUuJLLwjbdpi96uGo3tO
3ZT1iDrUAn/eqT+ToMZkwpH3X8ytTZY6/Z9yvQk37O8q6GpFvAmI/iqCNQIDAQAB
AoGBAJhB5ocqbBGSIvst2FR11L3xOccwBeXdr6sSBXP55SzgHBk1kZPLELqcSC+F
PqnNHqaoBMlGu+fWdsTEwgKjDpciR5CM5MJ6j6l48HutWlJQ+Wowq/ZaKNVUvzEU
0O92P5VnfQ2AiNMrVp3hXkjAOJQ809yfijU045dS7njRFto1AkEA+voIJeVNuUcK
zABzwHpXtdhPaGF2fzxn2bLp01MalHSSmsqQLQBhBO8uzeGSg5Fb6mXi0rTI6Npl
F/IREAIcjwJBAPd7iJN4EmaLh8eO1YFayt4oeS4gve6LWXp9ZXAdwbPIL7hUJtBm
2221Xm4AeSdwl0cczZieu0PVvcekSiakXvsCQQDkhipJJ0PgQpnIK1k6l6upvq5/
Ys9dB4mgJlLWw0Lejk63d15UO5YbwhYiDRU1i3PgOKmSJl8R91o5tYZnxyRtAkBs
l8stElHYpz8UJKuwz/sWkmHiCMHuqzy/D8jz8kqtrZiq5FoHtipwsFXYJOMEmFX5
AT2By5zWPjLBKGjVHekDAkEA17LmJ41BVqpOmfYimuUZzh2qtQH/NHjCidIkCr4G
0+XQsvGxQagBiEyCdS2/gUlEyzjnvt3G3ODoskVgH+UPrQ==
-----END RSA PRIVATE KEY-----
```

Generate public key:

```
zl@vm590lb5500:~/shiyanlou/performance$ openssl rsa -in mykey.pem -pubout -out mypubkey.pem
writing RSA key
zl@vm590lb5500:~/shiyanlou/performance$ find -cmin -1
.
./mypubkey.pem
zl@vm590lb5500:~/shiyanlou/performance$ cat mypubkey.pem
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDyoFnj4hE3nkbhuOyZiZpM/GTq
h7Doxfo3P3A5QzCDZbXMW8Ss5iozbyIUHUtRddQj0hVu5q3rYugi4TyOOg75CFsH
WXuMbUuJLLwjbdpi96uGo3tO3ZT1iDrUAn/eqT+ToMZkwpH3X8ytTZY6/Z9yvQk3
7O8q6GpFvAmI/iqCNQIDAQAB
-----END PUBLIC KEY-----
```

Now we encrypt the message for 1000 times and times the process.
```
zl@vm590lb5500:~/shiyanlou/performance$ cat test-pub-encrypt.sh
#/usr/bin/env sh
for i in {1..1000}
do
    openssl rsautl -encrypt -in message.txt -pubin -inkey mypubkey.pem -out message.enc
done

zl@vm590lb5500:~/shiyanlou/performance$ time ./test-pub-encrypt.sh

real	0m2.577s
user	0m1.069s
sys	0m1.479s
```

So the **average encryption time is 2.577ms**.

3.Decrypt it with private key.

```
zl@vm590lb5500:~/shiyanlou/performance$ cat test-priv-decrypt.sh
#/usr/bin/env sh
for i in {1..1000}
do
    openssl rsautl -decrypt -in message.enc -inkey mykey.pem -out message_decryped.txt
done

zl@vm590lb5500:~/shiyanlou/performance$ time ./test-priv-decrypt.sh

real	0m2.907s
user	0m1.429s
sys	0m1.488s
```

After running 1000 times, the average time of encryption is 2.907ms.

4.Encrypt the file with AES-128.

```
zl@vm590lb5500:~/shiyanlou/performance$ cat test-aes-encrypt.sh
#/usr/bin/env sh
for i in {1..1000}
do
    openssl enc -aes-128-cbc -in message.txt -out message.aes -k 123456
done

zl@vm590lb5500:~/shiyanlou/performance$ time ./test-aes-encrypt.sh

real	0m2.569s
user	0m0.986s
sys	0m1.549s
```

So the average time is 2.569ms.

6.Run standardized test on RSA and AES, see how fast they are.

Run the standardized test for RSA:

```
zl@vm590lb5500:~/shiyanlou/performance$ openssl speed rsa
Doing 512 bit private rsa's for 10s: 184837 512 bit private RSA's in 9.99s
Doing 512 bit public rsa's for 10s: 2452646 512 bit public RSA's in 9.99s
Doing 1024 bit private rsa's for 10s: 63074 1024 bit private RSA's in 9.99s
Doing 1024 bit public rsa's for 10s: 911658 1024 bit public RSA's in 9.99s
Doing 2048 bit private rsa's for 10s: 8282 2048 bit private RSA's in 9.99s
Doing 2048 bit public rsa's for 10s: 273940 2048 bit public RSA's in 9.99s
Doing 4096 bit private rsa's for 10s: 1088 4096 bit private RSA's in 10.00s
Doing 4096 bit public rsa's for 10s: 74753 4096 bit public RSA's in 9.99s
OpenSSL 1.0.1f 6 Jan 2014
built on: Mon Feb 29 18:11:15 UTC 2016
options:bn(64,64) rc4(16x,int) des(idx,cisc,16,int) aes(partial) blowfish(idx)
compiler: cc -fPIC -DOPENSSL_PIC -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -m64 -DL_ENDIAN -DTERMIO -g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2 -Wl,-Bsymbolic-functions -Wl,-z,relro -Wa,--noexecstack -Wall -DMD32_REG_T=int -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM
                  sign    verify    sign/s verify/s
rsa  512 bits 0.000054s 0.000004s  18502.2 245510.1
rsa 1024 bits 0.000158s 0.000011s   6313.7  91257.1
rsa 2048 bits 0.001206s 0.000036s    829.0  27421.4
rsa 4096 bits 0.009191s 0.000134s    108.8   7482.8
```

I guess the relation is approximately O(n^2)?

Run the standardized test for AES:

```
zl@vm590lb5500:~/shiyanlou/performance$ openssl speed aes
Doing aes-128 cbc for 3s on 16 size blocks: 21047079 aes-128 cbc's in 3.00s
Doing aes-128 cbc for 3s on 64 size blocks: 5820733 aes-128 cbc's in 2.99s
Doing aes-128 cbc for 3s on 256 size blocks: 1484692 aes-128 cbc's in 3.00s
Doing aes-128 cbc for 3s on 1024 size blocks: 373560 aes-128 cbc's in 3.00s
Doing aes-128 cbc for 3s on 8192 size blocks: 46667 aes-128 cbc's in 3.00s
Doing aes-192 cbc for 3s on 16 size blocks: 17853817 aes-192 cbc's in 3.00s
Doing aes-192 cbc for 3s on 64 size blocks: 4900493 aes-192 cbc's in 2.99s
Doing aes-192 cbc for 3s on 256 size blocks: 1254649 aes-192 cbc's in 3.00s
Doing aes-192 cbc for 3s on 1024 size blocks: 314941 aes-192 cbc's in 3.00s
Doing aes-192 cbc for 3s on 8192 size blocks: 39612 aes-192 cbc's in 3.00s
Doing aes-256 cbc for 3s on 16 size blocks: 15751815 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 64 size blocks: 4232076 aes-256 cbc's in 2.99s
Doing aes-256 cbc for 3s on 256 size blocks: 1065739 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 1024 size blocks: 265443 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 8192 size blocks: 33297 aes-256 cbc's in 3.00s
OpenSSL 1.0.1f 6 Jan 2014
built on: Mon Feb 29 18:11:15 UTC 2016
options:bn(64,64) rc4(16x,int) des(idx,cisc,16,int) aes(partial) blowfish(idx)
compiler: cc -fPIC -DOPENSSL_PIC -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -m64 -DL_ENDIAN -DTERMIO -g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2 -Wl,-Bsymbolic-functions -Wl,-z,relro -Wa,--noexecstack -Wall -DMD32_REG_T=int -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM
The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-128 cbc     112251.09k   124590.94k   126693.72k   127508.48k   127432.02k
aes-192 cbc      95220.36k   104893.50k   107063.38k   107499.86k   108167.17k
aes-256 cbc      84009.68k    90586.24k    90943.06k    90604.54k    90923.01k
```

Processing rate is sort of stable.

### Lab 6: Generating digest with openssl
1.Prepare a text file "example.txt" with whatever content you want.

```
zl@vm590lb5500:~/shiyanlou$ mkdir signature
zl@vm590lb5500:~/shiyanlou$ cd signature/
zl@vm590lb5500:~/shiyanlou/signature$ echo "This is a sentence." > example.txt
zl@vm590lb5500:~/shiyanlou/signature$ ll
total 12
drwxrwxr-x 2 zl zl 4096 Apr 22 13:12 ./
drwxrwxr-x 6 zl zl 4096 Apr 22 13:12 ../
-rw-rw-r-- 1 zl zl   20 Apr 22 13:12 example.txt
```

2.Use sha256 hash to calculate digest.

```
zl@vm590lb5500:~/shiyanlou/signature$ openssl genrsa -des3 -out myrsaCA.pem 1024
Generating RSA private key, 1024 bit long modulus
........................++++++
.......................++++++
e is 65537 (0x10001)
Enter pass phrase for myrsaCA.pem:
Verifying - Enter pass phrase for myrsaCA.pem:
zl@vm590lb5500:~/shiyanlou/signature$ openssl rsa -in myrsaCA.pem -pubout -out myrsapubkey.pem
Enter pass phrase for myrsaCA.pem:
writing RSA key
zl@vm590lb5500:~/shiyanlou/signature$ openssl dgst -sha256 -out example.sha256 -sign myrsaCA.pem example.txt
Enter pass phrase for myrsaCA.pem:
zl@vm590lb5500:~/shiyanlou/signature$ find -cmin -2
.
./example.sha256
./example.txt
./myrsaCA.pem
./myrsapubkey.pem
```

The new files are **text file, public key, private key and digest in sha256 format**.

3.Verify the digital signature file.

```
zl@vm590lb5500:~/shiyanlou/signature$ cat create-sign.sh
#！/usr/bin/env sh
openssl genrsa -des3 -out myrsaCA.pem 1024
openssl rsa -in myrsaCA.pem -pubout -out myrsapubkey.pem
openssl dgst -sha256 -out example.sha256 -sign myrsaCA.pem example.txt
zl@vm590lb5500:~/shiyanlou/signature$ echo "This is a sentence." > example.txt
zl@vm590lb5500:~/shiyanlou/signature$ ./create-sign.sh
Generating RSA private key, 1024 bit long modulus
..............................++++++
.................++++++
e is 65537 (0x10001)
Enter pass phrase for myrsaCA.pem:
Verifying - Enter pass phrase for myrsaCA.pem:
Enter pass phrase for myrsaCA.pem:
writing RSA key
Enter pass phrase for myrsaCA.pem:
zl@vm590lb5500:~/shiyanlou/signature$ openssl dgst -sha256 -signature example.sha256 -verify myrsapubkey.pem example.txt
Verified OK
```

4.Modify the example.txt and verify the signature again.

After modifying the data, the verification fails.

```
zl@vm590lb5500:~/shiyanlou/signature$ echo "Hello world." >> example.txt
zl@vm590lb5500:~/shiyanlou/signature$ openssl dgst -sha256 -signature example.sha256 -verify myrsapubkey.pem example.txt
Verification Failure
```

After regenerating the public and private keys and digest, the signature passed.

```
zl@vm590lb5500:~/shiyanlou/signature$ cat example.txt
This is a sentence.
Hello world.
zl@vm590lb5500:~/shiyanlou/signature$ ./create-sign.sh
Generating RSA private key, 1024 bit long modulus
..................................++++++
..............++++++
e is 65537 (0x10001)
Enter pass phrase for myrsaCA.pem:
Verifying - Enter pass phrase for myrsaCA.pem:
Enter pass phrase for myrsaCA.pem:
writing RSA key
Enter pass phrase for myrsaCA.pem:
zl@vm590lb5500:~/shiyanlou/signature$ openssl dgst -sha256 -signature example.sha256 -verify myrsapubkey.pem example.txt
Verified OK
```

---
## What have you got after finishing this lab?
System security is cool and challenging, pity it's nothing to do with my field of research.

So, I got my homework done for now.

This is what the directory looked like when it's over:

```
zl@vm590lb5500:~/shiyanlou$ tree
.
├── ca.crt
├── ca.key
├── demoCA
│   ├── certs
│   ├── crl
│   ├── index.txt
│   ├── index.txt.attr
│   ├── index.txt.old
│   ├── newcerts
│   │   └── 1234.pem
│   ├── serial
│   └── serial.old
├── demo_openssl_api
│   ├── ca.crt
│   ├── cli
│   ├── cli.cpp
│   ├── client.crt
│   ├── client.key
│   ├── Makefile
│   ├── README
│   ├── serv
│   ├── serv.cpp
│   ├── server.crt
│   └── server.key
├── demo_openssl_api.zip
├── openssl.cnf -> /usr/lib/ssl/openssl.cnf
├── performance
│   ├── message.aes
│   ├── message_decryped.txt
│   ├── message.enc
│   ├── message.txt
│   ├── mykey.pem
│   ├── mypubkey.pem
│   ├── pass.txt
│   ├── test-aes-encrypt.sh
│   ├── test-priv-decrypt.sh
│   └── test-pub-encrypt.sh
├── server.crt
├── server.csr
├── server.key
├── server.pem
└── signature
    ├── create-sign.sh
    ├── example.sha256
    ├── example.txt
    ├── myrsaCA.pem
    └── myrsapubkey.pem

7 directories, 40 files
```

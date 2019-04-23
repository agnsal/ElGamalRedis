# ElGamalRedis
ElGamal encryption system over a Redis communication channel, attacked with Index Calculus Algorithm.


## How it works
Alice.py, Bob.py and Eve.py are daemon processes that interact via Redis only:
-  Bob.py is a process that creates its own public and private keys, publishes the public one, waits for Alice's message and decrypts it.
-  Eve.py is a sniffer process (Redis channel is public), that uses Index Calculus algorithm to try to solve Discrete Logarithm problems.
-  Alice.py is a process that reads Bob's public key, encrypts a message and sends it to Bob.py.

## How to set up the environment
1. Install Redis (https://redis.io/):
```sh
    sudo apt update
    sudo apt install redis-server
```
2. The supervised directive is set to no by default. If you are running Ubuntu, which uses the systemd init system, find it and change it to systemd:
```sh
    sudo nano /etc/redis/redis.conf
```
3. Resrart Redis:
```sh
    sudo systemctl restart redis.service
```
4. If you don't want Redis to be a startup program:
```sh
    sudo systemctl disable redis
```

## How to run it
1. You have to run Redis first:
```sh
    redis-server
```
2. (Optional) If you want to see what's happening on Redis:
```sh
    redis-cli monitor
```
3. You have to run Bob.py first, Eve.py and finally Alice.py (in that order), because Alice and Eve need to read Bob's public key from Redis and because Eve needs to listen to the channel waiting for Alice's messages.

## Contacts

Agnese Salutari – agneses92@hotmail.it

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.

[https://github.com/agnsal](https://github.com/agnsal)


## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


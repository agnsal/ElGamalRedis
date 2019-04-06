# ElGamalRedis
ElGamal encryption system over a Redis communication channel.

-  https://redis.io/

## How it works
Alice.py, Bob.py and Eve.py are daemon processes that interact via Redis only:
-  Bob.py is a process that creates its own public and private keys, publishes the public one, waits for Alice's message and decrypts it.
-  Eve.py is a sniffer process (Redis channel is public).
-  Alice.py is a process that reads Bob's public key, encrypts a message and sends it to Bob.py.

You have to run these processes in that given order.

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


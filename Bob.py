'''
Copyright 2019 Agnese Salutari.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License
'''

# Dependencies
import ElGamal as eg
import Redis
import ast

RCh = Redis.RedisChannel()
print("Bob creates his ElGamal Keys: ")
BobElGamal = eg.ElGamalEncryption(False, keyFile='Utils/primes50.txt')
print("Bob connects and registers his Public Key on the channel:")
RCh.connect()
RCh.setRedisVariable(varName='BobPublicKey', varValue=str(BobElGamal.getKeys().getPublicKey()))
print("Bob waits for Alice's messages from the channel:")
pubsub = RCh.getRedisDirectly().pubsub()
channelName = 'CommunicationChannel'
pubsub.subscribe(channelName)
for item in pubsub.listen():
    if item['type'] == 'message':
        msg = ast.literal_eval(item['data'].decode('utf-8'))
        print('Message arrived: ' + str(msg))
        r = int(msg[0])
        tVector = msg[1]
        decodedText = BobElGamal.decrypt(r=r, tVector=tVector)
        print('Decoded Text: ' + decodedText)

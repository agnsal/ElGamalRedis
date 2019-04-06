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
import Redis
import ast

RCh = Redis.RedisChannel()
print('Eve connects and reads Bob Public Key from the channel: ')
RCh.connect()
BobPubKey = ast.literal_eval(RCh.getRedisVariable('BobPublicKey').decode('utf-8'))
print('Bob Key is: ' + str(BobPubKey))
print('Eve sniffs the channel, waiting for messages addressed to Bob...')
pubsub = RCh.getRedisDirectly().pubsub()
channelName = 'CommunicationChannel'
pubsub.subscribe(channelName)
for item in pubsub.listen():
    if item['type'] == 'message':
        msg = ast.literal_eval(item['data'].decode('utf-8'))
        print('Message sniffed: ' + str(msg))
        r = int(msg[0])
        tVector = msg[1]
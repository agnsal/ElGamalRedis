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
import IndexCalculusDiscreteLogSolver as IC


print('TEST: x = 2 ########################################################')

ic = IC.IndexCalculus(3, 9, 11)
res = ic.solveDiscreteLog(r=20)


print('TEST: x = 2 ########################################################')
ic = IC.IndexCalculus(6, 36, 101)
res = ic.solveDiscreteLog(r=30)


print('TEST: x = 4, a negative ########################################################')
ic = IC.IndexCalculus(-3, 23, 29)
res = ic.solveDiscreteLog(r=20)


print('TEST: x = 3 ########################################################')
ic = IC.IndexCalculus(7, 343, 15485863)
res = ic.solveDiscreteLog(r=20)



print('TEST: x = 20 #########################################################')
ic = IC.IndexCalculus(45, 2930230, 15485863)
res = ic.solveDiscreteLog(r=20, maxRounds=200)


print('TEST: x = 30, a = 1520  #########################################################')
ic = IC.IndexCalculus(1520, 15203215, 15485863)
res = ic.solveDiscreteLog(r=20, maxRounds=500)

print('TEST: x = 100, a = 16720  #########################################################')
ic = IC.IndexCalculus(16720, 5263484, 15485863)
res = ic.solveDiscreteLog(r=20, maxRounds=1000)



print('Eve connects and reads Bob Public Key from the channel: ')
RCh = Redis.RedisChannel()
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
        ICProblem = IC.IndexCalculus(a=BobPubKey[1], b=BobPubKey[2], p=BobPubKey[0])
        print("Eve tries to calculate Bob's private key via Index Calculus...")
        BobPrivKey = ICProblem.solveDiscreteLog(r=100, maxRounds=1000)
        print("But she can't, because it's too big to compute!")

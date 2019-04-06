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
import redis

class RedisChannel:
    __host = None  # The default value is localhost
    __password = None
    __db = None  # This is the database we are using
    __port = None
    __inputChannel = None  # The channel we eventually want to listen to
    __outputChannel = None  # The channel we have to put outputs into
    __redis = None  # Redis object

    def __init__(self, host='127.0.0.1', password='', db=0, port=6379, inChannel='CommunicationChannel', outChannel='CommunicationChannel'):
        assert isinstance(host, str)
        assert isinstance(password, str)
        assert isinstance(db, int)
        assert isinstance(port, int)
        assert isinstance(inChannel, str)
        assert isinstance(outChannel, str)
        self.__host = host
        self.__password = password
        self.__db = db
        self.__port = port
        self.__inputChannel = inChannel
        self.__outputChannel = outChannel

    def getHost(self):
        return self.__host

    def setHost(self, newHost):
        assert isinstance(newHost, str)
        self.__host = newHost

    def getPassword(self):
        return self.__password

    def setPassword(self, newPassword):
        assert isinstance(newPassword, str)
        self.__password = newPassword

    def getDB(self):
        return self.__db

    def setDB(self, newDB):
        assert isinstance(newDB, int)
        self.__db = newDB

    def getPort(self):
        return self.__port

    def getRedisDirectly(self):
        return self.__redis

    def setPort(self, newPort):
        assert isinstance(newPort, int)
        self.__port = newPort

    def getInputChannel(self):
        return self.__inputChannel

    def setInputChannel(self, newInputChannel):
        assert isinstance(newInputChannel, str)
        self.__inputChannel = newInputChannel

    def getOutputChannel(self):
        return self.__outputChannel

    def setOutputChannel(self, newOutputChannel):
        assert isinstance(newOutputChannel, str)
        self.__outputChannel = newOutputChannel

    def connect(self):
        self.__redis = redis.Redis(host=self.__host, port=self.__port, db=self.__db, password=self.__password)
        if self.__redis.info():
            print('Successfully Connected to Redis.')
        else:
            print('Redis Connection Failed!')

    def redisPublish(self, toPublish):
        str(toPublish)
        self.__redis.publish(channel=self.__outputChannel, message=toPublish)

    def addToRedisQueue(self, queueName, item):
        assert isinstance(queueName, str)
        str(item)
        self.__redis.rpush(queueName, item)

    def takeFromRedisQueue(self, queueName):
        assert isinstance(queueName, str)
        item = self.__redis.rpop(queueName)
        return item

    def readRedisQueue(self, queueName):
        assert isinstance(queueName, str)
        list = self.__redis.lrange(name=queueName, start=0, end=[-1])
        return list

    def readRedisQueueLastElem(self, queueName):
        assert isinstance(queueName, str)
        item = self.__redis.lrange(name=queueName, start=-1, end=-1)[0]
        return item

    def setRedisVariable(self, varName, varValue):
        assert isinstance(varName, str)
        self.__redis.set(name=varName, value=varValue)

    def getRedisVariable(self, varName):
        assert isinstance(varName, str)
        value = self.__redis.get(name=varName)
        return value

    def cleanRedisMemory(self):
        self.__redis.flushall()

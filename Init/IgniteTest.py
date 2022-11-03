from pyignite import Client
# from pyignite.datatypes.cache_config import CacheMode
# from pyignite.datatypes.prop_codes import *
# from pyignite.exceptions import SocketError

client = Client()
# client.connect('127.0.0.1', 10800)
client.connect('433-34.csse.rose-hulman.edu', 10800)
# client.connect('137.112.104.247', 47500)

# Create cache
my_cache = client.get_or_create_cache('my cache')
#Ipokedex = client.get_or_create_cache("Ipokedex")
#INameAndId = client.get_or_create_cache("INameAndId")

# Put value in cache
array = ["1","2"]

my_cache.put("22", array)
print(my_cache.get("22"))
# my_cache.put(2, ['pp-pp',  1, '-'])
# my_cache.put(2, "This is example for CSSE433 class222222")

# Get value from cache
# Ipokedex.remove_key("9100")
# INameAndId.remove_key("c")
#result0 = INameAndId.get("Charizard-Test")
# result0 = Ipokedex.get("9060")
result1 = Ipokedex.get("61")
# INameAndId.remove_all()
# Ipokedex.remove_all()

result0 = INameAndId.get_size()
result1 = Ipokedex.get_size()

#print(result0)
#print(result1)
# print('name to id', result2)
# print('id to detail', result3)
# print(my_cache.get(2))
def add(name, number):
    #if(my_cache.get(name) != None):
        print(type(number))
        array = [name, number]
        dict = {}
        dict[]
        my_cache.put(name, [ 't1'])
        print(my_cache.get(name))


add(1,["a1","a2"])
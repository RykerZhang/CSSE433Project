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
Ipokedex = client.get_or_create_cache("Ipokedex")
INameAndId = client.get_or_create_cache("INameAndId")

# Put value in cache
# my_cache.put(1, 'Hello World')
# my_cache.put(2, ['pp-pp',  1, '-'])
# my_cache.put(2, "This is example for CSSE433 class222222")
# Get value from cache
# Ipokedex.remove_key("10000")
# INameAndId.remove_key("pp-pp")
result1 = Ipokedex.get("10000")
result2 = INameAndId.get("pp-pp")
result3 = INameAndId.get("a")

print(result1)
print(result2)
print(result3)
# print(my_cache.get(2))

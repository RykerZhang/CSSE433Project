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
my_cache.put(1, 'Hello World')
result = my_cache.get(1)
print(result)
# my_cache.put(2, ['pp-pp',  1, '-'])
# my_cache.put(2, "This is example for CSSE433 class222222")

# Get value from cache
# Ipokedex.remove_key("9120")
# INameAndId.remove_key("b")
# result0 = INameAndId.get("b")
# result0 = Ipokedex.get("9060")
# result1 = Ipokedex.get("30")
# INameAndId.remove_all()
# Ipokedex.remove_all()

result0 = INameAndId.get_size()
result1 = Ipokedex.get_size()

print(result0)
print(result1)
# print('name to id', result2)
# print('id to detail', result3)
# print(my_cache.get(2))

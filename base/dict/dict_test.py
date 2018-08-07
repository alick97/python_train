#!/usr/bin/env python3

# dict test

dict1 = {'Name':'user1','Age':1}
print("name:{0} age:{1}".format(dict1['Name'], dict1['Age']))

dict2 = dict(Name='user2',Age=2)
print(str(dict2))

dict3 = dict(zip(['u1','u2','u3'], [1, 2, 3]))
for i in zip(['u1','u2','u3'], [1, 2, 3]):
    print(i)
print(str(dict3))

dict4 = dict([('u1', 1), ('u2', 2)])
print(str(dict4))

its=[it for it in dict({'u1':1, 'u2':2}).items()]
dict5 = dict(its)
print(str(dict5))

its6 = [(i,i+1) for i in [1,2 ,3]]
dict6 = dict(its6)
print(str(dict6))
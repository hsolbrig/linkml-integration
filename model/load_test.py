from pprint import pprint

from linkml_runtime.loaders import YAMLLoader
from test import Kvs, Kvls

input_as_dict = """
entry1: value1
entry2: value2
"""

input_as_list = """
- name: entry1
  value: value1
- name: entry2
  value: value2
"""

input_as_list2 = """
- name: entry1
  value: value1
  another_value: av1
- name: entry2
  another_value: av2
"""

input_as_odd_stuff = """
entry1:
   name: entry1
   value: value1
entry2:
   name: entry2
   value: value2
"""

input_in_a_list_only_world = """
- [entry3, value3]
- [entry4, value4]
"""

# Note that the only form that you can't use with a third value is input_as_dict

loader = YAMLLoader()
v1 = loader.load_any(input_as_dict, Kvs)
v2 = loader.load_any(input_as_list, Kvs)
v3 = loader.load_any(input_as_odd_stuff, Kvs)
v4 = loader.load_any(input_as_list2, Kvs)
v5 = loader.load_any(input_in_a_list_only_world, Kvs)

v1l = loader.load_any(input_as_dict, Kvls)
v2l = loader.load_any(input_as_list, Kvls)
v3l = loader.load_any(input_as_odd_stuff, Kvls)
v4l = loader.load_any(input_as_list2, Kvls)

pprint(v1)
pprint(v2)
pprint(v3)
pprint(v4)
pprint(v5)
print()
pprint(v1l)
pprint(v2l)
pprint(v3l)
pprint(v4l)

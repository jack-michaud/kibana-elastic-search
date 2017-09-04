# kibana-elastic-search

```python
from Elastic.elastic_requests import *

print user_connection_info(username="michaud.j")
print user_connection_info(mac="b005945c6d4d")

'''
{
  'last_connection': {
      'device': u'b005945c6d4d', 
      'username': u'michaud.j', 
      'time': datetime.datetime(2017, 9, 3, 12, 10, 47, tzinfo=tzutc())
   }, 
   'success': True
}
'''

```

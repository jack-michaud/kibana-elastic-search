
from .settings import ElasticSettings

from elasticsearch import Elasticsearch
import datetime
from dateutil import parser
import re
import pytz



mac_regex  = r"dmac=(\d+|\w+)+"
name_regex = r"(?:duser=)(.+?\s)"

find_mac      = lambda string: re.search(mac_regex, string).groups()[0]
find_username = lambda string: re.search(name_regex, string).groups()[0][:-1]
find_time     = lambda string: parser.parse(string)

client = Elasticsearch(ElasticSettings.ELASTIC_SEARCH_URL)

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000

def user_connection_info(username=None, mac=None, date=None):
    '''
    @param username:  MyNEU username ("michaud.j", "lastname.first")
    @param mac:       MAC address (digits 0-9, A-F). Automatically replaces 
                      delineators (: or -)
    @param date:      Fetches data after given date. By default searches 
                      after 60 days ago. Datetime object

    @returns          Dictionary - 
                      {
                          "success": True|False,
                          "last_connection": {
                              "time": datetime|None,
                              "device": str, MAC address,
                              "username": str|None (if failed connection, this will be none)
                          }
                      }
    '''

    if username is None and mac is None:
        raise Exception("Must give either a username or mac (or both)")

    if date is None:
        date = datetime.datetime.now() - datetime.timedelta(days=60)
    
    def generate_search(query):
        return client.search(index=ElasticSettings.ELASTIC_INDEX,
	        body={
		        "query": {
		            "filtered": { "query": {
		                "query_string": {
		                    "analyze_wildcard": True,
		                    "query": query,
		                }
		            }}
		        },
		        "size": 10,
		        "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    },
                ],
                "filter": {
                    "bool": {
                        "must": [{
                            "range": {
                                "@timestamp": {
                                    "gte": int(unix_time_millis(date)),
                                    "lte": int(unix_time_millis(datetime.datetime.now())),
                                    "format": "epoch_millis",
                                } 
                            },
                        }]
                    }
                }
	        }
	    )
    
    def generate_query(query):
        if mac is not None:
            query = query + "AND \"{mac}\" ".format(mac=mac)

        if username is not None:
            query = query + "AND \"{username}\" ".format(username=username)

        return query
    
    if mac is not None:
        mac = mac.lower().replace('-','').replace(':','')
        if set(mac).intersection(set(['1','2','3','4','5', \
                                      '6','7','8','9','0', \
                                      'a','b','c','d','e', \
                                      'f'])) != set(mac) and \
                                    len(mac) == 12:
            raise Exception("Invalid mac address {}".format(mac))

    query = "message:\"NEU-NUResdevice-Device-Allowed\" AND \"outcome=\" "
    query = generate_query(query)

    response = generate_search(query)
	
    # If there are any successful connections, end with success.
    if response['hits']['total'] > 0:
        return { 
            "success": True, 
            "last_connection": {
                "time": find_time(response['hits']['hits'][0]['_source']['@timestamp']),
                "device": find_mac(response['hits']['hits'][0]['_source']['message']),
                "username": find_username(response['hits']['hits'][0]['_source']['message']),
            }
        }

    # Otherwise, check failed connections.

    query = "message:\"[Deny Access Profile]\" "
    query = generate_query(query)

    response = generate_search(query)
	

    if response['hits']['total'] > 0:
        return {
            "success": False,
            "last_connection": {
                "time": None,
                "device": None,
                "username": None,
            }
        }
    else:
        return { 
            "success": False, 
            "last_connection": {
                "time": find_time(response['hits']['hits'][0]['_source']['@timestamp']),
                "device": find_mac(response['hits']['hits'][0]['_source']['message']),
                "username": None
            }
        }
	




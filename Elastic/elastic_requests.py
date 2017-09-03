
from elasticsearch import Elasticsearch
from datetime import datetime
from dateutil import parser

client = Elasticsearch(['155.33.208.205:9200'])

epoch = datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def user_connection_info(username=None, mac=None, date=None):
    '''
    @param username:  MyNEU username ("michaud.j", "lastname.first")
    @param mac:       MAC address (digits 0-9, A-F). Automatically replaces 
                      delineators (: or -)
    @param date:      Fetches data after given date. Datetime object

    @returns          Dictionary - 
                      {
                          "success": True|False,
                          "last_connection": datetime|None 
                      }
    '''
    
    def generate_search(query):
        return client.search(index='logstash-*',
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
                                    "gte": unix_time_millis(date),
                                    "lte": unix_time_millis(datetime.now()),
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
                                      'f'])) != set(mac):
            raise Exception("Invalid mac address {}".format(mac))

    query = "message:\"NEU-NUResdevice-Device-Allowed\" AND \"outcome=\" "
    query = generate_query(query)

    response = generate_search(query)
	
    # If there are any successful connections, end with success.
    if response['hits']['total'] > 0:
        return { 
            "success": True, 
            "last_connection": parser.parse(response['hits']['hits'][0]['_source']['@timestamp']) 
        }

    # Otherwise, check failed connections.

    query = "message:\"[Deny Access Profile]\" "
    query = generate_query(query)

    response = generate_search(query)
	
    return { 
        "success": False, 
        "last_connection": parser.parse(response['hits']['hits'][0]['_source']['@timestamp']) 
    }
	




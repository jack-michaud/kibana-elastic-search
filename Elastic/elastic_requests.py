from .Request import Request
import requests

BASE_URL = "http://155.33.208.205/elasticsearch"
SEARCH_URL = BASE_URL + "/_msearch"
STATS_URL = BASE_URL + "/logstash-*/_field_stats"

# http://155.33.208.205/elasticsearch/logstash-*/_field_stats?level=indices


def msearch_generator():
	querystring = {"timeout":"0","ignore_unavailable":"true","preference":"1503602952189"}

	payload = "{\"index\":[\"{logstash_date}\"],\"search_type\":\"count\",\"ignore_unavailable\":true}\n{\"highlight\":{\"pre_tags\":[\"@kibana-highlighted-field@\"],\"post_tags\":[\"@/kibana-highlighted-field@\"],\"fields\":{\"*\":{}},\"require_field_match\":false,\"fragment_size\":2147483647},\"query\":{\"filtered\":{\"query\":{\"query_string\":{\"query\":\"message:\\\"NEU-NUResdevice-Device-Allowed\\\" AND \\\"outcome=\\\"\",\"analyze_wildcard\":true}},\"filter\":{\"bool\":{\"must\":[{\"query\":{\"match\":{\"host\":{\"query\":\"155.33.208.205\",\"type\":\"phrase\"}}}},{\"query\":{\"match\":{\"programname\":{\"query\":\"CEF\",\"type\":\"phrase\"}}}},{\"query\":{\"match\":{\"sysloghost\":{\"query\":\"155.33.33.90\",\"type\":\"phrase\"}}}},{\"range\":{\"@timestamp\":{\"gte\":1498418997919,\"lte\":1503602997919,\"format\":\"epoch_millis\"}}}],\"must_not\":[]}}}},\"size\":0,\"sort\":[{\"@timestamp\":{\"order\":\"desc\",\"unmapped_type\":\"boolean\"}}],\"aggs\":{\"2\":{\"date_histogram\":{\"field\":\"@timestamp\",\"interval\":\"1d\",\"time_zone\":\"America/New_York\",\"min_doc_count\":0,\"extended_bounds\":{\"min\":1498418997919,\"max\":1503602997919}}}},\"fields\":[\"*\",\"_source\"],\"script_fields\":{},\"fielddata_fields\":[\"@timestamp\"]}\n"
	headers = {
	    'kbn-version': "4.5.4",
	    'content-type': "application/json",
	    'cache-control': "no-cache",
	    }
	return {'querystring': querystring, 'payload': payload, 'headers': headers}

MSEARCH = Request(SEARCH_URL, **msearch_generator())


# encoding = utf-8

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example sends rest requests to some endpoint
    # response is a response object in python requests library
    response = helper.send_http_request("http://www.splunk.com", "GET", parameters=None,
                                        payload=None, headers=None, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()


    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example gets the setup parameters and prints them to the log
    api_key = helper.get_global_setting("api_key")
    helper.log_info("api_key={}".format(api_key))
    log_datadog = helper.get_global_setting("log_datadog")
    helper.log_info("log_datadog={}".format(log_datadog))
    log_index = helper.get_global_setting("log_index")
    helper.log_info("log_index={}".format(log_index))

    # The following example gets the alert action parameters and prints them to the log
    title = helper.get_param("title")
    helper.log_info("title={}".format(title))

    message = helper.get_param("message")
    helper.log_info("message={}".format(message))

    tags = helper.get_param("tags")
    helper.log_info("tags={}".format(tags))

    alert_type = helper.get_param("alert_type")
    helper.log_info("alert_type={}".format(alert_type))

    priority = helper.get_param("priority")
    helper.log_info("priority={}".format(priority))

    aggregation_key = helper.get_param("aggregation_key")
    helper.log_info("aggregation_key={}".format(aggregation_key))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    helper.log_info("Alert action datadog_event started.")
    
    helper.log_debug("helper.settings='{}'".format(helper.settings))

    # TODO: Implement your alert action logic here
    try:
        import json
        import splunklib.client as client
    except Exception as err_message:
        helper.log_error("{}".format(err_message))
        return 1
    
    send_url = 'https://app.datadoghq.com/api/v1/events'

    message = dict()
    message['source_type_name'] = "splunk"
    message['title'] = helper.get_param('title')
    message['text'] = helper.get_param('message')
    message['alert_type'] = helper.get_param('alert_type')
    message['priority'] = helper.get_param('priority')
    message['tags'] = helper.get_param('tags')
    message['aggregation_key'] = helper.get_param('aggregation_key')

    payload = json.dumps(message)
    helper.log_debug("payload='{}'".format(payload))

    try:
        headers = dict()
        headers['Content-type']= "application/json"

        params = dict()
        params['api_key'] = helper.get_global_setting("api_key")

        r = helper.send_http_request(send_url, 'POST', parameters=params, payload=payload, headers=headers , use_proxy=True )
    except Exception as err:
        helper.log_error("Handling run-time error: {}".format(err))
        helper.log_error("r: {}".format(r.text))
        return False
        
    helper.log_debug("result.text='{}'".format(r.text))

    if (helper.get_global_setting("log_datadog")) :
        log_index = helper.get_global_setting("log_index")
        helper.log_info('Logging response to index="{}"'.format(log_index))
    
        event='status="{}" id="{}" title="{}" text="{}" date_happened="{}" alert_type="{}" priority="{}" tags="{}" url="{}" owner="{}" app="{}" search_name="{}" results_link="{}"'.format(r.json()["status"], r.json()["event"]["id"], r.json()["event"]["title"], r.json()["event"]["text"], r.json()["event"]["date_happened"], helper.get_param('alert_type'), r.json()["event"]["priority"], r.json()["event"]["tags"], r.json()["event"]["url"], helper.settings.get("owner"), helper.settings.get("app"), helper.settings.get("search_name"), helper.settings.get("results_link") )
        
        helper.log_debug('event to sent to splunk {}'.format(event))

        try:
            helper.addevent(event, sourcetype="datadog:response")
            helper.writeevents(index=log_index, host=helper.settings.get("server_host"), source="datadog_event")
        except Exception as err:
            helper.log_error("Handling run-time error: {}".format(err))
            return False    

    
    helper.log_info("Alert action datadog_event completed successfully.")
    return True


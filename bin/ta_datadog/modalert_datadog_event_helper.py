
import json

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
    dd_uri = helper.get_global_setting("dd_uri")
    helper.log_info("dd_uri={}".format(dd_uri))
    api_key = helper.get_global_setting("api_key")
    helper.log_info("api_key={}".format(api_key))
    app_key = helper.get_global_setting("app_key")
    helper.log_info("app_key={}".format(app_key))

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

    # TODO: Implement your alert action logic here
    dd_uri = helper.get_global_setting("dd_uri")
    app_key = helper.get_global_setting("app_key")
    api_key = helper.get_global_setting("api_key")

    send_url = dd_uri + "/events" #?api_key=" + api_key + "&" + app_key
    helper.log_debug("send_url: {}".format(send_url))

    message = dict()
    message['source_type_name'] = "splunk"
    message['title'] = helper.get_param('title')
    message['text'] = helper.get_param('message')
    message['alert_type'] = helper.get_param('alert_type')
    message['priority'] = helper.get_param('priority')
    message['tags'] = helper.get_param('tags')
    message['aggregation_key'] = helper.get_param('aggregation_key')

    payload = json.dumps(message)
    helper.log_info("payload: {}".format(payload))

    try:
        #r = requests.post(send_url, data=payload)
        headers = dict()
        headers['Content-type'] = "application/json"

        params = dict()
        params['app_key'] = app_key
        params['api_key'] = api_key

        r = helper.send_http_request(send_url, 'POST', parameters=params, payload=payload, headers=headers )
    except Exception as err:
        helper.log_error("Handling run-time error: {}".format(err))
        helper.log_error("r: {}".format(r.text))
        return 1
    helper.log_info("result text: {}".format(r.text))

    helper.log_info("Alert action datadog_event completed successfully.")
    return 0

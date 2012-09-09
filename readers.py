"""
Module to send urls to Pocket and Instapapper.
"""

import json
import requests
import time
import logging

_POCKET_KEY="dhuddrmvT6624y80g0Ab02eS2bg4I8fI"
#1 request every rate seconds
_INSTAPAPPER_RATE = 0.5

BAD_CREDENTIALS = 0
REQ_ERROR = 1
SERVICE_DOWN = 2
SUCCESS = 3

#set of all URLs that have been submitted to Pocket by this app
#on the first call to send_to_pocket this is populated
pocket_urls = set()
#since parameter for Pocket get request
last_pocket_url_check = None

module_logger = logging.getLogger('readers')

def _pocket_submitted_urls(name, pw, since=None):
    """Return a list of URLs submitted to Pocket by this 
    application since the given time.
    """
    if since:
        since_param = '&since={0}'.format(since)
    else:
        since_param = ''
    module_logger.debug("Requesting already submitted URLs since {0}".format(
        since))
    resp = requests.get('https://readitlaterlist.com/v2/get?username={0}&password={1}&apikey={2}&myAppOnly=1{3}'.format(name, pw, _POCKET_KEY, 
                                                 since_param))
    if resp.status_code != 200:
        module_logger.error('Unable to get pocket URLs: {0}, {1}'.format(
            resp.status_code, resp.headers.get('X-Error', None)))
        return [], None
    urls = []
    json_resp = json.loads(resp.text)
    since_resp = json_resp["since"]
    for uid in json_resp["list"]:
        urls.append(json_resp["list"][uid]["url"])
    return urls, since_resp    

def send_to_pocket(urls, name, pw):
    """Sends a list of urls to Pocket
    with the given name and password.

    urls - a list of tuples [(url, title), ...]
    name - string, username
    pw - string, username

    Returns status code to indicate success/failure
    """
    global last_pocket_url_check
    
    already_submitted, last_pocket_url_check = _pocket_submitted_urls(
        name, pw, last_pocket_url_check)
    for url in already_submitted:
        pocket_urls.add(url)
        
    new_urls = {}
    for idx, url in enumerate(urls):
        if not url[0].startswith("http"):
            formatted_url = "http://" + url[0]
        else:
            formatted_url = url[0]
        if formatted_url in pocket_urls:
            module_logger.debug("Skipping URL {0}".format(formatted_url))
            continue
        new_urls["{0}".format(idx)] = {"url":formatted_url,
                                       "title":url[1]}
    params = {}
    params['username'] = name
    params['password'] = pw
    params['apikey'] = _POCKET_KEY
    params['new'] = json.dumps(new_urls)
    debug_params = params.copy()
    del debug_params['password']
    module_logger.info("Sending request to Pocket {0}".format(debug_params))
    resp = requests.post("https://readitlaterlist.com/v2/send",
                     data=params)
    err = resp.headers.get('X-Error', None)
    if resp.status_code == 200:
        module_logger.info("Request successful")
        return SUCCESS
    elif resp.status_code == 400:
        module_logger.error("Invalid request: {0}".format(err))
        return REQ_ERROR
    elif resp.status_code == 401:
        module_logger.error("Invalid username")
        return BAD_CREDENTIALS
    elif resp.status_code == 403:
        module_logger.error("Rate limit exceeded")
        return REQ_ERROR
    elif resp.status_code == 503:
        module_logger.error("Pocket server is temp. unavailable")
        return SERVICE_DOWN
    else:
        module_logger.error("Unable to contact server")
        return SERVICE_DOWN

def send_to_instapapper(urls, name, pw):
    """Sends a list of urls to instapapper
    with the given name and password.
    The function pauses between each call, so the runtime
    is proportional to the number of urls.
    
    urls - a list of tuples [(url, title), ...]
    name - string, username
    pw - string, username

    Returns status code to indicate success/failure
    """
    params = {}
    params['username'] = name
    params['password' ] = pw
    while urls:
        params['url'] = urls[0][0]
        params['title'] = urls[0][1]
        debug_params = params.copy()
        del debug_params['password']
        module_logger.info("Sending request to instapapper {0}".format(
            debug_params))
        resp = requests.post("https://www.instapaper.com/api/add", data=params)
        if resp.status_code == 201:
            module_logger.info("Successful")
        elif resp.status_code == 400:
            module_logger.error("Invalid request")
            return REQ_ERROR 
        elif resp.status_code == 403:
            module_logger.error("Bad credentials")
            return BAD_CREDENTIALS
        elif resp.status_code == 500:
            module_logger.error("Temporarily unavailable")
            return SERVICE_DOWN
        else:
            #failed to contact server at all
            module_logger.error("Unable to contact server {0}".format(
                resp.status_code))
            return SERVICE_DOWN
        urls.pop(0)
        time.sleep(_INSTAPAPPER_RATE)

    return SUCCESS


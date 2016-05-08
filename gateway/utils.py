# -*- coding: utf-8 -*-
import leancloud
import requests
import requests_unixsocket
# Required for services which bind to unix socket
requests_unixsocket.monkeypatch()

from .classes import Object


def gte_zero(v):
    '''Limit given parameter to be greater than or equal to 0'''
    try:
        v = int(v)
        v = 0 if v < 0 else v
    except:
        v = 0
    return v


def list_services(page=0, page_limit=20):
    page = gte_zero(page)
    page_limit = gte_zero(page_limit)
    service_query = leancloud.Query('Service')
    service_query.skip(page * page_limit)
    service_query.limit(page_limit)
    return [Object(s.dump()) for s in service_query.find()]


def fetch_service_content(so, method='get'):
    if so.type == 'http':
        return requests.request(method, so.uri).content
    elif so.type == 'unix_socket':
        return 'Unix socket URI not supported yet'

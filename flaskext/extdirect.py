# -*- coding: utf-8 -*-
"""
    flaskext.extdirect
    ~~~~~~~~~~~~~~~~~~

    Adds Ext.Direct support to Flask. Under development.

    :copyright: (c) 2010 by PA Parent.
    :license: MIT, see LICENSE for more details.
"""

import inspect
import traceback
from sys import stderr

from flask import request, url_for

try:
    import json
except ImportError:
    import simplejson as json


class ExtDirect(object):

    def __init__(self, app=None, urlprefix='/direct', namespace='Ext.app',
                 name='Ext.app.REMOTING_API'):
        self.urlprefix = urlprefix
        self.ns = namespace
        self.name = name
        self.defs = {}
        self.registry = {}
        self.before_request_funcs = {}

        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        self.app.add_url_rule('%s/api' % self.urlprefix, 'directapi', self.api)
        self.app.add_url_rule('%s/router' % self.urlprefix, 'directrouter',
                              self.router, methods=['POST'])

    def before_request(self, f):
        self.before_request_funcs.setdefault(None, []).append(f)
        return f

    def preprocess_request(self):
        funcs = self.before_request_funcs.get(None, ())
        for func in funcs:
            func()

    def register(self, collection=None, flags=None):
        def decorate(func):
            funcname = func.__name__
            module = collection
            myflags = flags
            if module is None:
                module = func.__module__.split('.')[-1]

            if module not in self.registry:
                self.registry[module] = {}
            if module not in self.defs:
                self.defs[module] = []

            if myflags is None:
                myflags = {}

            args = inspect.getargspec(func)[0]
            infos = {'name': funcname, 'len': len(args)}
            infos.update(myflags)
            self.defs[module].append(infos)
            self.registry[module][funcname] = func

            return func
        return decorate

    def api(self):
        lines = ["Ext.ns('%s'); %s = %s;" % (self.ns, self.name,
            json.dumps({'url': url_for('directrouter'),
                      'type': 'remoting',
                      'actions': self.defs}))]
        lines.append("Ext.Direct.addProvider(%s);" % self.name)
        return "\n".join(lines)

    def router(self):
        self.preprocess_request()

        try:
            data = request.form.to_dict()
            data.pop('extAction')
            data.pop('extMethod')
            data.pop('extType')
            data.pop('extUpload')
            data.pop('extTID')
            req = {
                'action': request.form['extAction'],
                'method': request.form['extMethod'],
                'type': request.form['extType'],
                'upload': request.form['extUpload'],
                'tid': request.form['extTID'],
                'data': data,
            }
            return json.dumps(self._request(req))
        except KeyError:
            requests = json.loads(request.data)

            if isinstance(requests, dict):
                requests = [requests]

            responses = []
            for req in requests:
                responses.append(self._request(req))

            if len(responses) == 1:
                responses = responses[0]

            return json.dumps(responses)

    def _request(self, req):
        action, method, data, tid = (req['action'], req['method'],
                                     req['data'], req['tid'])

        func = self.registry[action][method]

        try:
            if isinstance(data, dict):
                result = func(**data)
            elif data:
                result = func(*data)
            else:
                result = func()
        except Exception, ex:
            traceback.print_exc(file=stderr)
            return {'type': 'exception',
                    'tid': tid,
                    'message': unicode(ex),
                    'where': traceback.format_exc()}
        else:
            return {'type': 'rpc',
                    'tid': tid,
                    'action': action,
                    'method': method,
                    'result': result}

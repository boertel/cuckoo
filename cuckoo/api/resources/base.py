from flask import jsonify, current_app, request, Response
from flask.views import View

from cuckoo import auth

from ..authentication import ApiTokenAuthentication


class Resource(View):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    authentication_classes = (ApiTokenAuthentication, )

    auth_required = True

    def dispatch_request(self, *args, **kwargs):
        tenant = None
        if self.authentication_classes:
            for auth_cls in self.authentication_classes:
                try:
                    _tenant = auth_cls().authenticate()
                    if _tenant:
                        tenant = _tenant
                        break
                except auth.AuthenticationFailed:
                    return self.respond({
                        'error': 'invalid_auth',
                    }, 401)

        if tenant:
            auth.set_current_tenant(tenant)
        elif self.auth_required:
            return self.respond({
                'error': 'auth_required',
            }, 401)

        try:
            method = getattr(self, request.method.lower())
        except AttributeError:
            return self.respond({'message': 'resource not found'}, 405)

        try:
            resp = method(*args, **kwargs)
            if not isinstance(resp, Response):
                resp = self.respond(resp)
            return resp
        except Exception:
            current_app.logger.exception('failed to handle api request')
            self.error('internal server error', 500)

    def error(self, message, status):
        return self.respond({'message': message}, status)

    def respond(self, context, status=200):
        resp = jsonify(context)
        resp.status_code = status
        return resp

    def schema_from_request(self, schema, partial=False):
        return schema.load(request.get_json() or request.form, partial=partial)

    def respond_with_schema(self, schema, value, status=200):
        result = schema.dump(value)
        if result.errors:
            return self.error('invalid schema supplied')
        return self.respond(result.data, status)

from flask import redirect, request, current_app, Response
import requests
from requests_oauthlib import OAuth2Session


class GithubProvider(object):
    AUTHORIZE_URI = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URI = 'https://github.com/login/oauth/access_token'
    SCOPES = ('user:email', )

    name = 'github'

    def get_oauth_session(self, redirect_uri=None, state=None):
        return OAuth2Session(
            client_id=current_app.config['GITHUB_CLIENT_ID'],
            scope=self.get_scope(),
            state=state,
            redirect_uri=redirect_uri,
        )

    def get_scope(self):
        return ','.join(self.SCOPES)

    def api(self, path, *args, **kwargs):
        url = 'https://api.github.com{}'.format(path)
        return requests.get(url, *args, **kwargs).json()

    def get_user_data(self, token):
        headers = {
            'Authorization': 'token {}'.format(token),
        }
        user_data = self.api('/user', headers=headers)
        emails = self.api('/user/emails', headers=headers)

        user_data['email'] = user_data.get('email')
        if user_data.get('email') is None:
            user_data['email'] = next((e['email'] for e in emails if e['verified'] and e['primary']))
        return user_data

    def authorize(self, redirect_uri):
        # auth.bind_redirect_target() TODO handle ?next=...
        oauth = self.get_oauth_session(redirect_uri)
        authorization_url, state = oauth.authorization_url(self.AUTHORIZE_URI)
        return redirect(authorization_url)

    def complete(self):
        oauth = self.get_oauth_session()

        oauth_response = oauth.fetch_token(
            self.ACCESS_TOKEN_URI,
            client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
            authorization_response=request.url,
        )

        assert oauth_response.get('access_token') is not None
        assert oauth_response.get('token_type') == 'bearer'

        scopes = oauth_response['scope'][0].split(',')

        if 'user:email' not in scopes:
            raise NotImplementedError

        user_data = self.get_user_data(oauth_response['access_token'])
        user_data['scopes'] = scopes

        identity_config = {
            'access_token': oauth_response['access_token'],
            'refresh_token': oauth_response.get('refresh_token'),
            'login': user_data['login'],
        }

        return identity_config, user_data

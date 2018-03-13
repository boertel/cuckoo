from flask import Blueprint, url_for

from cuckoo.auth.providers import GithubProvider
from cuckoo.web import views
from cuckoo.web.views.auth_github import identify

provider = GithubProvider()


def authorize():
    redirect_uri = url_for('web.complete', _external=True)
    return provider.authorize(redirect_uri=redirect_uri)


def complete():
    identity_config, user_data = provider.complete()
    return identify(provider, identity_config, user_data)


app = Blueprint('web', __name__)
app.add_url_rule('/auth/github', 'authorize', authorize)
app.add_url_rule('/auth/github/complete', 'complete', complete)

app.add_url_rule('/<path:path>', view_func=views.index)
app.add_url_rule('/', 'index', view_func=views.index)

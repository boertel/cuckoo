from flask import render_template, current_app


def index(path=None):
    return render_template(
        'index.html', **{
            'SENTRY_DSN_FRONTEND': current_app.config.get('SENTRY_DSN_FRONTEND', ''),
        }
    )

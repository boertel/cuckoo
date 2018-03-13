from flask import redirect
from sqlalchemy.exc import IntegrityError

from cuckoo import auth
from cuckoo.config import db
from cuckoo.models import Identity, User


def identify(provider, identity_config, user_data):
        scopes = user_data['scopes']
        primary_email = user_data.get('email')
        external_id = str(user_data['id'])

        try:
            with db.session.begin_nested():
                user = User(
                    email=primary_email,
                )
                db.session.add(user)

                identity = Identity(
                    user=user,
                    external_id=external_id,
                    provider=provider.name,
                    scopes=scopes,
                    config=identity_config,
                )
                db.session.add(identity)
            user_id = user.id
        except IntegrityError:
            identity = Identity.query.filter(
                Identity.external_id == external_id,
                Identity.provider == provider.name
            ).first()

            if not identity:
                user = User.query.filter(
                    User.email == primary_email
                ).first()
                assert user
                identity = Identity(
                    user=user,
                    external_id=external_id,
                    provider=provider.name,
                    scopes=scopes,
                    config=identity_config,
                )
                db.session.add(identity)
                user_id = user.id
            else:
                identity.config = identity_config
                identity.scopes = scopes
                db.session.add(identity)
                user_id = identity.user_id

        db.session.flush()
        db.session.commit()

        auth.login_user(user_id)
        return redirect('/')

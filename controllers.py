"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field
from yatl.helpers import A
from py4web.utils.form import Form,FormStyleBulma
from .common import db, session, T, cache, auth, logger


@action("index", method=["GET","POST"])
@action.uses("manager.html", session, db, T, auth.user)
def index():
    form = Form(db.documents,formstyle=FormStyleBulma)
    if form.accepted:
        # Do something with form.vars['product_name'] and form.vars['product_quantity']
        redirect(URL('success'))
    return dict(message=form)


@action("success", method="GET")
@action.uses("success.html", session, db, T, auth.user)
def acknowledgement():
    message="Entry successful"
    data = db().select(db.documents.ALL)
    return dict(message=message,data=data)

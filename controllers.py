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

from py4web import action, request
from py4web.utils.form import Form, FormStyleBulma
from .common import db, session, T, cache, auth, logger


@action("index", method=["GET"])
@action.uses("manager.html", session, db, T, auth.user)
def index():
    msg=''
    if request.query:
        try:
            db(db.documents.id == int(request.query.get('xid'))).delete()
            db.commit()
        except Exception as err:
            msg = err
    data = db(db.documents.user_id == auth.get_user()['id']).select(db.documents.ALL)
    return dict(data=data, msg=msg)


@action("upload", method=['GET', 'POST'])
@action.uses('uploader.html', session, db, T, auth.user)
def uploader():
    doc_type = db().select(db.tipo_document.ALL)
    if request.forms:
        file_type = request.forms['file_type']
        title = request.forms['title']
        description = request.forms['description']
        note = request.forms['note']
        files = db.documents.file.store(request.files.get('user_file').file, request.files.get('user_file').filename)
        try:
            id = db.documents.insert(
                user_id=auth.get_user()['id'],
                tipodocument_id=file_type,
                title=title,
                description=description,
                note=note,
                file=files
            )
            msg= "Record Number "+ str(id)
        except Exception as e:
            msg = "Error: {}".format(e)
    else:
        msg = "Not Posted"
    return dict(doc=doc_type,msg=msg)


@action("success", method="GET")
@action.uses("success.html", session, db, T, auth.user)
def acknowledgement():
    message="Entry successful"
    data = db().select(db.documents.ALL)
    return dict(message=message, data=data)


@action("tipo_document",method=["GET","POST"])
@action.uses("tipo.html",session,db,auth.user)
def tipo():
    form = Form(db.tipo_document, formstyle=FormStyleBulma)
    return dict(form=form)


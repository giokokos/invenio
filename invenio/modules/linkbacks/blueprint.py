# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2012 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebSearch Flask Blueprint"""

import datetime
import pprint
from functools import wraps
from string import rfind, strip
from datetime import datetime

from flask import Blueprint, session, make_response, g, render_template, \
                  request, flash, jsonify, redirect, url_for, current_app, \
                  Response
from invenio.base.decorators import wash_arguments
from invenio.ext.cache import cache
from invenio.intbitset import intbitset as HitSet
from invenio.ext.sqlalchemy import db
from invenio.base.i18n import _
from flask.ext.login import current_user
from invenio.modules.linkbacks.models import LnkENTRY
from invenio.access_control_engine import acc_authorize_action
from invenio.config import CFG_SITE_URL, \
                           CFG_SITE_LANG, \
                           CFG_SITE_RECORD, \
                           CFG_WEBLINKBACK_TRACKBACK_ENABLED

from invenio.weblinkback_config import CFG_WEBLINKBACK_TYPE, \
                                       CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME, \
                                       CFG_WEBLINKBACK_STATUS, \
                                       CFG_WEBLINKBACK_ORDER_BY_INSERTION_TIME, \
                                       CFG_WEBLINKBACK_LIST_TYPE, \
                                       CFG_WEBLINKBACK_TRACKBACK_SUBSCRIPTION_ERROR_MESSAGE, \
                                       CFG_WEBLINKBACK_PAGE_TITLE_STATUS, \
                                       CFG_WEBLINKBACK_BROKEN_COUNT


blueprint = Blueprint('weblinkback', __name__, url_prefix="/"+CFG_SITE_RECORD,
                      )

from invenio.modules.records.blueprint import request_record


@blueprint.route('/<int:recid>/linkbacks2', methods=['GET', 'POST'])
@request_record
def index(recid):
    uid = current_user.get_id()
    linkbacks = LnkENTRY.query.filter(db.and_(
        LnkENTRY.id_bibrec == recid,
        LnkENTRY.status == CFG_WEBLINKBACK_STATUS['APPROVED']
        )).all()
    return render_template('weblinkback_index.html',
                linkbacks=linkbacks)


@blueprint.route('/<int:recid>/sendtrackback', methods=['GET', 'POST'])
@request_record
@wash_arguments({'url': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME),
                                 'title': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME),
                                 'excerpt': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME),
                                 'blog_name': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME),
                                 'id': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME),
                                 'source': (unicode, CFG_WEBLINKBACK_SUBSCRIPTION_DEFAULT_ARGUMENT_NAME)})
def sendtrackback(recid, url, title, excerpt, blog_name, id, source):
    from invenio.weblinkback import perform_sendtrackback, perform_sendtrackback_disabled
    mime_type = 'text/xml; charset=utf-8'
    if CFG_WEBLINKBACK_TRACKBACK_ENABLED:
        xml_response, status = perform_sendtrackback(recid, url, title, excerpt, blog_name, id, source, current_user)
    else:
        xml_response, status = perform_sendtrackback_disabled()
    return Response(response=xml_response, status=status, mimetype=mime_type)
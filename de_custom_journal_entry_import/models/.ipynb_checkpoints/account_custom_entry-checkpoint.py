import base64
import hashlib
import itertools
import logging
import mimetypes
import os
import re
from collections import defaultdict
import uuid
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, ValidationError, MissingError, UserError
from odoo.tools import config, human_size, ustr, html_escape
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)


class AccountCustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    is_custom_entry_import = fields.Boolean(string='Update Entry')
    
    
    
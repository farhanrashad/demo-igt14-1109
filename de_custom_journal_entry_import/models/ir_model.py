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


class website_form_model(models.Model):
    _inherit = 'ir.model'
    
    
    def _get_form_writable_fields(self):
        """
        Restriction of "authorized fields" (fields which can be used in the
        form builders) to fields which have actually been opted into form
        builders and are writable. By default no field is writable by the
        form builder.
        """
        included = {
            field.name
            for field in self.env['ir.model.fields'].sudo().search([
                ('model_id', '=', self.id),
            ])
        }
        return {
            k: v for k, v in self.get_authorized_fields(self.model).items()
            if k in included
        }
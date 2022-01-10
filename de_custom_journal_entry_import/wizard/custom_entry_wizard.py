# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tempfile
import binascii
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io


class CustomEntryWizard(models.Model):
    _name = 'entry.import.wizard'
    _description = 'Entry Import Wizard'





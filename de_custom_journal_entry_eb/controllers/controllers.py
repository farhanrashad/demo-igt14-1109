# -*- coding: utf-8 -*-
# from odoo import http


# class DeCustomJournalEntryEbHistory(http.Controller):
#     @http.route('/de_custom_journal_entry_eb_history/de_custom_journal_entry_eb_history/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_custom_journal_entry_eb_history/de_custom_journal_entry_eb_history/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_custom_journal_entry_eb_history.listing', {
#             'root': '/de_custom_journal_entry_eb_history/de_custom_journal_entry_eb_history',
#             'objects': http.request.env['de_custom_journal_entry_eb_history.de_custom_journal_entry_eb_history'].search([]),
#         })

#     @http.route('/de_custom_journal_entry_eb_history/de_custom_journal_entry_eb_history/objects/<model("de_custom_journal_entry_eb_history.de_custom_journal_entry_eb_history"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_custom_journal_entry_eb_history.object', {
#             'object': obj
#         })

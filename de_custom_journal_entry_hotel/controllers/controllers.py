# -*- coding: utf-8 -*-
# from odoo import http


# class DeCustomJournalEntryPenalty(http.Controller):
#     @http.route('/de_custom_journal_entry_penalty/de_custom_journal_entry_penalty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_custom_journal_entry_penalty/de_custom_journal_entry_penalty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_custom_journal_entry_penalty.listing', {
#             'root': '/de_custom_journal_entry_penalty/de_custom_journal_entry_penalty',
#             'objects': http.request.env['de_custom_journal_entry_penalty.de_custom_journal_entry_penalty'].search([]),
#         })

#     @http.route('/de_custom_journal_entry_penalty/de_custom_journal_entry_penalty/objects/<model("de_custom_journal_entry_penalty.de_custom_journal_entry_penalty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_custom_journal_entry_penalty.object', {
#             'object': obj
#         })

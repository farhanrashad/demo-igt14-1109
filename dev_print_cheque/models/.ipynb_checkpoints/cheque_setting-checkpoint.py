# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models, fields, api,_


class cheque_setting(models.Model):
    _name = 'cheque.setting'
    _description = "Cheque Setting Module"

    name = fields.Char(string='Name', required="1")
    font_size = fields.Float(string='Font Size', default="13", required="1")
    color = fields.Char(string='Color', default="#000", required="1")
    alignment = fields.Selection([('vertical', 'Vertical'), ('horizontal', 'Horizontal')], default='horizontal',string='Alignment')

    is_partner = fields.Boolean(string='Print Partner', default=True)
    is_partner_bold = fields.Boolean(string='Font Bold')
    partner_text = fields.Selection([('prefix', 'Prefix'), ('suffix', 'Suffix')], string='Partner Title')
    partner_m_top = fields.Float(string='Partner From Top', default=150)
    partner_m_left = fields.Float(string='Partner From Left', default=70)

    is_date = fields.Boolean(string='Print Date', default=True)
    is_date_bold = fields.Boolean(string='Date Font Bold')
    date_formate = fields.Selection([('dd_mm', 'DD MM'), ('mm_dd', 'MM DD')], string='Date Format', default='dd_mm')
    year_formate = fields.Selection([('yy', 'YY'), ('yyyy', 'YYYY')], string='Year Format', default='yy')
    date_m_top = fields.Float(string='Date From Top', default=90)
    f_d_m_left = fields.Float(string='First Digit', default=550)
    s_d_m_left = fields.Float(string='Second Digit', default=565)
    t_d_m_left = fields.Float(string='Third Digit', default=580)
    fo_d_m_left = fields.Float(string='Fourth Digit', default=595)
    fi_d_m_left = fields.Float(string='Fifth Digit', default=610)
    si_d_m_left = fields.Float(string='Six Digit', default=625)
    se_d_m_left = fields.Float(string='Seven Digit', default=640)
    e_d_m_left = fields.Float(string='Eight Digit', default=655)
    
    date_seprator = fields.Char(string='Seperator')

    is_amount = fields.Boolean(string='Print Amount', default=True)
    amt_m_top = fields.Float(string='Amount From Top', default=158.76)
    amt_m_left = fields.Float(string='Amount From Left', default=540)
    is_star = fields.Boolean(string='Print Star', help="if true then print 3 star before and after Amount", default=True)
    is_amount_bold = fields.Boolean(string='Amount Font Bold')
    
    is_currency = fields.Boolean('Print Currency')

    is_amount_word = fields.Boolean('Print Amount Words', default=True)
    is_word_bold = fields.Boolean(string='Word Font Bold')
    word_in_f_line = fields.Float('Split Words After', default=5,
                                  help="How Many Words You want to print in first line, The rest will go in second line")
    amt_w_m_top = fields.Float(string='From First Top', default=158.76)
    amt_w_m_left = fields.Float(string='From First Left', default=105.84)
    is_star_word = fields.Boolean(string='Print Star with Word', help="if true then print 3 star before and after Words Amount",
                                  default=True)

    amt_w_s_m_top = fields.Float(string='From Sec Top', default=185)
    amt_w_s_m_left = fields.Float(string='From Sec Left', default=45)

    is_company = fields.Boolean(string='Print Company')
    c_margin_top = fields.Float(string='Company From Top', default=280)
    c_margin_left = fields.Float(string='Company From Left', default=560)

    print_journal = fields.Boolean('Print Journal')
    journal_margin_top = fields.Float(string='Journal From Top', default=600)
    journal_margin_left = fields.Float(string='Journal From Left', default=45)

    is_stub = fields.Boolean(string='Print Stub')
    stub_margin_top = fields.Float(string='Stub From Top', default=350)
    stub_margin_left = fields.Float(string='Stub From Left', default=45)

    is_cheque_no = fields.Boolean(string='Print Cheque No')
    cheque_margin_top = fields.Float(string='Cheque From Top', default=50)
    cheque_margin_left = fields.Float(string='Cheque From Left', default=450)

    is_free_one = fields.Boolean(string='Print Free Text One')
    f_one_margin_top = fields.Float(string='Free From Top', default=230)
    f_one_margin_left = fields.Float(string='Free From Left', default=100)

    is_free_two = fields.Boolean(string='Print Free Text Two')
    f_two_margin_top = fields.Float(string='Margin From Top', default=500)
    f_two_margin_left = fields.Float(string='Margin From Left', default=100)

    is_acc_pay = fields.Boolean(string='Print A/C PAY', default=True)
    is_acc_bold = fields.Boolean(string='A/C Font Bold')

    acc_pay_m_top = fields.Float(string='Pay From Top', default=90)
    acc_pay_m_left = fields.Float(string='Pay From Left', default=50)
    
    is_f_line_sig = fields.Boolean(string='Print First Signature')
    f_sig_m_top = fields.Float(string='Sign From Top', default=200)
    f_sig_m_left = fields.Float(string='Sign From Left', default=540)
    
    is_s_line_sig = fields.Boolean(string='Print Second Signature')
    s_sig_m_top = fields.Float('Sign2 From Top', default=300)
    s_sig_m_left = fields.Float('Sign2 From Left', default=540)





# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:

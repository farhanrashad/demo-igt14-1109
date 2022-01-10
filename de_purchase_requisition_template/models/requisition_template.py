# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class RequisitionTemplate(models.Model):
    _name = "purchase.requisition.template"
    _description = "Requisition Template"

    name = fields.Char('Quotation Template', required=True)
    requisition_template_line_ids = fields.One2many('purchase.requisition.template.line', 'requisition_template_id', 'Lines', copy=True)
    note = fields.Text('Terms and conditions', translate=True)
    active = fields.Boolean(default=True, help="If unchecked, it will allow you to hide the quotation template without removing it.")
    company_id = fields.Many2one('res.company', string='Company')

    @api.constrains('company_id', 'requisition_template_line_ids')
    def _check_company_id(self):
        for template in self:
            companies = template.mapped('requisition_template_line_ids.product_id.company_id')
            if len(companies) > 1:
                raise ValidationError(_("Your template cannot contain products from multiple companies."))
            elif companies and companies != template.company_id:
                raise ValidationError(_(
                    "Your template contains products from company %(product_company)s whereas your template belongs to company %(template_company)s. \n Please change the company of your template or remove the products from other companies.",
                    product_company=', '.join(companies.mapped('display_name')),
                    template_company=template.company_id.display_name,
                ))

    @api.onchange('requisition_template_line_ids')
    def _onchange_template_line_ids(self):
        companies = self.mapped('requisition_template_line_ids.product_id.company_id')
        if companies and self.company_id not in companies:
            self.company_id = companies[0]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(RequisitionTemplate, self).create(vals_list)
        #records._update_product_translations()
        return records

    def write(self, vals):
        #if 'active' in vals and not vals.get('active'):
         #   companies = self.env['res.company'].sudo().search([('requisition_template_id', 'in', self.ids)])
          #  companies.requisition_template_id = None
        result = super(RequisitionTemplate, self).write(vals)
        #self._update_product_translations()
        return result
"""
    def _update_product_translations(self):
        languages = self.env['res.lang'].search([('active', '=', 'true')])
        for lang in languages:
            for line in self.requisition_template_line_ids:
                if line.name == line.product_id.get_product_multiline_description_purchase():
                    self.create_or_update_translations(model_name='purchase.requisition.template.line,name', lang_code=lang.code, res_id=line.id,src=line.name,                                                       value=line.product_id.with_context(lang=lang.code).get_product_multiline_description_purchase())


    def create_or_update_translations(self, model_name, lang_code, res_id, src, value):
        data = {
            'type': 'model',
            'name': model_name,
            'lang': lang_code,
            'res_id': res_id,
            'src': src,
            'value': value,
            'state': 'inprogress',
        }
        existing_trans = self.env['ir.translation'].search([('name', '=', model_name),
                                                            ('res_id', '=', res_id),
                                                            ('lang', '=', lang_code)])
        if not existing_trans:
            self.env['ir.translation'].create(data)
        else:
            existing_trans.write(data)

"""

class RequisitionTemplateLine(models.Model):
    _name = "purchase.requisition.template.line"
    _description = "Requisition Template Line"
    _order = 'requisition_template_id, sequence, id'

    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sale quote lines.",
        default=10)
    requisition_template_id = fields.Many2one(
        'purchase.requisition.template', 'Requisition Template Reference',
        required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', related='requisition_template_id.company_id', store=True, index=True)
    name = fields.Text('Description', required=True, translate=True)
    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True,
        domain=[('sale_ok', '=', True)])
    product_uom_qty = fields.Float('Quantity', required=True, digits='Product Unit of Measure', default=1)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id
            self.name = self.product_id.get_product_multiline_description_sale()

    def write(self, values):
        return super(RequisitionTemplateLine, self).write(values)
    
    def _prepare_purchase_requisition_line(self, product_qty=0.0, ):
        self.ensure_one()
        template = self.requisition_template_id
        #if self.product_description_variants:
        #    name += '\n' + self.product_description_variants
        #if requisition.schedule_date:
         #   date_planned = datetime.combine(requisition.schedule_date, time.min)
        #else:
         #   date_planned = datetime.now()
        return {
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_po_id.id,
            'product_qty': product_qty,
            #'price_unit': price_unit,
            #'date_planned': date_planned,
            #'account_analytic_id': self.account_analytic_id.id,
            #'analytic_tag_ids': self.analytic_tag_ids.ids,
        }
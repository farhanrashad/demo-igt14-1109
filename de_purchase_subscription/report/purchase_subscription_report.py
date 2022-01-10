from odoo import tools
from odoo import api, fields, models


class purchase_subscription_report(models.Model):
    _name = "purchase.subscription.report"
    _description = "Subscription Analysis"
    _auto = False

    name = fields.Char()
    date_start = fields.Date('Start Date', readonly=True)
    date_end = fields.Date('End Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    recurring_monthly = fields.Float('Monthly Recurring Revenue', readonly=True)
    recurring_yearly = fields.Float('Yearly Recurring Revenue', readonly=True)
    recurring_total = fields.Float('Recurring Price', readonly=True)
    quantity = fields.Float('Quantity', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    subscription_plan_id = fields.Many2one('purchase.subscription.plan', 'Subscription Plan', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    stage_category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('closed', 'Closed')], readonly=True, help="Category of the stage")
    stage_id = fields.Many2one('purchase.subscription.stage', string='Stage', readonly=True)

    def _select(self):
        select_str = """
             SELECT min(l.id) as id,
                    sub.name as name,
                    l.product_id as product_id,
                    l.uom_id as product_uom,
                    sum(
                        coalesce(l.price_subtotal / nullif(sub.recurring_total, 0), 0)
                        * sub.recurring_price
                    ) as recurring_monthly,
                    sum(
                        coalesce(l.price_subtotal / nullif(sub.recurring_total, 0), 0)
                        * sub.recurring_price * 12
                    ) as recurring_yearly,
                    sum(l.price_subtotal) as recurring_total,
                    sum(l.quantity) as quantity,
                    sub.date_start as date_start,
                    sub.date as date_end,
                    sub.partner_id as partner_id,
                    sub.user_id as user_id,
                    sub.company_id as company_id,
                    stage.stage_category,
                    
                    sub.stage_id,
                    sub.subscription_plan_id as subscription_plan_id,
                    t.categ_id as categ_id,
                    p.product_tmpl_id
        """
        return select_str

    def _from(self):
        from_str = """
                purchase_subscription_line l
                      join purchase_subscription sub on (l.purchase_subscription_id=sub.id)
                      join purchase_subscription_stage stage on sub.stage_id = stage.id
                      left outer join account_analytic_account a on sub.analytic_account_id=a.id
                      join res_partner partner on sub.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.uom_id)
                    
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                    l.uom_id,
                    t.categ_id,
                    sub.recurring_price,
                    sub.recurring_total,
                    sub.date_start,
                    sub.date,
                    sub.partner_id,
                    sub.user_id,
                    quantity,
                    sub.company_id,
                    stage.stage_category,
                    sub.stage_id,
                    sub.name,
                    sub.subscription_plan_id,
                    p.product_tmpl_id,
                    partner.country_id
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

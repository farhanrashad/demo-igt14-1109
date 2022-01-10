from psycopg2 import sql

from odoo import tools
from odoo import api, fields, models


class FleetReport(models.Model):
    _inherit = "fleet.vehicle.cost.report"
    
    
    service_type_id = fields.Many2one('fleet.vehicle.log.services', 'Service Type', readonly=True)
    liter = fields.Integer(string='Liter')
    total_price = fields.Integer(string='Cost of fuels')
    odometer_value = fields.Char(string='Odometer Reading')
    
    def init(self):
        query = """
WITH service_costs AS (
    SELECT
        ve.id AS vehicle_id,
        ve.company_id AS company_id,
        ve.name AS name,
        ve.driver_id AS driver_id,
        ve.fuel_type AS fuel_type,
        date(date_trunc('month', d)) AS date_start,
        COALESCE(sum(se.amount), 0) AS
        COST,
        se.service_type_id,
        fuel.liter,
        fuel.total_price,
        fuel.odometer_value,
        'service' AS cost_type
    FROM
        fleet_vehicle ve
    CROSS JOIN generate_series((
            SELECT
                min(acquisition_date)
                FROM fleet_vehicle), CURRENT_DATE, '1 month') d
        LEFT JOIN fleet_vehicle_log_services se ON se.vehicle_id = ve.id
            AND date_trunc('month', se.date) = date_trunc('month', d)
        LEFT JOIN vehicle_fuel_log fuel ON fuel.vehicle = ve.id    
    WHERE
        ve.active AND se.active AND se.state != 'cancelled'
    GROUP BY
        ve.id,
        se.service_type_id,
        fuel.liter,
        fuel.total_price,
        fuel.odometer_value,
        ve.company_id,
        ve.name,
        date_start,
        d
    ORDER BY
        ve.id,
        date_start
),
contract_costs AS (
    SELECT
        ve.id AS vehicle_id,
        ve.company_id AS company_id,
        ve.name AS name,
        ve.driver_id AS driver_id,
        ve.fuel_type AS fuel_type,
        date(date_trunc('month', d)) AS date_start,
        (COALESCE(sum(co.amount), 0) + COALESCE(sum(cod.cost_generated * extract(day FROM least (date_trunc('month', d) + interval '1 month', cod.expiration_date) - greatest (date_trunc('month', d), cod.start_date))), 0) + COALESCE(sum(com.cost_generated), 0) + COALESCE(sum(coy.cost_generated), 0)) AS
        COST,
        ser.service_type_id,
        fuels.liter,
        fuels.total_price,
        fuels.odometer_value,
        'contract' AS cost_type
    FROM
        fleet_vehicle ve
    CROSS JOIN generate_series((
            SELECT
                min(acquisition_date)
                FROM fleet_vehicle), CURRENT_DATE, '1 month') d
        LEFT JOIN fleet_vehicle_log_contract co ON co.vehicle_id = ve.id
            AND date_trunc('month', co.date) = date_trunc('month', d)
        LEFT JOIN fleet_vehicle_log_contract cod ON cod.vehicle_id = ve.id
            AND date_trunc('month', cod.start_date) <= date_trunc('month', d)
            AND date_trunc('month', cod.expiration_date) >= date_trunc('month', d)
            AND cod.cost_frequency = 'daily'
    LEFT JOIN fleet_vehicle_log_contract com ON com.vehicle_id = ve.id
        AND date_trunc('month', com.start_date) <= date_trunc('month', d)
        AND date_trunc('month', com.expiration_date) >= date_trunc('month', d)
        AND com.cost_frequency = 'monthly'
    LEFT JOIN fleet_vehicle_log_contract coy ON coy.vehicle_id = ve.id
        AND date_trunc('month', coy.date) = date_trunc('month', d)
        AND date_trunc('month', coy.start_date) <= date_trunc('month', d)
        AND date_trunc('month', coy.expiration_date) >= date_trunc('month', d)
        AND coy.cost_frequency = 'yearly'
    LEFT JOIN fleet_vehicle_log_services ser ON ser.vehicle_id = ve.id
    LEFT JOIN vehicle_fuel_log fuels ON fuels.vehicle = ve.id    

WHERE
    ve.active
GROUP BY
    ve.id,
    ve.company_id,
    ser.service_type_id,
    fuels.liter,
    fuels.total_price,
    fuels.odometer_value,
    ve.name,
    date_start,
    d
ORDER BY
    ve.id,
    date_start
)
SELECT
    vehicle_id AS id,
    company_id,
    vehicle_id,
    service_type_id,
    liter,
    total_price,
    odometer_value,
    name,
    driver_id,
    fuel_type,
    date_start,
    COST,
    'service' as cost_type
FROM
    service_costs sc
UNION ALL (
    SELECT
        vehicle_id AS id,
        company_id,
        vehicle_id,
        service_type_id,
        liter,
        total_price,
        odometer_value,
        name,
        driver_id,
        fuel_type,
        date_start,
        COST,
        'contract' as cost_type
    FROM
        contract_costs cc)
"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table),
                sql.SQL(query)
            ))


    
    
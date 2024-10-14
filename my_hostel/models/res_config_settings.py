
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_hostel_user = fields.Boolean("Hostel User", implied_group="my_hostel.group_hostel_manager")
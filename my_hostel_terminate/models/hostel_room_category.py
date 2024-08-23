from odoo import fields, models


class RoomCategory(models.Model):
    _inherit = "hostel.room.category"

    max_allow_days = fields.Integer(
        "Maximum allows days",
        help="For how many days room can be borrowed",
        default=365,
    )

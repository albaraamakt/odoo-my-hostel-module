from datetime import timedelta
from odoo import fields, models

class HostelRoom(models.Model):
    _inherit = "hostel.room"

    date_termination = fields.Date('Date of Termination')

    def make_closed(self):
        day_to_allocate = self.category_id.max_allow_days or 10
        self.date_termination = fields.Date.today() + timedelta(days=day_to_allocate)

        return super(HostelRoom, self).make_closed()

    def make_available(self):
        self.date_termination = False

        return super(HostelRoom, self).make_available()
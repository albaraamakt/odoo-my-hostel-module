from datetime import timedelta
from odoo.exceptions import UserError
from odoo import models, fields, api

class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = "Hostel Student"

    name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    active = fields.Boolean(
        "Active", default=True, help="Activate/Deactivate hostel record"
    )
    room_id = fields.Many2one("hostel.room", string="Room", ondelete='set null')
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("reservation", "Reservation"),
            ("pending", "Pending"),
            ("paid", "Done"),
            ("discharge", "Discharge"),
            ("cancel", "Cancel"),
        ],
        string="Status",
        default='draft',
        readonly=False
    )
    admission_date = fields.Date("Admission Date", default=fields.Date.today())
    discharge_date = fields.Date("Discharge Date", compute="_compute_discharge_date", inverse="_inverse_discharge_date")
    duration = fields.Integer("Duration", default=7)

    @api.depends('admission_date', 'duration')
    def _compute_discharge_date(self):
        for record in self:
            if record.admission_date and record.duration:
                record.discharge_date = record.admission_date + timedelta(days=record.duration)
            else:
                record.discharge_date = False

    def _inverse_discharge_date(self):
        for record in self:
            if record.admission_date and record.discharge_date:
                record.duration = (record.discharge_date - record.admission_date).days
            else:
                record.duration = 0

    def action_assign_room(self):
        self.ensure_one()

        if self.status != "paid":
            raise UserError("You can't assign a room if it's not paid.")

        room_as_superuser = self.env['hostel.room'].sudo()

        room_rec = room_as_superuser.create({
            "name": "Room 431",
            "room_no": "431",
            "room_category_id": self.env.ref("my_hostel.single_room_categ").id,
        })

    def action_remove_room(self):
        if self.env.context.get("is_hostel_room"):
            self.room_id = False
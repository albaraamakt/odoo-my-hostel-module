
from odoo import fields, models

class HostelAssignRoom(models.TransientModel):
    _name = "hostel.assign.room.wizard"

    # active = fields.Boolean("Active", default=True)
    room_id = fields.Many2one("hostel.room", string="Room", required=True)

    def add_room_in_student(self):
        hostel_room_student = self.env['hostel.student'].browse(self.env.context.get('active_id'))

        if hostel_room_student:
            hostel_room_student.update({
                # 'hostel_id': self.room_id.hostel_id.id,
                'room_id': self.room_id.id,
                'admission_date': fields.Date.today(),
            })
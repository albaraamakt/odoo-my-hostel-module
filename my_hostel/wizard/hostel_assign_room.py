
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class HostelAssignRoom(models.TransientModel):
    _name = "hostel.assign.room.wizard"
    _description = "Hostel Assign Room Wizard"

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
        rooms = self.mapped('room_id')
        action = rooms.get_formview_action()
        if len(rooms.ids) > 1:
            _logger.debug(msg='if block in add_room_in_student is reached.')
            action['domain'] = [('id', 'in', tuple(rooms.ids))]
            action['view_mode'] = 'tree,form'
        return action
# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):

    _name = "hostel.room"
    _description = "Information about hostel Room"

    name = fields.Char(string="Hostel Name", required=True)
    room_no = fields.Char(string="Room Number", required=True)
    other_info = fields.Text("Other Information", help="Enter more information")
    allocation_date = fields.Date("Allocation Date")
    category_id = fields.Many2one("hostel.room.category", string="Category")
    description = fields.Html("Description")
    room_rating = fields.Float("Hostel Average Rating", digits=(14, 4))
    member_ids = fields.Many2many("hostel.room.member", string="Members")
    state = fields.Selection(
        [("draft", "Unavailable"), ("available", "Available"), ("closed", "Closed")],
        "State",
        default="draft",
    )
    remarks = fields.Text("Remarks")
    cost_price = fields.Float("Room Cost")
    student_per_room = fields.Integer('Student per Room')
    rent_amount = fields.Integer('Rent')

    def grouped_data(self):
        data = self._get_average_cost()
        _logger.info("Grouped Data %s" % data)

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [("cost_price", "!=", False)],  # Domain
            ["category_id", "cost_price:avg"],  # Fields to access
            ["category_id"],  # group_by
        )
        return grouped_result

    @api.model
    def create(self, values):
        _logger.info("Create Hostel Room %s" % values)
        _logger.info(" ".center(15, "="))
        if not self.user_has_groups("my_hostel.group_hostel_manager"):
            if values.get("remarks"):
                raise UserError("You are not allowed to modify " "remarks")
        return super(HostelRoom, self).create(values)

    @api.model
    def write(self, values):
        _logger.info("Updated Hostel Room %s" % values)
        if not self.user_has_groups("my_hostel.group_hostel_manager"):
            if values.get("remarks"):
                raise UserError("You are not allowed to modify " "manager_remarks")
        return super(HostelRoom, self).create(values)

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [("draft", "available"), ("available", "closed"), ("closed", "draft")]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _("Moving from %s to %s is not allowed") % (
                    room.state,
                    new_state,
                )
                raise UserError(message)

    def make_available(self):
        self.change_state("available")

    def make_closed(self):
        self.change_state("closed")

    def log_all_room_members(self):
        hostel_room_obj = self.env[
            "hostel.room.member"
        ]  # This is an empty recordset of model hostel.room.member
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def create_categories(self):
        categ1 = {"name": "Child category 1", "description": "Description for child 1"}
        categ2 = {"name": "Child category 2", "description": "Description for child 2"}
        parent_category_val = {
            "name": "Parent category",
            "description": "Description for parent category",
            "child_ids": [
                (0, 0, categ1),
                (0, 0, categ2),
            ],
        }
        self.env["hostel.room.category"].create(parent_category_val)
        return True

    def update_room_no(self):
        self.ensure_one()
        self.room_no = "RM002"

    def find_room(self):
        domain = [
            "|",
            "&",
            ("name", "ilike", "Room Name"),
            ("category_id.name", "=", "Category Name"),
            "&",
            ("name", "ilike", "Second Room Name"),
            ("category_id.name", "=", "Second Category Name"),
        ]
        Rooms = self.search(domain)
        _logger.info("Room found: %s", Rooms)
        return True

    # Filter recordset
    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        _logger.info("Filtered Rooms: %s", filtered_rooms)

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.member_ids) > 1:
                return True

        return all_rooms.filtered(predicate)

    # Traversing recordset
    def mapped_rooms(self):
        all_rooms = self.search([])
        room_authors = self.get_member_names(all_rooms)
        _logger.info("Rooms Members: %s", room_authors)

    @api.model
    def get_member_names(self, all_rooms):
        return all_rooms.mapped("member_ids.name")

    # Sorting recordset
    def sort_room(self):
        all_rooms = self.search([])
        rooms_sorted = self.sort_rooms_by_rating(all_rooms)
        _logger.info("Rooms before sorting: %s", all_rooms)
        _logger.info("Rooms after sorting: %s", rooms_sorted)

    @api.model
    def sort_rooms_by_rating(self, all_rooms):
        return all_rooms.sorted(key="room_rating")

    @api.model
    def _update_room_price(self, category):
        all_rooms = self.search(['category_id', '=', category.id])
        for room in all_rooms:
            room.cost_price += 10
    
    def action_remove_room_members(self):
        student = self.env['hostel.student']
        student.with_context(is_hostel_room=True).action_remove_room()

    def action_category_with_amount(self):
        if self.category_id.id:
            query = """
            SELECT hrc.name
            FROM hostel_room AS hostel_room
            JOIN hostel_room_category as hrc ON hrc.id = hostel_room.category_id
            WHERE hostel_room.category_id = %(cate_id)s;
            """ % {'cate_id': self.category_id.id}

            self.env.cr.execute(query)
            result = self.env.cr.fetchall()
            _logger.warning("Hostel Room With Amount: %s", result)
        else:
            _logger.warning("Hostel room doesn't belong to a category")

class HostelRoomMember(models.Model):

    _name = "hostel.room.member"
    _inherits = {"res.partner": "partner_id"}
    _description = "Hostel Room member"

    partner_id = fields.Many2one("res.partner", ondelete="cascade")
    date_start = fields.Date("Member Since")
    date_end = fields.Date("Termination Date")
    member_number = fields.Char()
    date_of_birth = fields.Date("Date of birth")

class HostelRoomAvailability(models.Model):
    _name = "hostel.room.availability"
    _auto = False

    room_id = fields.Many2one('hostel.room', 'Room', readonly=True)
    availability = fields.Integer('Availability', readonly=True)
    student_per_room = fields.Integer('Student per Room', readonly=True)
    amount = fields.Integer('Amount', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            CREATE OR REPLACE VIEW hostel_room_availability AS (
            SELECT
                    min(h_room.id) as id,
                    h_room.id as room_id,
                    h_room.student_per_room as student_per_room,
                    h_room.rent_amount as amount
                FROM
                    hostel_room AS h_room
                GROUP BY h_room.id
            );
        """
        self.env.cr.execute(query)

# -*- coding: utf-8 -*-
# from odoo import http


# class MyHostelTerminate(http.Controller):
#     @http.route('/my_hostel_terminate/my_hostel_terminate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_hostel_terminate/my_hostel_terminate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_hostel_terminate.listing', {
#             'root': '/my_hostel_terminate/my_hostel_terminate',
#             'objects': http.request.env['my_hostel_terminate.my_hostel_terminate'].search([]),
#         })

#     @http.route('/my_hostel_terminate/my_hostel_terminate/objects/<model("my_hostel_terminate.my_hostel_terminate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_hostel_terminate.object', {
#             'object': obj
#         })


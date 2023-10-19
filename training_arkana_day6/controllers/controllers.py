# -*- coding: utf-8 -*-
# from odoo import http


# class TrainingArkanaDay6(http.Controller):
#     @http.route('/training_arkana_day6/training_arkana_day6', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training_arkana_day6/training_arkana_day6/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('training_arkana_day6.listing', {
#             'root': '/training_arkana_day6/training_arkana_day6',
#             'objects': http.request.env['training_arkana_day6.training_arkana_day6'].search([]),
#         })

#     @http.route('/training_arkana_day6/training_arkana_day6/objects/<model("training_arkana_day6.training_arkana_day6"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training_arkana_day6.object', {
#             'object': obj
#         })

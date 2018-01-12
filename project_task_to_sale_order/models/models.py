# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Project(models.Model):
    _inherit = ['project.project']

    allow_convert_task_to_quotation = fields.Boolean(
        string="Allow convert Task to quoation",
        default=False, store=True,
        help="Allows to display the button in tasks to create a quoation from" +
             " the task. If you want to see the button, you also need to" +
             " check this field under the stage"
    )


class ProjectTaskType(models.Model):
    _inherit = ['project.task.type']

    allow_convert_task_to_quotation = fields.Boolean(
        string="Allow convert Task to quoation",
        default=False, store=True,
        help="Allows to display the button in tasks to create a quoation from" +
             " the task. If you want to see the button, you also need to" +
             " check this field under the project"
    )


class Task(models.Model):
    _inherit = ['project.task']

    created_sale_order = fields.Many2one(
        'sale.order',
        string="Reference to Sale Order",
        ondelete="SET NULL"
    )
    product_template_ids = fields.Many2many(
        'product.template',
        string="Products",
        ondelete="SET NULL"
    )
    hide_create_order_button = fields.Boolean(
        string='Hides the create order button',
        compute="_compute_hide_create_order_button"
    )

    @api.depends('created_sale_order', 'stage_id', 'stage_id')
    def _compute_hide_create_order_button(self):
        self.ensure_one()
        if len(self.created_sale_order):
            self.hide_create_order_button = True
        elif not self.project_id.allow_convert_task_to_quotation:
            self.hide_create_order_button = True
        elif not self.stage_id.allow_convert_task_to_quotation:
            self.hide_create_order_button = True
        else:
            self.hide_create_order_button = False

    @api.multi
    def create_order(self):
        if not len(self.partner_id):
            raise exceptions.MissingError('You need to add a partner/customer to do this action!')

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
        })

        sol_model = self.env['sale.order.line']
        for line in self.product_template_ids:
            sol_model.create({
                'name': line.name,
                'product_id': line.id,
                'product_uom': line.uom_id.id,
                'product_uom_qty': 1,
                'order_id': sale_order.id,
            })

        self.created_sale_order = sale_order
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
        }

    @api.multi
    def redirect_to_order(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self.created_sale_order.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
        }
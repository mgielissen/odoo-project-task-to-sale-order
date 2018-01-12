from odoo.tests.common import TransactionCase


class TestProjectTask(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProjectTask, self).setUp(*args, **kwargs)
        project = self.env['project.project'].search([])[0]
        project.allow_convert_task_to_quotation = True

        self.stage = self.env['project.task.type'].search([('name', '=', 'Done')])
        self.stage.allow_convert_task_to_quotation = True

        products = self.env['product.template'].search([])[0:10]

        self.task = self.env['project.task'].create({
            'name': 'testcase',
            'project_id': project.id
        })
        self.task.write({'product_template_ids': [(4, x.id) for x in products]})

    def test_task(self):
        self.assertEqual(self.task.hide_create_order_button, True)

    def test_stage_change(self):
        self.task.stage_id = self.stage.id
        self.assertEqual(self.task.hide_create_order_button, False)

    def test_create_order(self):
        self.task.create_order()
        self.assertEqual(len(self.task.created_sale_order), 1)
        self.assertEqual(len(self.task.created_sale_order.order_line.ids), 10)

# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class todo(models.Model)ww
#     _name = 'todo.todo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
class TodoCategory(models.Model):
	_name="todo.category"
	_description =u"待办事项类别"

	name=fields.Char(string=u"类别名称",required=True)
	task_ids=fields.One2many("todo.task","category_id",string=u"待办事项")
	task_count=fields.Integer(string=u"待办事项数量",compute="_compute_task_count")

	@api.depends("task_ids")
	@api.multi
	def _compute_task_count(self):
		for rec in self:
			rec.task_count = len(rec.task_ids)





class TodoTask(models.Model):
	_name="todo.task"
	_description=u"待办事项详情"

	name=fields.Char(string=u"Task Name")
	category_id = fields.Many2one("todo.category", string=u"类别")
	is_done=fields.Boolean(string=u"是否完成")
	priority=fields.Selection([("todo","待办"),("normal","普通"),("urgency","紧急")],default="todo",string="紧急程度")
	deadline=fields.Datetime(string="截止时间")
	is_expired=fields.Boolean(string="是否过期",compute="_compute_is_expired")

	@api.depends("deadline")
	@api.multi #将数据
	def _compute_is_expired(self):
		for rec in self:
			if rec.deadline:
				rec.is_expired=rec.deadline < fields.Datetime.now()
			else:
				rec.is_expired=False

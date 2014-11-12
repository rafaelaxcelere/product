# -*- coding: utf-8 -*-

from openerp import models


class account_invoice_refund(models.Model):

    _inherit = 'account.invoice.refund'

    def compute_refund(self, cr, uid, ids, data_refund, context=None):
        res = super(account_invoice_refund, self).compute_refund(
            cr, uid, ids, data_refund, context=context)
        domain = res.get('domain', [])
        invoice_ids = context.get('active_ids', [])
        if not invoice_ids:
            return res
        sale_order_ids = self.pool['sale.order'].search(
            cr, uid, [('invoice_ids', 'in', invoice_ids)])
        invoice_obj = self.pool['account.invoice']
        refund_invoice_ids = invoice_obj.search(cr, uid, domain)
        origin = ', '.join([x.number for x in invoice_obj.browse(
            cr, uid, invoice_ids) if x.number])
        invoice_obj.write(cr, uid, refund_invoice_ids, {'origin': origin})
        for invoice_id in refund_invoice_ids:
            self.pool['sale.order'].write(
                cr, uid, sale_order_ids, {'invoice_ids': [(4, invoice_id)]})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# Copyright (c) 2023, test and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


frappe.whitelist()
def make_item(self,method):
	newdoc = frappe.new_doc("Item")
	newdoc.item_code = self.item_id
	newdoc.item_name = self.product_name
	newdoc.valuation_rate = self.price

	if not frappe.db.exists("UOM",self.unit):
		doc = frappe.new_doc("UOM")
		doc.uom_name = self.unit
		doc.save()
	else:
		newdoc.stock_uom = self.unit

	if not frappe.db.exists("GST HSN Code",self.hsn_code):
		doc1 = frappe.new_doc("GST HSN Code")
		doc1.hsn_code = self.hsn_code
		doc1.save()
		frappe.db.commit()
	else:
		newdoc.gst_hsn_code = self.hsn_code
	# print(frappe.get_doc("Item Group",{"item_group_name":self.business}))
	if not frappe.db.exists("Item Group",{"name":self.business}):
		# frappe.errprint("1")
		doc2=frappe.new_doc("Item Group")
		doc2.item_group_name = self.business
		doc2.is_group = 1
		doc2.save()
		frappe.db.commit()

	if not frappe.db.exists("Item Group",{"name":self.main_category, "parent_item_group":self.business}):
		doc3=frappe.new_doc("Item Group")
		doc3.item_group_name = self.main_category
		doc3.parent_item_group = self.business
		doc3.is_group = 1
		doc3.save()
		frappe.db.commit()

	if not frappe.db.exists("Item Group",{"name":self.category, "parent_item_group":self.main_category}):
		doc4=frappe.new_doc("Item Group")
		doc4.item_group_name = self.category
		doc4.parent_item_group = self.main_category
		doc4.is_group = 1
		doc4.save()
		frappe.db.commit()

	if not frappe.db.exists("Item Group",{"name":self.subcategory, "parent_item_group":self.category}):
		doc5=frappe.new_doc("Item Group")
		doc5.item_group_name = self.subcategory
		doc5.parent_item_group = self.category
		doc5.save()
	
	
	newdoc.item_group = self.subcategory
	newdoc.barcode = self.barcode
	newdoc.vendor = self.vendor
	newdoc.buyer = self.buyer
	newdoc.invent_color_id = self.invent_color_id
	newdoc.invent_style_id = self.invent_style_id
	newdoc.invent_size_id = self.invent_size_id
	newdoc.config_id = self.config_id
	newdoc.save()

	if not frappe.db.exists("Item Price",{"item_code" : self.item_id, "price_list":"Standard Buying"}):
		item_price = frappe.new_doc("Item Price")
		item_price.item_code = self.item_id
		item_price.price_list = "Standard Buying"
		item_price.price_list_rate = self.price
		item_price.save()
		frappe.db.commit()
	else:
		frappe.db.sql(""" update `tabItem Price` set price_list_rate = '{0}' where item_code = '{1}' """.format(self.rate,self.item_id))


class ItemMasterConnector(Document):
	pass

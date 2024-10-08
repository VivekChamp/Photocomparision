# Copyright (c) 2024, Sibikumar and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PatientImage(Document):
	@frappe.whitelist()
	def preview_image(self):
		if not self.patient:
			return ""
		if self.from_date and self.to_date:
			if self.from_date > self.to_date:
				frappe.throw(_("From Date is Greater then To Date"))
		
		filter = {
			"parenttype": "Patient Encounter"
		}
		get_pe = frappe.get_all("Patient Encounter", filters={"patient": self.patient}, pluck="name")
		filter['parent'] = ["in", get_pe]
			
		if self.from_date and self.to_date:
			filter['date'] = ["between",(self.from_date, self.to_date)]
		elif self.from_date:
			filter['date'] = [">", self.from_date]
		elif self.to_date:
			filter['date'] = ["<", self.to_date]
		get_img = frappe.get_all("Patient Health Image", filters=filter, fields=["image_file", "date"], order_by="date asc")
		html = '''
			<html>
				<style>
					body {
						font-family: Arial, sans-serif;
						background-color: #f8f9fa;
						margin: 0;
						padding: 20px;
					}

					.gallery-container {
						display: flex;
						flex-wrap: wrap;
						justify-content: center;
						gap: 20px;
					}

					div.gallery {
						margin: 5px;
						border: 1px solid #ccc;
						width: 220px;
						border-radius: 8px;
						overflow: hidden;
						box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
						transition: transform 0.3s ease, box-shadow 0.3s ease;
					}

					div.gallery:hover {
						transform: translateY(-5px);
						box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
					}

					div.gallery img {
						width: 100%;
						height: auto;
						border-bottom: 1px solid #ddd;
					}

					div.desc {
						padding: 15px;
						text-align: center;
						background-color: #fff;
					}

					div.desc .date {
						font-size: 14px;
						color: #555;
					}

					div.desc:hover {
						color: #007bff;
					}
				</style>
				<body>
					<div class="gallery-container">
		'''
		for i in get_img:
			html += f'''
						<div class="gallery">
							<a target="_blank" href="{i.image_file}">
								<img src="{i.image_file}" alt="No Image" width="600" height="400">
							</a>
							<div class="desc">
								<p>Date: <span class="date">{i.date}</span></p>
							</div>
						</div>
					'''
		html += '''
					</div>
				</body>
			</html>
		'''

		return html


import frappe
from frappe import _
import json

@frappe.whitelist()
def preview_image(self):
    self = json.loads(self)
    if not self.get('patient'):
        return "", ""
    if self.get('custom_from_date') and self.get('custom_to_date'):
        if self.get('custom_from_date') > self.get('custom_to_date'):
            frappe.throw(_("From Date is Greater then To Date"))
    
    filter = {
        "parenttype": "Patient Encounter"
    }
    get_pe = frappe.get_all("Patient Encounter", filters={"patient": self.get('patient')}, pluck="name")
    filter['parent'] = ["in", get_pe]
    filter["date"] = self.get('custom_from_date')
    from_get_img = frappe.get_all("Patient Health Image", filters=filter, fields=["image_file", "date"], order_by="date asc")
    filter["date"] = self.get('custom_to_date')
    to_get_img = frappe.get_all("Patient Health Image", filters=filter, fields=["image_file", "date"], order_by="date asc")
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
    from_html = to_html = html
    if self.get('custom_from_date'):
        for i in from_get_img:
            from_html += f'''
                        <div class="gallery">
                            <a target="_blank" href="{i.image_file}">
                                <img src="{i.image_file}" alt="No Image" width="600" height="400">
                            </a>
                            <div class="desc">
                                <p>Date: <span class="date">{i.date}</span></p>
                            </div>
                        </div>
                    '''
    elif self.get('docstatus') == 0:
        from_html += ''' <h3>Select From Date...</h3> '''
    if self.get('custom_to_date'):
        for i in to_get_img:
            to_html += f'''
                        <div class="gallery">
                            <a target="_blank" href="{i.image_file}">
                                <img src="{i.image_file}" alt="No Image" width="600" height="400">
                            </a>
                            <div class="desc">
                                <p>Date: <span class="date">{i.date}</span></p>
                            </div>
                        </div>
                    '''
    elif self.get('docstatus') == 0:
        to_html += ''' <h3>Select To Date...</h3> '''
    end_html = '''
                </div>
            </body>
        </html>
    '''

    return from_html+end_html, to_html+end_html


// Copyright (c) 2024, Sibikumar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient Encounter", {
	refresh(frm) {
        if(frm.doc.docstatus == 0){
            if(!frm.doc.custom_from_date)frm.set_value("custom_from_date", frappe.datetime.get_today())
            if(!frm.doc.custom_to_date)frm.set_value("custom_to_date", frappe.datetime.get_today())
        }
        pre_image(frm)
	},
    custom_from_date(frm){
        pre_image(frm)
    },
    custom_to_date(frm){
        pre_image(frm)
    },
});

function pre_image(frm){
    console.log(frm.doc.custom_from_date, frm.doc.custom_to_date)
    if(!frm.doc.custom_from_date){
        frm.set_df_property("custom_from_html", "options", "<html><h2>Select From Date...</h2><html>")
    }
    if(!frm.doc.custom_to_date){
        frm.set_df_property("custom_to_html", "options", "<html><h2>Select To Date...</h2><html>")
    }
    frm.call({
        method: "healthcare_customization.healthcare_customization.customization.patient_encounter.patient_encounter.preview_image",
        args: {
            self: frm.doc
        },
        freeze: true,
        freeze_message: __("Reposting..."),
        callback: (r) => {
            if (r.message) {
                frm.set_df_property("custom_from_html", "options", r.message[0])
                frm.set_df_property("custom_to_html", "options", r.message[1])
            }
        },
    });
}
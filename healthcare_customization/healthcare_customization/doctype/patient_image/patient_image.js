// Copyright (c) 2024, Sibikumar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient Image", {
	refresh(frm) {
        frm.set_value("from_date", frappe.datetime.get_today())
        frm.set_value("to_date", frappe.datetime.get_today())
        frm.set_value("patient", "")
        pre_image(frm)
	},
    patient(frm){
        pre_image(frm)
    },
    from_date(frm){
        pre_image(frm)
    },
    to_date(frm){
        pre_image(frm)
    },
});

function pre_image(frm){
    if(!frm.doc.patient){
        frm.set_df_property("image_preview", "options", "<html><h2>Select Patient...</h2><html>")
    }
    frm.call({
        doc: frm.doc,
        method: "preview_image",
        freeze: true,
        freeze_message: __("Reposting..."),
        callback: (r) => {
            if (r.message) {
                frm.set_df_property("image_preview", "options", r.message)
            }
        },
    });
    
}
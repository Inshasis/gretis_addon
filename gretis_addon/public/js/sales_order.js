frappe.ui.form.on("Sales Order", {
    month: function(frm) {
        if (frm.doc.month) {
            frappe.call({
                method: "gretis_addon.gretis_addon.custom.sales_order.get_salary_details",
                args: {
                    project: frm.doc.project,
                    month: frm.doc.month
                },
                callback: function(r) {
                    console.log(r.message)
                    if (r.message) {
                        frappe.model.clear_table(frm.doc, 'items');
                        let row = frm.add_child("items");
                        row.item_code = 'Basic';
                        row.item_name = 'Basic';
                        row.description = 'Basic'
                        row.qty = 1;
                        row.uom = 'Nos'
                        row.rate = r.message;
                    }
                    frm.refresh_field("items");
                }
            })
        }
    }
})
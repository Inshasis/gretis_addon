// Copyright (c) 2023, Inshasis and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Tool Company Wise', {
	branch:function(frm) {
    
        frappe.db.get_list('Employee',{ 
        fields:['name'], 
        filters:{
            'company': frm.doc.company,
            'department': frm.doc.department,
            'branch': frm.doc.branch
        } 
        }).then(function(r){ 
            console.log(r); 
            frm.clear_table("attendance_tool_company_wise_child");
            for(let rec of  r){
                let row = frm.add_child("attendance_tool_company_wise_child");
                row.employee = rec.name;
                
                frm.refresh_field("attendance_tool_company_wise_child");
            }
            
        });
    }
});

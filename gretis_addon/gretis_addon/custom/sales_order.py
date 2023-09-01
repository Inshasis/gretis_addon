import frappe

@frappe.whitelist()
def get_salary_details(project, month):
    month_ = frappe.db.sql("select month(str_to_date('{}','%b'))".format(month))[0][0]

    get_base_total_amount = frappe.db.sql("""
        select 
            coalesce(sum(sd.amount), 0) as amount
        from
            `tabSalary Slip` ss
        join
            `tabSalary Detail` sd
        on
            ss.name = sd.parent
        join
            `tabEmployee` emp
        on 
            ss.employee = emp.name
        where
            emp.project = '{}' and
            month(ss.end_date) = '{}' and
            ss.docstatus = 1 and sd.salary_component = 'Basic Salary'
        """.format(project, month_))
    return get_base_total_amount[0][0]
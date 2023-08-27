# Copyright (c) 2023, Inshasis and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class AttendanceToolCompanyWise(Document):
	def before_submit(self):
		if not self.month:
			frappe.throw('Please Select Month...')
		for i in self.get("attendance_tool_company_wise_child"):
			dates = [
				{
					'date': 1,
					'status': i.get('1')
				},
				{
					'date': 2,
					'status': i.get('2')
				},
				{
					'date': 3,
					'status': i.get('3')
				},
				{
					'date': 4,
					'status': i.get('4')
				},
				{
					'date': 5,
					'status': i.get('5')
				},
				{
					'date': 6,
					'status': i.get('6')
				},
				{
					'date': 7,
					'status': i.get('7')
				},
				{
					'date': 8,
					'status': i.get('8')
				},
				{
					'date': 9,
					'status': i.get('9')
				},
				{
					'date': 10,
					'status': i.get('10')
				},
				{
					'date': 11,
					'status': i.get('11')
				},
				{
					'date': 12,
					'status': i.get('12')
				},
				{
					'date': 13,
					'status': i.get('13')
				},
				{
					'date': 14,
					'status': i.get('14')
				},
				{
					'date': 15,
					'status': i.get('15')
				},
				{
					'date': 16,
					'status': i.get('16')
				},
				{
					'date': 17,
					'status': i.get('17')
				},
				{
					'date': 18,
					'status': i.get('18')
				},
				{
					'date': 19,
					'status': i.get('19')
				},
				{
					'date': 20,
					'status': i.get('20')
				},
				{
					'date': 21,
					'status': i.get('21')
				},
				{
					'date': 22,
					'status': i.get('22')
				},
				{
					'date': 23,
					'status': i.get('23')
				},
				{
					'date': 24,
					'status': i.get('24')
				},
				{
					'date': 25,
					'status': i.get('25')
				},
				{
					'date': 26,
					'status': i.get('26')
				},
				{
					'date': 27,
					'status': i.get('27')
				},
				{
					'date': 28,
					'status': i.get('28')
				},
				{
					'date': 29,
					'status': i.get('29')
				},
				{
					'date': 30,
					'status': i.get('30')
				},
				{
					'date': 31,
					'status': i.get('31')
				},
			]
			month = frappe.db.sql("select month(str_to_date('{}','%b'))".format(self.month))[0][0]
			
			doj = frappe.db.get_value("Employee", i.employee, 'date_of_joining')
			
			from frappe.utils import getdate
			year = getdate(self.date).year

			ot = 0
			ot_hrs = 0
			for o in dates:
				if o.get('status') == 'OT With Present':
					ot += 1

			if i.hrs:
				if ot != 0:
					ot_hrs = int(i.hrs) / ot
				else:
					ot_hrs = 0
			
			import datetime, calendar
			num_days = calendar.monthrange(year, month)[1]
			for day in range(1, num_days+1):
				checkin_date = datetime.date(year, month, day)
				if doj < checkin_date:
					in_time = None
					out_time = None
					status = None
					ot = 0
					for d in dates:
						
						if d.get('date') == checkin_date.day:
							
							if d.get('status') in ('Present', 'OT With Present'):
								in_time = str(checkin_date) + ' 10:00:00'
							
							if d.get('status') == 'Present':
								out_time = str(checkin_date) + ' 06:00:00'

							elif d.get('status') == 'OT With Present':
								time = datetime.datetime.strptime("02:00:00", "%H:%M:%S")+datetime.timedelta(hours=ot_hrs)
								out_time = str(checkin_date) + ' {}'.format(time.time())

								# create timesheet for ot

								emp_timesheet = frappe.new_doc('Timesheet')
								emp_timesheet.company = self.company
								emp_timesheet.employee = i.employee
								emp_timesheet.append('time_logs', {
									'activity_type': 'Regular OT',
									'from_time': str(checkin_date) + ' 02:00:00',
									'to_time': out_time,
									'hours': ot_hrs
								})
								emp_timesheet.save(ignore_permissions=True)
								emp_timesheet.submit()

							if d.get('status') == 'Absent':
								status = d.get('status')

								# create attendance for Absent employee
								
								create_attendance = frappe.new_doc('Attendance')
								create_attendance.employee = i.employee
								create_attendance.status = 'Absent'
								create_attendance.attendance_date = checkin_date
								create_attendance.save(ignore_permissions=True)
								create_attendance.submit()

					if status == 'Absent':
						continue
									
					create_checkins(i.employee, 'IN', in_time)
					create_checkins(i.employee, 'OUT', out_time)
			
def create_checkins(employee, log_type, time):
	emp_checkin = frappe.new_doc("Employee Checkin")
	emp_checkin.employee = employee
	emp_checkin.log_type = log_type
	emp_checkin.time = time
	emp_checkin.save(ignore_permissions=True)
	

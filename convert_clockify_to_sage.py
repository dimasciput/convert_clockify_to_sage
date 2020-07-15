#!/usr/bin/python

import sys
import csv
import os

def convert():
	converted_data = {}
	if len(sys.argv) == 1:
		print('File path for the clockify report not provided')
		return
	file_path = sys.argv[1]
	if not os.path.exists(file_path):
		print('File does not exist')
		return
	with open(file_path) as csv_file:
		csv_dict_reader = csv.DictReader(csv_file)
		for row in csv_dict_reader:
			if row['Start Date'] not in converted_data:
				converted_data[row['Start Date']] = {}
			converted_data_date = converted_data[row['Start Date']]
			if row['Client'] not in converted_data_date:
				converted_data_date[row['Client']] = {}
			converted_data_customer = converted_data_date[row['Client']]
			if row['Project'] not in converted_data_customer:
				converted_data_customer[row['Project']] = {}
			converted_data_project = converted_data_customer[row['Project']]
			if row['Task'] not in converted_data_project:
				converted_data_project[row['Task']] = {}
			converted_data_task = converted_data_project[row['Task']]
			if row['Description'] not in converted_data_task:
				converted_data_task[row['Description']] = float(row['Duration (decimal)'])
			else:
				converted_data_task[row['Description']] += float(row['Duration (decimal)'])
		print(converted_data)

	filename, file_extension = os.path.splitext(file_path)
	converted_file_name = '{name}_converted{ext}'.format(name=filename, ext=file_extension)
	print(converted_file_name)
	with open(converted_file_name, mode='w') as converted_csv_file:
		writer = csv.writer(
			converted_csv_file, delimiter=',', quotechar='"',
			quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['Date', 'Customer', 'Project Name', 'Comment', 'Task', 'Hours'])
		for date in converted_data:
			for client in converted_data[date]:
				for project in converted_data[date][client]:
					for task in converted_data[date][client][project]:
						for comment in converted_data[date][client][project][task]:
							writer.writerow([date, client, project, comment, task, converted_data[date][client][project][task][comment]])

convert()


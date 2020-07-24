#!/usr/bin/python

import sys
import csv
import os
import requests
import json

workspace_url = 'https://api.clockify.me/api/v1/workspaces'
headers = {'X-Api-Key': sys.argv[1], 'Content-Type': 'application/json'}
start_date = sys.argv[2]
end_date = sys.argv[3]

def convert_to_sage(clockify_data):
	converted_data = {}
	print(clockify_data)
	for row in clockify_data['timeentries']:
		start_date = row['timeInterval']['start'].split('T')[0]
		if start_date not in converted_data:
			converted_data[start_date] = {}
		converted_data_date = converted_data[start_date]
		if row['clientName'] not in converted_data_date:
			converted_data_date[row['clientName']] = {}
		converted_data_customer = converted_data_date[row['clientName']]
		if row['projectName'] not in converted_data_customer:
			converted_data_customer[row['projectName']] = {}
		converted_data_project = converted_data_customer[row['projectName']]
		if 'taskName' in row:
			task_name = row['taskName']
		else:
			task_name = '-'
		if task_name not in converted_data_project:
			converted_data_project[task_name] = {}
		converted_data_task = converted_data_project[task_name]
		if row['description'] not in converted_data_task:
			converted_data_task[row['description']] = float(row['timeInterval']['duration']) / 3600
		else:
			converted_data_task[row['description']] += float(row['timeInterval']['duration']) / 3600
	print(converted_data)

	converted_file_name = 'sage_report.csv'
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

def request_clockify_data():
	response = requests.get(workspace_url, headers=headers)
	response_content = json.loads(response.content)
	for workspace in response_content:
		workspace_id = workspace['id']
		report_url = 'https://reports.api.clockify.me/v1/workspaces/{workspace}/reports/detailed'.format(workspace=workspace_id)
		payload = {
		  "dateRangeStart": "{start_date}T00:00:00.000Z".format(start_date=start_date),
		  "dateRangeEnd": "{end_date}T23:59:59.999Z".format(end_date=end_date),
		  "detailedFilter": {
		    "sortColumn": "DATE",
		    "page": 1,
		    "pageSize": 50
		  }
		}
		response = requests.post(report_url, json.dumps(payload), headers=headers)
		convert_to_sage(json.loads(response.content))

request_clockify_data()


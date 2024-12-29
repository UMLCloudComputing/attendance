import boto3
import csv
import os

AWS_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
USER_TABLENAME = os.getenv("DYNAMO_USERTABLE")

def generate_report(report_semester: str) -> bytes:
    filename = '/tmp/attendance-report-' + report_semester.lower().replace(' ', '-') + '.csv'

    dynamodb = boto3.client("dynamodb")

    response = dynamodb.scan(
        TableName=USER_TABLENAME,
        Select="ALL_ATTRIBUTES"
    )

    fp = open(filename, 'w')
    csvwriter = csv.DictWriter(fp, fieldnames=['meeting_name', 'total_attended', 'in_person', 'virtual'])
    csvwriter.writeheader()
    data = {}
    
    for item in response['Items']:
        for event in item['events_attended']['L']:
            try:
                name, type, semester = event['S'].split('|')
            except ValueError:
                name, type = event['S'].split('|')
                semester = "Fall 2024"


            if semester == report_semester:
                if name not in data.keys():
                    data[name] = {
                        'total_attended': 0,
                        'in_person': 0,
                        'virtual': 0
                    }
                    
                data[name][type.lower().replace(' ', '_')] += 1
                data[name]['total_attended'] += 1

    rows = []
    for event in data.keys():
        row = {
            'meeting_name': event,
            'total_attended': data[event]['total_attended'],
            'in_person': data[event]['in_person'],
            'virtual': data[event]['virtual']
        }
        rows.append(row)
    csvwriter.writerows(rows)

    return filename
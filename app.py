#!/usr/bin/env python3
import os
import aws_cdk as cdk

from attendance.attendance_stack import AttendanceStack


app = cdk.App()
AttendanceStack(app, os.getenv("APP_NAME"),)
app.synth()

"""Constants for the infinitecampus integration."""

from datetime import timedelta

NAME = "Infinite Campus"
DOMAIN = "infinitecampus"
VERSION = "0.0.1"

HA_SENSOR = ["sensor"]

SCAN_INT = timedelta(minutes=1)

CONF_BASEURI = "baseuri"
CONF_DISTRICT = "district"
CONF_SECRET = "password"
CONF_USERNAME = "username"

STUDENTS = "Student(s)"
COURSES = "Course(s)"
ASSIGNMENTS = "Assignment(s)"

ATTR_STUDENTS = "_students"
ATTR_COURSES = "_courses"
ATTR_ASSIGNMENTS = "_assignments"
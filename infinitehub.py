"""Infinite Campus Hub."""
from __future__ import annotations

import logging
from typing import Any

from .ic_parent_api import InfiniteCampus
from .ic_parent_api.models.assignment import Assignment
from .ic_parent_api.models.course import Course
from .ic_parent_api.models.student import Student
from .ic_parent_api.models.term import Term
from .ic_parent_api.models.grade import Grade
from .ic_parent_api.models.attendance import Attendance
from .ic_parent_api.models.message import Message

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_BASEURI,
    CONF_DISTRICT,
    CONF_SECRET,
    CONF_USERNAME,
    DOMAIN,
    SCAN_INT,
)

_LOGGER = logging.getLogger(__name__)


class InfiniteHub(DataUpdateCoordinator[dict[str, Any]]):
    """Infinite Campus Hub definition."""

    config_entry: config_entries.ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: config_entries.ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INT,
        )
        self.config_entry = entry

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._username = self.config_entry.data[CONF_USERNAME]
        self._secret = self.config_entry.data[CONF_SECRET]
        self._district = self.config_entry.data[CONF_DISTRICT]
        self._client = InfiniteCampus(
            f"{self._baseuri}",
            f"{self._username}",
            f"{self._secret}",
            f"{self._district}",
        )

    async def poll_students(self) -> list[Student]:
        """Get Students Data."""
        return await self._client.students()

    async def poll_terms(self) -> list[Term]:
        """Get Terms."""
        return await self._client.terms()

    async def poll_courses(self) -> list[Course]:
        """Get Courses."""
        courses: list[Course] = []
        students = await self.poll_students()
        for student in students:
            courseresp = await self._client.courses(student.personid)
            courses.extend(
                [course for course in courseresp if hasattr(course, "rosterid")]
            )
        return courses

    async def poll_assignments(self) -> list[Assignment]:
        """Get Assignments."""
        assignments: list[Assignment] = []
        students = await self.poll_students()
        for student in students:
            assignmentresp = await self._client.assignments(student.personid)
            assignments.extend(
                [
                    assignment
                    for assignment in assignmentresp
                    if hasattr(assignment, "objectsectionid")
                ]
            )
        return assignments

    async def poll_grades(self) -> list[dict]:
        """Get Grades for all students."""
        grades_data: list[dict] = []
        students = await self.poll_students()
        for student in students:
            gradesresp = await self._client.grades(student.personid)
            for grade in gradesresp:
                for term in grade.terms:
                    for course in term.courses:
                        grades_data.append({
                            "student_name": f"{student.firstname} {student.lastname}",
                            "student_id": student.personid,
                            "term_name": term.termname,
                            "course_name": course.coursename,
                            "grade": course.grade,
                            "teacher": course.teacherdisplay,
                        })
        return grades_data

    async def poll_attendance(self) -> list[dict]:
        """Get Attendance for all students."""
        attendance_data: list[dict] = []
        students = await self.poll_students()
        for student in students:
            for enrollment in student.enrollments:
                attendanceresp = await self._client.attendance(
                    enrollment.enrollmentid, student.personid
                )
                for term in attendanceresp.terms:
                    attendance_data.append({
                        "student_name": f"{student.firstname} {student.lastname}",
                        "student_id": student.personid,
                        "term_name": term.termname,
                        "total_absent": term.totalabsent,
                        "total_tardy": term.totaltardy,
                    })
        return attendance_data

    async def poll_messages(self) -> list[dict]:
        """Get Inbox Messages with full content."""
        messages_data: list[dict] = []
        messages = await self._client.messages()
        for msg in messages:
            # Fetch full message details including body
            detail = await self._client.message_detail(msg)
            messages_data.append({
                "messageid": msg.messageid,
                "subject": msg.subject,
                "date": msg.date,
                "sender": msg.sender,
                "studentname": msg.studentname,
                "coursename": msg.coursename,
                "actionrequired": msg.actionrequired,
                "newmessage": msg.newmessage,
                "duedate": msg.duedate,
                "body": detail.body_text if detail else None,
            })
        return messages_data

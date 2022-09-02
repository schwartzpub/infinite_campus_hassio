"""Infinite Campus Hub."""
from __future__ import annotations

import logging
from typing import Any

from ic_parent_api import InfiniteCampus
from ic_parent_api.models.assignment import Assignment
from ic_parent_api.models.course import Course
from ic_parent_api.models.student import Student
from ic_parent_api.models.term import Term

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

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INT,
        )

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

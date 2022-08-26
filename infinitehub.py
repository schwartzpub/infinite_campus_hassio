"""Infinite Campus Hub."""
from __future__ import annotations

from datetime import date, datetime
import logging
from typing import Any

import aiohttp

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

    async def authenticate(self, session) -> bool:
        """Test if we can authenticate with the district."""
        async with session.post(
            "{}/campus/verify.jsp?nonBrowser=true&username={}&password={}&appName={}&portalLoginPage={}".format(
                self._baseuri, self._username, self._secret, self._district, "parents"
            )
        ) as authresponse:
            response = authresponse
            return bool(
                response.status == 200 and "password-error" not in await response.text()
            )

    async def poll_students(self) -> list:
        """Get Students Data."""
        students = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(
                    f"{self._baseuri}/campus/api/portal/students"
                ) as studentresp:
                    studentresponse = await studentresp.json()
                    for student in studentresponse:
                        student["scheduleDays"] = (
                            await self.poll_scheduledays(
                                student["enrollments"][0]["calendarID"]
                            )
                            if len(student["enrollments"]) > 0
                            else ""
                        )
                        students.append(student)
                    return students
            else:
                return []

    async def poll_term(self) -> str:
        """Get Terms."""
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(
                    f"{self._baseuri}/campus/resources/term?structureID=1063",
                    headers={"Accept": "application/json"},
                ) as termresp:
                    terms = await termresp.json()
                    today = date.today().strftime("%Y-%m-%d")

                    for term in terms:
                        # _LOGGER.warning(term)
                        if term["startDate"] <= today <= term["endDate"]:
                            return term["termID"]

                    return ""
            return ""

    async def poll_scheduledays(self, calendarid) -> list:
        """Get Schedule Days."""
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(
                    f"{self._baseuri}/campus/resources/calendar/instructionalDay?calendarID={calendarid}"
                ) as dayresp:
                    daysresponse = await dayresp.json()
        return daysresponse

    async def poll_courses(self) -> list:
        """Get Courses."""
        term = await self.poll_term()
        courses = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(
                    f"{self._baseuri}/campus/api/portal/students",
                    headers={"Accept": "application/json"},
                ) as studentresp:
                    studentresponse = await studentresp.json()
                    for student in studentresponse:
                        async with session.get(
                            "{}/campus/resources/portal/roster?&personID={}".format(
                                self._baseuri, str(student["personID"])
                            ),
                            headers={"Accept": "application/json"},
                        ) as courseresp:
                            courseresponse = await courseresp.json()
                            for section in courseresponse:
                                for placement in section["sectionPlacements"]:
                                    if placement["termID"] == term:
                                        placement["personID"] = student["personID"]
                                        courses.append(placement)
                return courses
            return []

    async def poll_assignments(self) -> list:
        """Get Assignments."""
        term = await self.poll_term()
        assignments = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(
                    f"{self._baseuri}/campus/api/portal/students",
                    headers={"Accept": "application/json"},
                ) as studentresp:
                    studentresponse = await studentresp.json()
                    students = []
                    for student in studentresponse:
                        students.append(student["personID"])
                        async with session.get(
                            "{}/campus/api/portal/assignment/listView?&personID={}".format(
                                self._baseuri, str(student["personID"])
                            ),
                            headers={"Accept": "application/json"},
                        ) as assignmentresp:
                            assignmentresponse = await assignmentresp.json()
                            for assignment in assignmentresponse:
                                if assignment["dueDate"]:
                                    assignment["dueDate"] = datetime.strptime(
                                        assignment["dueDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
                                    ).strftime("%Y-%m-%d (%H:%M:%S)")
                                if term in assignment["termIDs"]:
                                    assignments.append(assignment)
                return assignments
            return []

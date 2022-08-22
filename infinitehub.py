from __future__ import annotations

import logging
import aiohttp

from typing import Any, Dict
from datetime import datetime, date

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_USERNAME,
    CONF_BASEURI,
    CONF_DISTRICT,
    CONF_SECRET,
    DOMAIN,
    SCAN_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

class InfiniteHub(DataUpdateCoordinator[Dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._username = self.config_entry.data[CONF_USERNAME]
        self._secret = self.config_entry.data[CONF_SECRET]
        self._district = self.config_entry.data[CONF_DISTRICT]

    async def authenticate(self, session) -> bool:
        """Test if we can authenticate with the district."""
        async with session.post('{0}/campus/verify.jsp?nonBrowser=true&username={1}&password={2}&appName={3}&portalLoginPage={4}'.format(self._baseuri,self._username,self._secret,self._district,'parents')) as authresponse:
            response = authresponse
            if response.status == 200 and "password-error" not in await response.text():
                return True
            else:
                return False

    async def poll_students(self) -> str:
        """Get Students Data"""
        students = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get('{0}/campus/api/portal/students'.format(self._baseuri)) as studentresp:
                    studentresponse = await studentresp.json()
                    for student in studentresponse:
                        student["scheduleDays"] = await self.poll_scheduleDays(student["enrollments"][0]["calendarID"]) if len(student["enrollments"]) > 0 else ""
                        students.append(student)
                    return students
            else:
                return False

    async def poll_term(self) -> str:
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get('{0}/campus/resources/term?structureID=1002'.format(self._baseuri),headers={'Accept': 'application/json'}) as termresp:
                    terms = await termresp.json()
                    today = date.today().strftime("%Y-%m-%d")

                    for term in terms:
                        if term["startDate"] <= today and term["endDate"] >= today:
                            return term["termID"]

                    return False

    async def poll_scheduleDays(self,calendarID) -> str:
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get('{0}/campus/resources/calendar/instructionalDay?calendarID={1}'.format(self._baseuri,calendarID)) as dayresp:
                    daysresponse = await dayresp.json()
        return daysresponse

    async def poll_courses(self) -> str:
        term = await self.poll_term()
        courses = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get('{0}/campus/api/portal/students'.format(self._baseuri),headers={'Accept': 'application/json'}) as studentresp:
                    studentresponse = await studentresp.json()
                    for student in studentresponse:
                        async with session.get('{0}/campus/resources/portal/roster?&personID={1}'.format(self._baseuri,str(student["personID"])),headers={'Accept': 'application/json'}) as courseresp:
                            courseresponse = await courseresp.json()
                            for section in courseresponse:
                                for placement in section["sectionPlacements"]:
                                    if placement["termID"] == term:
                                        placement["personID"] = student["personID"]
                                        courses.append(placement)
                return courses

    async def poll_assignments(self) -> str:
        term = await self.poll_term()
        assignments = []
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get('{0}/campus/api/portal/students'.format(self._baseuri),headers={'Accept': 'application/json'}) as studentresp:
                    studentresponse = await studentresp.json()
                    students = []
                    for student in studentresponse:
                        students.append(student["personID"])
                        async with session.get('{0}/campus/api/portal/assignment/listView?&personID={1}'.format(self._baseuri,str(student["personID"])),headers={'Accept': 'application/json'}) as assignmentresp:
                            assignmentresponse = await assignmentresp.json()
                            for assignment in assignmentresponse:
                                if (assignment["dueDate"]):
                                    assignment["dueDate"] = datetime.strptime(assignment["dueDate"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d (%H:%M:%S)")
                                if term in assignment["termIDs"]:
                                    assignments.append(assignment)
                return assignments
from __future__ import annotations

import logging

from typing import Any

from homeassistant.core import HomeAssistant

import aiohttp

_LOGGER = logging.getLogger(__name__)

class InfiniteHub:
    def __init__(self, hass: HomeAssistant, district: str, baseuri: str, username: str, password: str) -> None:
        """Initialize."""
        self._district = district
        self._baseuri = baseuri
        self._hass = hass
        self._username = username
        self._secret = password
        self._id = district.lower()

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the district."""
        async with aiohttp.ClientSession() as session:
            async with session.post('{0}/campus/verify.jsp?nonBrowser=true&username={1}&password={2}&appName={3}&portalLoginPage={4}'.format(self._baseuri,self._username,self._secret,self._district,'parents')) as authresponse:
                response = authresponse
                if response.status == 200 and "password-error" not in await response.text():
                    return True
                else:
                    return False
        
    async def poll_data(self,type) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post('{0}/campus/verify.jsp?nonBrowser=true&username={1}&password={2}&appName={3}&portalLoginPage={4}'.format(self._baseuri,self._username,self._secret,self._district,'parents')) as authresponse:
                response = authresponse
                if response.status == 200 and "password-error" not in await response.text():
                    async with session.get('{0}/campus/resources/prism/portal/familyInfo'.format(self._baseuri)) as studentresp:
                        studentresponse = await studentresp.text()
                        return studentresponse
                else:
                    return False
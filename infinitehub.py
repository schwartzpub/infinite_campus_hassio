from __future__ import annotations

import logging
import aiohttp

from typing import Any, Dict

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
        if type == "student":
            async with aiohttp.ClientSession() as session:
                async with session.post('{0}/campus/verify.jsp?nonBrowser=true&username={1}&password={2}&appName={3}&portalLoginPage={4}'.format(self._baseuri,self._username,self._secret,self._district,'parents')) as authresponse:
                    response = authresponse
                    if response.status == 200 and "password-error" not in await response.text():
                        async with session.get('{0}/campus/resources/prism/portal/familyInfo'.format(self._baseuri)) as studentresp:
                            studentresponse = await studentresp.text()
                            return studentresponse
                    else:
                        return False
        elif type == "course":
            return False
        elif type == "assignment":
            return False
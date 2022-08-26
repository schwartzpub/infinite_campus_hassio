"""Config flow for infinitecampus integration."""
from __future__ import annotations

import logging
import aiohttp
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    NAME,
    CONF_SECRET,
    CONF_USERNAME,
    CONF_BASEURI,
    CONF_DISTRICT,
    DOMAIN,
    VERSION
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASEURI): str,
        vol.Required(CONF_DISTRICT): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_SECRET): str
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    async with aiohttp.ClientSession() as session:
            async with session.post('{0}/campus/verify.jsp?nonBrowser=true&username={1}&password={2}&appName={3}&portalLoginPage={4}'.format(data[CONF_BASEURI].rstrip('/'),data[CONF_USERNAME],data[CONF_SECRET],data[CONF_DISTRICT],'parents')) as authresponse:
                response = authresponse
                if response.status == 200 and "password-error" not in await response.text():
                    return {
                        "title": NAME, 
                        CONF_BASEURI: data[CONF_BASEURI].rstrip('/'), 
                        CONF_DISTRICT: data[CONF_DISTRICT], 
                        CONF_USERNAME: data[CONF_USERNAME], 
                        CONF_SECRET: data[CONF_SECRET]
                    }
                if response.status != 200:
                    raise CannotConnect
                raise InvalidAuth

@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for infinitecampus."""

    VERSION = VERSION

    async def async_step_user(self, user_input: None): # pylint: disable=signature-differs
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

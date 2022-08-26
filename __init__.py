"""The infinitecampus integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, HA_SENSOR
from .infinitehub import InfiniteHub

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Set up init."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up infinitecampus from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = InfiniteHub(hass)

    # _LOGGER.warning("-------SETTING UP PLATFORMS--------")

    hass.config_entries.async_setup_platforms(entry, HA_SENSOR)

    # _LOGGER.warning("-------COMPLETED SETTING UP PLATFORMS---------")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, HA_SENSOR):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

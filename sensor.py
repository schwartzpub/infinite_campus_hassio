"""Platform for sensor integration."""
from __future__ import annotations
from datetime import timedelta
from homeassistant.components import infinitecampus

from homeassistant.components.sensor import (
    SCAN_INTERVAL,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)

CONF_BASEURI= "baseuri"
CONF_USERNAME= "username"
CONF_SECRET= "password"
CONF_DISTRICT= "district"

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass,config_entry,async_add_entities):
    """Set up the sensor platform."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([InfiniteStudentSensor(hass,hub)])

class InfiniteStudentSensor(SensorEntity):
    def __init__(
        self,
        hass: HomeAssistant,
        hub: infinitecampus.InfiniteHub
    ) -> None:
        self._attr_name = "Infinite Campus Student"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "ic_student"
        self._hub = hub
        self._hass = hass

    async def async_update(self) -> str:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = await self._hub.poll_data("student")

class InfiniteCourseSensor(SensorEntity):
    def __init__(
        self,
        unique_id
    ) -> None:
        self._attr_unique_id = unique_id
        self._attr_name = "Infinite Campus Course"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 23

class InfiniteAssignmentSensor(SensorEntity):
    def __init__(
        self,
        unique_id
    ) -> None:
        self._attr_unique_id = unique_id
        self._attr_name = "Infinite Campus Assignment"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 23
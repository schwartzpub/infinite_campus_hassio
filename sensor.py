"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN, SCAN_INT

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = SCAN_INT


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            InfiniteStudentSensor(hass, hub),
            InfiniteCourseSensor(hass, hub),
            InfiniteAssignmentSensor(hass, hub),
        ]
    )


class InfiniteStudentSensor(SensorEntity):
    """Infinite Campus Student entity definition."""

    def __init__(self, hass: HomeAssistant, hub) -> None:
        """Init Student sensor."""
        self._attr_name = "Infinite Campus Students"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "ic_student"
        self._hub = hub
        self._hass = hass
        self._attr_json = "test"

    @property
    def extra_state_attributes(self):
        """Set up extra attributes."""
        return {"json": self._attr_json}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_json = await self._hub.poll_students()
        return


class InfiniteCourseSensor(SensorEntity):
    """Infinite Campus Course entity definition."""

    def __init__(self, hass: HomeAssistant, hub) -> None:
        """Init Course sensor."""
        self._attr_name = "Infinite Campus Courses"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "ic_course"
        self._hub = hub
        self._hass = hass
        self._attr_json = "test"

    @property
    def extra_state_attributes(self):
        """Add extra attributes."""
        return {"json": self._attr_json}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_json = await self._hub.poll_courses()
        return


class InfiniteAssignmentSensor(SensorEntity):
    """Infinite Campus Assignment entity definition."""

    def __init__(self, hass: HomeAssistant, hub) -> None:
        """Init Assignment Sensor."""
        self._attr_name = "Infinite Campus Assignments"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "ic_assignment"
        self._hub = hub
        self._hass = hass
        self._attr_json = "test"

    @property
    def extra_state_attributes(self):
        """Add extra attributes."""
        return {"json": self._attr_json}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_json = await self._hub.poll_assignments()
        return

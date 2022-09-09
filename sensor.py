"""Platform for sensor integration."""
from __future__ import annotations

import logging

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SCAN_INT

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = SCAN_INT


@dataclass
class InfiniteCampusEntityDescriptionMixIn:
    """Mixin for required keys."""

    value_fn: Callable
    unique_id: str


@dataclass
class InfiniteCampusEntityDescription(
    SensorEntityDescription, InfiniteCampusEntityDescriptionMixIn
):
    """Describes Infinite Campus sensor entity."""


SENSORS: tuple[InfiniteCampusEntityDescription, ...] = (
    InfiniteCampusEntityDescription(
        key="student",
        name="Infinite Campus Students",
        unique_id="ic_student",
        value_fn=lambda canvas: canvas.poll_students()
    ),
    InfiniteCampusEntityDescription(
        key="course",
        name="Infinite Campus Courses",
        unique_id="ic_course",
        value_fn=lambda canvas: canvas.poll_courses()
    ),
    InfiniteCampusEntityDescription(
        key="assignment",
        name="Infinite Campus Assignments",
        unique_id="ic_assignment",
        value_fn=lambda canvas: canvas.poll_assignments()
    ),
    InfiniteCampusEntityDescription(
        key="term",
        name="Infinite Campus Terms",
        unique_id="ic_term",
        value_fn=lambda canvas: canvas.poll_terms()
    )
)
async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
    ):
    """Set up the sensor platform."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [InfiniteCampusSensor(description, hub) for description in SENSORS],
        True,
    )


class InfiniteCampusSensor(SensorEntity):
    """Infinite Campus Sensor Definition."""
    entity_description: InfiniteCampusEntityDescription

    def __init__(
        self,
        description: InfiniteCampusEntityDescription,
        hub
    ) -> None:
        self._hub = hub
        self._attr_name = description.name
        self._attr_unique_id = f"{description.unique_id}"
        self._entity_description = description
        self._attr_infinite_campus_data = {}    

    @property
    def extra_state_attributes(self):
        """Add extra attribute."""
        return {f"{self._entity_description.key}": [x.as_dict() for x in self._attr_infinite_campus_data]}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_infinite_campus_data = await self._entity_description.value_fn(self._hub)
        return

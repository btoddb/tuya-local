"""
Setup for different kinds of Tuya water heater devices
"""

import logging
from enum import IntFlag

from homeassistant.helpers.entity import Entity

from .device import TuyaLocalDevice
from .entity import TuyaLocalEntity
from .helpers.config import async_tuya_setup_platform
from .helpers.device_config import TuyaEntityConfig

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    config = {**config_entry.data, **config_entry.options}
    await async_tuya_setup_platform(
        hass,
        async_add_entities,
        config,
        "coffee_maker",
        CoffeeMaker,
    )


class CoffeeMakerEntityFeature(IntFlag):
    """Supported features of the coffee maker entity."""

    CARAF_OFF_PAD = 1


class CoffeeMaker(TuyaLocalEntity, Entity):
    """Representation of a Tuya coffee maker entity."""

    def __init__(self, device: TuyaLocalDevice, config: TuyaEntityConfig):
        """
        Initialise the coffee maker device.
        Args:
           device (TuyaLocalDevice): The device API instance.
           config (TuyaEntityConfig): The entity config.
        """
        super().__init__()
        dps_map = self._init_begin(device, config)

        self._power_status = dps_map.pop(
            "power_status",
            None,
        )

        self._support_flags = CoffeeMakerEntityFeature(0)


    @property
    def supported_features(self):
        """Return the features supported by this coffee maker device."""
        return self._support_flags

    @property
    def power_status(self):
        """Return the power status of the coffee maker."""
        if self._power_status is None:
            return None
        return self._power_status.get_value(self._device)

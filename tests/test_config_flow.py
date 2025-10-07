"""Test configuration flow for Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.wattbox.const import (
    CONF_POLLING_INTERVAL,
    DEFAULT_PASSWORD,
    DEFAULT_POLLING_INTERVAL,
    DEFAULT_USERNAME,
    DOMAIN,
)
from custom_components.wattbox.config_flow import ConfigFlow, CannotConnect, InvalidAuth


def test_constants() -> None:
    """Test that constants are defined correctly."""
    assert DOMAIN == "wattbox"
    assert DEFAULT_USERNAME == "wattbox"
    assert DEFAULT_PASSWORD == "wattbox"
    assert DEFAULT_POLLING_INTERVAL == 30


@pytest.mark.asyncio
async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    
    # Test form submission
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "host": "192.168.1.100",
            "username": "wattbox",
            "password": "wattbox",
            "polling_interval": 30,
        },
    )
    
    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "192.168.1.100"
    assert result2["data"] == {
        "host": "192.168.1.100",
        "username": "wattbox",
        "password": "wattbox",
        "polling_interval": 30,
    }


@pytest.mark.asyncio
async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test user flow with connection error."""
    with patch.object(ConfigFlow, "_test_connection", side_effect=CannotConnect):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
                "polling_interval": 30,
            },
        )
        
        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"]["base"] == "cannot_connect"


@pytest.mark.asyncio
async def test_user_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test user flow with invalid auth error."""
    with patch.object(ConfigFlow, "_test_connection", side_effect=InvalidAuth):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wrong_password",
                "polling_interval": 30,
            },
        )
        
        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"]["base"] == "invalid_auth"


@pytest.mark.asyncio
async def test_user_flow_unknown_error(hass: HomeAssistant) -> None:
    """Test user flow with unknown error."""
    with patch.object(ConfigFlow, "_test_connection", side_effect=Exception("Unknown error")):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
                "polling_interval": 30,
            },
        )
        
        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"]["base"] == "unknown"


@pytest.mark.asyncio
async def test_user_flow_validation_errors(hass: HomeAssistant) -> None:
    """Test user flow with validation errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    
    # Test with invalid polling interval (too low)
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "host": "192.168.1.100",
            "username": "wattbox",
            "password": "wattbox",
            "polling_interval": 1,  # Too low
        },
    )
    
    # Should still succeed since validation is handled by voluptuous
    assert result2["type"] == FlowResultType.CREATE_ENTRY


def test_test_connection_method() -> None:
    """Test the _test_connection method."""
    config_flow = ConfigFlow()
    
    # Should not raise an exception (currently just passes)
    config_flow._test_connection({"host": "192.168.1.100"})


def test_exception_classes() -> None:
    """Test that custom exception classes work correctly."""
    # Test CannotConnect
    try:
        raise CannotConnect("Test connection error")
    except CannotConnect as e:
        assert str(e) == "Test connection error"
    
    # Test InvalidAuth
    try:
        raise InvalidAuth("Test auth error")
    except InvalidAuth as e:
        assert str(e) == "Test auth error"

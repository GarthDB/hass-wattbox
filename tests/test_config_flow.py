"""Config flow for Wattbox integration tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.wattbox.config_flow import (
    CannotConnect,
    ConfigFlow,
    InvalidAuth,
)
from custom_components.wattbox.const import (
    DEFAULT_PASSWORD,
    DEFAULT_POLLING_INTERVAL,
    DEFAULT_USERNAME,
)


def test_constants() -> None:
    """Test that constants are defined correctly."""
    assert DEFAULT_USERNAME == "wattbox"
    assert DEFAULT_PASSWORD == "wattbox"
    assert DEFAULT_POLLING_INTERVAL == 30


@pytest.mark.asyncio
async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    flow = ConfigFlow()
    flow.hass = hass

    # Test initial step
    result = await flow.async_step_user()

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    # Mock successful connection test
    with patch.object(flow, "_test_connection") as mock_test:
        mock_test.return_value = None  # No exception means success

        # Test form submission
        result2 = await flow.async_step_user(
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
                "polling_interval": 30,
            }
        )

        assert result2["type"] == FlowResultType.CREATE_ENTRY
        assert result2["title"] == "Wattbox 192.168.1.100"
        assert result2["data"] == {
            "host": "192.168.1.100",
            "username": "wattbox",
            "password": "wattbox",
            "polling_interval": 30,
        }


@pytest.mark.asyncio
async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test user flow with connection error."""
    flow = ConfigFlow()
    flow.hass = hass

    # Mock connection test to raise CannotConnect
    with patch.object(flow, "_test_connection") as mock_test:
        mock_test.side_effect = CannotConnect("Connection failed")

        # Test form submission
        result = await flow.async_step_user(
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
                "polling_interval": 30,
            }
        )

        assert result["type"] == FlowResultType.FORM
        assert result["errors"]["base"] == "cannot_connect"


@pytest.mark.asyncio
async def test_user_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test user flow with invalid auth error."""
    flow = ConfigFlow()
    flow.hass = hass

    # Mock connection test to raise InvalidAuth
    with patch.object(flow, "_test_connection") as mock_test:
        mock_test.side_effect = InvalidAuth("Invalid credentials")

        # Test form submission
        result = await flow.async_step_user(
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wrong_password",
                "polling_interval": 30,
            }
        )

        assert result["type"] == FlowResultType.FORM
        assert result["errors"]["base"] == "invalid_auth"


@pytest.mark.asyncio
async def test_user_flow_unknown_error(hass: HomeAssistant) -> None:
    """Test user flow with unknown error."""
    flow = ConfigFlow()
    flow.hass = hass

    # Mock connection test to raise generic exception
    with patch.object(flow, "_test_connection") as mock_test:
        mock_test.side_effect = Exception("Unknown error")

        # Test form submission
        result = await flow.async_step_user(
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
                "polling_interval": 30,
            }
        )

        assert result["type"] == FlowResultType.FORM
        assert result["errors"]["base"] == "unknown"


@pytest.mark.asyncio
async def test_user_flow_validation_errors(hass: HomeAssistant) -> None:
    """Test user flow with validation errors."""
    flow = ConfigFlow()
    flow.hass = hass

    # Test with missing required fields
    result = await flow.async_step_user(
        {
            "host": "",  # Empty host
            "username": "wattbox",
            "password": "wattbox",
            "polling_interval": 30,
        }
    )

    assert result["type"] == FlowResultType.FORM
    assert "errors" in result


@pytest.mark.asyncio
async def test_test_connection_success(hass: HomeAssistant) -> None:
    """Test successful connection test."""
    flow = ConfigFlow()
    flow.hass = hass

    with patch(
        "custom_components.wattbox.telnet_client.WattboxTelnetClient"
    ) as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        mock_instance.async_connect.return_value = None
        mock_instance.async_disconnect.return_value = None

        # Should not raise any exception
        await flow._test_connection(
            {
                "host": "192.168.1.100",
                "username": "wattbox",
                "password": "wattbox",
            }
        )


@pytest.mark.asyncio
async def test_test_connection_auth_error(hass: HomeAssistant) -> None:
    """Test connection test with auth error."""
    from custom_components.wattbox.telnet_client import WattboxAuthenticationError

    flow = ConfigFlow()
    flow.hass = hass

    with patch(
        "custom_components.wattbox.telnet_client.WattboxTelnetClient"
    ) as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        mock_instance.async_connect.side_effect = WattboxAuthenticationError(
            "Auth failed"
        )

        with pytest.raises(InvalidAuth):
            await flow._test_connection(
                {
                    "host": "192.168.1.100",
                    "username": "wattbox",
                    "password": "wrong_password",
                }
            )


@pytest.mark.asyncio
async def test_test_connection_connection_error(hass: HomeAssistant) -> None:
    """Test connection test with connection error."""
    from custom_components.wattbox.telnet_client import WattboxConnectionError

    flow = ConfigFlow()
    flow.hass = hass

    with patch(
        "custom_components.wattbox.telnet_client.WattboxTelnetClient"
    ) as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        mock_instance.async_connect.side_effect = WattboxConnectionError(
            "Connection refused"
        )

        with pytest.raises(CannotConnect):
            await flow._test_connection(
                {
                    "host": "192.168.1.100",
                    "username": "wattbox",
                    "password": "wattbox",
                }
            )


def test_cannot_connect_exception() -> None:
    """Test CannotConnect exception."""
    error = CannotConnect("Test connection error")
    assert str(error) == "Test connection error"


def test_invalid_auth_exception() -> None:
    """Test InvalidAuth exception."""
    error = InvalidAuth("Test auth error")
    assert str(error) == "Test auth error"

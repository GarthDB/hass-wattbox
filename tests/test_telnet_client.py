"""Test telnet client for Wattbox integration."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wattbox.telnet_client import (
    WattboxAuthenticationError,
    WattboxConnectionError,
    WattboxTelnetClient,
)


@pytest.fixture
def mock_reader():
    """Mock telnet reader."""
    reader = MagicMock()
    reader.readuntil = AsyncMock()
    return reader


@pytest.fixture
def mock_writer():
    """Mock telnet writer."""
    writer = MagicMock()
    writer.write = MagicMock()
    writer.drain = AsyncMock()
    writer.close = MagicMock()
    writer.wait_closed = AsyncMock()
    return writer


@pytest.fixture
def telnet_client():
    """Create a WattboxTelnetClient instance for testing."""
    return WattboxTelnetClient("192.168.1.100", "test_user", "test_password")


def test_telnet_client_init(telnet_client: WattboxTelnetClient) -> None:
    """Test WattboxTelnetClient initialization."""
    assert telnet_client._host == "192.168.1.100"
    assert telnet_client._username == "test_user"
    assert telnet_client._password == "test_password"
    assert telnet_client._reader is None
    assert telnet_client._writer is None
    assert telnet_client._connected is False


def test_telnet_client_is_connected_property(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test is_connected property."""
    assert telnet_client.is_connected is False

    telnet_client._connected = True
    assert telnet_client.is_connected is True


def test_telnet_client_device_data_property(telnet_client: WattboxTelnetClient) -> None:
    """Test device_data property."""
    data = telnet_client.device_data
    assert isinstance(data, dict)
    assert "device_info" in data
    assert "outlet_info" in data
    # Note: voltage, current, power are not in the initial device_data structure
    # They are added by the coordinator when calling async_get_power_metrics


@pytest.mark.asyncio
async def test_async_connect_success(
    telnet_client: WattboxTelnetClient,
    mock_reader,
    mock_writer,
) -> None:
    """Test successful connection."""
    with patch("telnetlib3.open_connection") as mock_open:
        mock_open.return_value = (mock_reader, mock_writer)

        # Mock successful authentication
        mock_reader.readuntil.side_effect = [
            b"Username: ",
            b"Password: ",
            b"Successfully Logged In!\n",
        ]

        await telnet_client.async_connect()

        assert telnet_client._connected is True
        assert telnet_client._reader == mock_reader
        assert telnet_client._writer == mock_writer
        mock_open.assert_called_once()


@pytest.mark.asyncio
async def test_async_connect_timeout_error(telnet_client: WattboxTelnetClient) -> None:
    """Test connection timeout error."""
    with patch("telnetlib3.open_connection") as mock_open:
        mock_open.side_effect = asyncio.TimeoutError()

        with pytest.raises(
            WattboxConnectionError, match="Connection timeout to 192.168.1.100:23"
        ):
            await telnet_client.async_connect()

        assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_connect_connection_refused(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test connection refused error."""
    with patch("telnetlib3.open_connection") as mock_open:
        mock_open.side_effect = ConnectionRefusedError()

        with pytest.raises(
            WattboxConnectionError, match="Failed to connect to 192.168.1.100:23"
        ):

            await telnet_client.async_connect()

        assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_connect_authentication_error(
    telnet_client: WattboxTelnetClient,
    mock_reader,
    mock_writer,
) -> None:
    """Test authentication error."""
    with patch("telnetlib3.open_connection") as mock_open:
        mock_open.return_value = (mock_reader, mock_writer)

        # Mock authentication failure
        mock_reader.readuntil.side_effect = asyncio.IncompleteReadError(b"", 10)

        with pytest.raises(
            WattboxConnectionError, match="Failed to connect to 192.168.1.100:23"
        ):

            await telnet_client.async_connect()

        assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_disconnect(
    telnet_client: WattboxTelnetClient, mock_writer
) -> None:
    """Test disconnection."""
    telnet_client._connected = True
    telnet_client._writer = mock_writer

    await telnet_client.async_disconnect()

    assert telnet_client._connected is False
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_called_once()


@pytest.mark.asyncio
async def test_async_disconnect_not_connected(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test disconnection when not connected."""
    # Should not raise an error
    await telnet_client.async_disconnect()
    assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_send_command_success(
    telnet_client: WattboxTelnetClient,
    mock_reader,
    mock_writer,
) -> None:
    """Test successful command sending."""
    telnet_client._connected = True
    telnet_client._reader = mock_reader
    telnet_client._writer = mock_writer

    mock_reader.read = AsyncMock(return_value=b"?Firmware=1.0.0\n")

    response = await telnet_client.async_send_command("?Firmware")

    assert response == "?Firmware=1.0.0"
    mock_writer.write.assert_called_once_with("?Firmware\r\n")
    mock_writer.drain.assert_called_once()
    # read is called twice: once for buffer flush, once for actual response
    assert mock_reader.read.call_count == 2
    mock_reader.read.assert_any_call(1024)


@pytest.mark.asyncio
async def test_async_send_command_not_connected(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test command sending when not connected."""
    # Ensure client is not connected
    telnet_client._connected = False

    with pytest.raises(WattboxConnectionError):
        await telnet_client.async_send_command("?Firmware")


@pytest.mark.asyncio
async def test_async_get_device_info(telnet_client: WattboxTelnetClient) -> None:
    """Test getting device info."""
    with (
        patch.object(telnet_client, "async_connect"),
        patch.object(telnet_client, "async_send_command") as mock_send,
    ):
        mock_send.side_effect = [
            "?Firmware=1.0.0",
            "?Model=WB-800VPS",
            "?ServiceTag=TEST123",
            "?Hostname=test-box",
            "?AutoReboot=1",
        ]

        info = await telnet_client.async_get_device_info()

        assert info["hardware_version"] == "1.0.0"
        assert info["model"] == "WB-800VPS"
        assert info["serial_number"] == "TEST123"
        assert info["hostname"] == "test-box"
        assert info["auto_reboot"] == "1"


@pytest.mark.asyncio
async def test_async_get_outlet_status(telnet_client: WattboxTelnetClient) -> None:
    """Test getting outlet status."""
    with (
        patch.object(telnet_client, "async_connect"),
        patch.object(telnet_client, "async_send_command") as mock_send,
    ):
        # Mock responses for the new command delay behavior:
        # 1. Get outlet count: ?OutletCount -> empty, ?Firmware -> ?OutletCount=12
        # 2. Get outlet status: ?Firmware -> empty, ?OutletStatus -> empty,
        #    ?Firmware -> ?OutletStatus=...
        # 3. Get outlet names: ?Firmware -> empty, ?OutletName -> empty,
        #    ?Firmware -> ?OutletName=...
        mock_send.side_effect = [
            # Outlet count sequence
            "",  # ?OutletCount returns empty
            "?OutletCount=12",  # ?Firmware returns outlet count
            # Outlet status sequence
            "",  # ?Firmware returns empty
            "",  # ?OutletStatus returns empty
            "?OutletStatus=1,0,1,0,1,0,1,0,1,0,1,0",  # ?Firmware returns outlet status
            # Outlet names sequence
            "",  # ?Firmware returns empty
            "",  # ?OutletName returns empty
            "?OutletName={Outlet 1},{Outlet 2},{Outlet 3},{Outlet 4},"
            "{Outlet 5},{Outlet 6},{Outlet 7},{Outlet 8},{Outlet 9},"
            "{Outlet 10},{Outlet 11},{Outlet 12}",  # ?Firmware returns outlet names
        ]

        outlets = await telnet_client.async_get_outlet_status()

        assert len(outlets) == 12
        assert outlets[0]["state"] == 1
        assert outlets[0]["name"] == "Outlet 1"
        assert outlets[1]["state"] == 0
        assert outlets[1]["name"] == "Outlet 2"


@pytest.mark.asyncio
async def test_async_set_outlet_state(telnet_client: WattboxTelnetClient) -> None:
    """Test setting outlet state."""
    with (
        patch.object(telnet_client, "async_connect"),
        patch.object(telnet_client, "async_send_command") as mock_send,
    ):
        # Initialize outlet info
        telnet_client._device_data["outlet_info"] = [
            {"state": 0, "name": "Outlet 1"},
            {"state": 0, "name": "Outlet 2"},
        ]

        await telnet_client.async_set_outlet_state(1, True)

        mock_send.assert_called_once_with("!OutletSet=1,ON")
        # Check that internal state was updated
        assert telnet_client._device_data["outlet_info"][0]["state"] == 1


@pytest.mark.asyncio
async def test_async_get_power_metrics(telnet_client: WattboxTelnetClient) -> None:
    """Test getting power metrics (placeholder implementation)."""
    metrics = await telnet_client.async_get_power_metrics()

    # Should return placeholder values
    assert metrics["voltage"] is None
    assert metrics["current"] is None
    assert metrics["power"] is None


# Note: _ensure_connected method doesn't exist in the current implementation


def test_connection_error_exception() -> None:
    """Test WattboxConnectionError exception."""
    error = WattboxConnectionError("Test connection error")
    assert str(error) == "Test connection error"


def test_authentication_error_exception() -> None:
    """Test WattboxAuthenticationError exception."""
    error = WattboxAuthenticationError("Test auth error")
    assert str(error) == "Test auth error"


# Status monitoring tests
@pytest.mark.asyncio
async def test_async_get_status_info(telnet_client: WattboxTelnetClient) -> None:
    """Test async_get_status_info method."""
    with (
        patch.object(
            telnet_client, "async_connect", new_callable=AsyncMock
        ) as mock_connect,
        patch.object(
            telnet_client, "_get_power_status", new_callable=AsyncMock
        ) as mock_power,
        patch.object(
            telnet_client, "_get_ups_connection", new_callable=AsyncMock
        ) as mock_ups_conn,
        patch.object(
            telnet_client, "_get_ups_status", new_callable=AsyncMock
        ) as mock_ups_status,
    ):

        result = await telnet_client.async_get_status_info()

        mock_connect.assert_called_once()
        mock_power.assert_called_once()
        mock_ups_conn.assert_called_once()
        mock_ups_status.assert_called_once()

        assert isinstance(result, dict)
        assert "power_status" in result
        assert "ups_status" in result
        assert "ups_connected" in result


@pytest.mark.asyncio
async def test_get_power_status_success(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_power_status method with successful response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "?PowerStatus=60.00,600.00,110.00,1"

        await telnet_client._get_power_status()

        mock_send.assert_called_once_with("?PowerStatus")

        power_status = telnet_client._device_data["status_info"]["power_status"]
        assert power_status["current"] == 60.0
        assert power_status["power"] == 600.0
        assert power_status["voltage"] == 110.0
        assert power_status["safe_voltage"] == 1


@pytest.mark.asyncio
async def test_get_power_status_failure(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_power_status method with failed response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.side_effect = Exception("Connection failed")

        await telnet_client._get_power_status()

        # Should not raise exception, just log warning
        power_status = telnet_client._device_data["status_info"]["power_status"]
        assert power_status["current"] is None
        assert power_status["power"] is None
        assert power_status["voltage"] is None
        assert power_status["safe_voltage"] is None


@pytest.mark.asyncio
async def test_get_ups_connection_success(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_ups_connection method with successful response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "?UPSConnection=1"

        await telnet_client._get_ups_connection()

        mock_send.assert_called_once_with("?UPSConnection")

        assert telnet_client._device_data["status_info"]["ups_connected"] is True


@pytest.mark.asyncio
async def test_get_ups_connection_disconnected(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test _get_ups_connection method with disconnected response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "?UPSConnection=0"

        await telnet_client._get_ups_connection()

        assert telnet_client._device_data["status_info"]["ups_connected"] is False


@pytest.mark.asyncio
async def test_get_ups_connection_failure(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_ups_connection method with failed response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.side_effect = Exception("Connection failed")

        await telnet_client._get_ups_connection()

        # Should not raise exception, just log warning
        assert telnet_client._device_data["status_info"]["ups_connected"] is None


@pytest.mark.asyncio
async def test_get_ups_status_success(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_ups_status method with successful response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "?UPSStatus=50,0,Good,False,25,True,False"

        await telnet_client._get_ups_status()

        mock_send.assert_called_once_with("?UPSStatus")

        ups_status = telnet_client._device_data["status_info"]["ups_status"]
        assert ups_status["battery_charge"] == 50
        assert ups_status["battery_load"] == 0
        assert ups_status["battery_health"] == "Good"
        assert ups_status["power_lost"] is False
        assert ups_status["battery_runtime"] == 25
        assert ups_status["alarm_enabled"] is True
        assert ups_status["alarm_muted"] is False


@pytest.mark.asyncio
async def test_get_ups_status_power_lost(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_ups_status method with power lost response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "?UPSStatus=30,80,Bad,True,10,True,False"

        await telnet_client._get_ups_status()

        ups_status = telnet_client._device_data["status_info"]["ups_status"]
        assert ups_status["battery_charge"] == 30
        assert ups_status["battery_load"] == 80
        assert ups_status["battery_health"] == "Bad"
        assert ups_status["power_lost"] is True
        assert ups_status["battery_runtime"] == 10
        assert ups_status["alarm_enabled"] is True
        assert ups_status["alarm_muted"] is False


@pytest.mark.asyncio
async def test_get_ups_status_failure(telnet_client: WattboxTelnetClient) -> None:
    """Test _get_ups_status method with failed response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        mock_send.side_effect = Exception("Connection failed")

        await telnet_client._get_ups_status()

        # Should not raise exception, just log warning
        ups_status = telnet_client._device_data["status_info"]["ups_status"]
        assert ups_status["battery_charge"] is None
        assert ups_status["battery_load"] is None
        assert ups_status["battery_health"] is None
        assert ups_status["power_lost"] is None
        assert ups_status["battery_runtime"] is None
        assert ups_status["alarm_enabled"] is None
        assert ups_status["alarm_muted"] is None


@pytest.mark.asyncio
async def test_get_outlet_states_invalid_response(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test _get_outlet_states method with invalid response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        # Mock the three calls in sequence
        mock_send.side_effect = ["", "", "InvalidResponse"]

        await telnet_client._get_outlet_states()

        # Should not raise exception, just log warning
        assert mock_send.call_count == 3


@pytest.mark.asyncio
async def test_get_outlet_names_invalid_response(
    telnet_client: WattboxTelnetClient,
) -> None:
    """Test _get_outlet_names method with invalid response."""
    with patch.object(
        telnet_client, "async_send_command", new_callable=AsyncMock
    ) as mock_send:
        # Mock the three calls in sequence
        mock_send.side_effect = ["", "", "InvalidResponse"]

        await telnet_client._get_outlet_names()

        # Should not raise exception, just log warning
        assert mock_send.call_count == 3


def test_device_data_structure(telnet_client: WattboxTelnetClient) -> None:
    """Test that device_data has the correct structure for status monitoring."""
    device_data = telnet_client.device_data

    assert "status_info" in device_data
    assert "power_status" in device_data["status_info"]
    assert "ups_status" in device_data["status_info"]
    assert "ups_connected" in device_data["status_info"]

    # Check power_status structure
    power_status = device_data["status_info"]["power_status"]
    assert "current" in power_status
    assert "power" in power_status
    assert "voltage" in power_status
    assert "safe_voltage" in power_status

    # Check ups_status structure
    ups_status = device_data["status_info"]["ups_status"]
    assert "battery_charge" in ups_status
    assert "battery_load" in ups_status
    assert "battery_health" in ups_status
    assert "power_lost" in ups_status
    assert "battery_runtime" in ups_status
    assert "alarm_enabled" in ups_status
    assert "alarm_muted" in ups_status

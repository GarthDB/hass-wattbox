"""Test telnet client for Wattbox integration."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import telnetlib3

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


def test_telnet_client_is_connected_property(telnet_client: WattboxTelnetClient) -> None:
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
        
        with pytest.raises(WattboxConnectionError, match="Connection timeout to 192.168.1.100:23"):
            await telnet_client.async_connect()
        
        assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_connect_connection_refused(telnet_client: WattboxTelnetClient) -> None:
    """Test connection refused error."""
    with patch("telnetlib3.open_connection") as mock_open:
        mock_open.side_effect = ConnectionRefusedError()
        
        with pytest.raises(WattboxConnectionError, match="Failed to connect to 192.168.1.100:23"):
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
        
        with pytest.raises(WattboxConnectionError, match="Failed to connect to 192.168.1.100:23"):
            await telnet_client.async_connect()
        
        assert telnet_client._connected is False


@pytest.mark.asyncio
async def test_async_disconnect(telnet_client: WattboxTelnetClient, mock_writer) -> None:
    """Test disconnection."""
    telnet_client._connected = True
    telnet_client._writer = mock_writer
    
    await telnet_client.async_disconnect()
    
    assert telnet_client._connected is False
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_called_once()


@pytest.mark.asyncio
async def test_async_disconnect_not_connected(telnet_client: WattboxTelnetClient) -> None:
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
    
    mock_reader.readuntil.return_value = b"?Firmware=1.0.0\n"
    
    response = await telnet_client.async_send_command("?Firmware")
    
    assert response == "?Firmware=1.0.0"
    mock_writer.write.assert_called_once_with("?Firmware\r\n")
    mock_writer.drain.assert_called_once()
    mock_reader.readuntil.assert_called_once_with(b"\n")


@pytest.mark.asyncio
async def test_async_send_command_not_connected(telnet_client: WattboxTelnetClient) -> None:
    """Test command sending when not connected."""
    # Ensure client is not connected
    telnet_client._connected = False
    
    with pytest.raises(WattboxConnectionError, match="Not connected"):
        await telnet_client.async_send_command("?Firmware")


@pytest.mark.asyncio
async def test_async_get_device_info(telnet_client: WattboxTelnetClient) -> None:
    """Test getting device info."""
    with patch.object(telnet_client, "async_connect") as mock_connect:
        with patch.object(telnet_client, "async_send_command") as mock_send:
            mock_send.side_effect = [
                "?Firmware=1.0.0", 
                "?Model=WB-800VPS", 
                "?ServiceTag=TEST123", 
                "?Hostname=test-box", 
                "?AutoReboot=1"
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
    with patch.object(telnet_client, "async_connect") as mock_connect:
        with patch.object(telnet_client, "async_send_command") as mock_send:
            # Mock responses for outlet status and names
            mock_send.side_effect = [
                "?Firmware=1.0.0",  # Dummy command response
                "?OutletStatus=1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0",  # Outlet states
                "?Firmware=1.0.0",  # Dummy command response
                "?OutletName={Outlet 1},{Outlet 2},{Outlet 3},{Outlet 4},{Outlet 5},{Outlet 6},{Outlet 7},{Outlet 8},{Outlet 9},{Outlet 10},{Outlet 11},{Outlet 12},{Outlet 13},{Outlet 14},{Outlet 15},{Outlet 16},{Outlet 17},{Outlet 18}",  # Outlet names
            ]
            
            outlets = await telnet_client.async_get_outlet_status(18)
            
            assert len(outlets) == 18
            assert outlets[0]["state"] == 1
            assert outlets[0]["name"] == "Outlet 1"
            assert outlets[1]["state"] == 0
            assert outlets[1]["name"] == "Outlet 2"


@pytest.mark.asyncio
async def test_async_set_outlet_state(telnet_client: WattboxTelnetClient) -> None:
    """Test setting outlet state."""
    with patch.object(telnet_client, "async_connect") as mock_connect:
        with patch.object(telnet_client, "async_send_command") as mock_send:
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

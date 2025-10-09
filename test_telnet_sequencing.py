#!/usr/bin/env python3
"""Test telnet command sequencing to verify proper response handling."""

import asyncio
import os
import telnetlib3
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_telnet_sequencing():
    """Test telnet command sequencing with proper buffer flushing."""
    # Load environment variables
    host = os.getenv("WATTBOX_TEST_HOST", "192.168.1.34")
    username = os.getenv("WATTBOX_TEST_USERNAME", "garthdb")
    password = os.getenv("WATTBOX_TEST_PASSWORD", "FE@7bc3YHE86q!cb")
    port = int(os.getenv("WATTBOX_TEST_PORT", "23"))
    timeout = int(os.getenv("WATTBOX_TEST_TIMEOUT", "10"))

    print(f"Testing telnet sequencing with Wattbox at {host}:{port}")
    print("=" * 60)

    try:
        # Connect to device
        reader, writer = await telnetlib3.open_connection(host, port, timeout=timeout)
        print("✅ Connected successfully")

        # Wait for username prompt
        data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        print(f"Initial data: {repr(data)}")

        if "Username:" in data:
            # Send username
            writer.write(username + "\r\n")
            await writer.drain()
            print(f"Sent username: {username}")

            # Wait for password prompt
            data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            print(f"Password prompt: {repr(data)}")

            if "Password:" in data:
                # Send password
                writer.write(password + "\r\n")
                await writer.drain()
                print(f"Sent password")

                # Wait for login success
                data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
                print(f"Login response: {repr(data)}")

                if "Successfully Logged In!" in data:
                    print("✅ Login successful")

                    # Test commands in sequence with proper flushing
                    commands = [
                        "?Firmware",
                        "?Model",
                        "?ServiceTag",
                        "?Hostname"
                    ]

                    responses = {}

                    for i, command in enumerate(commands):
                        print(f"\n--- Command {i+1}: {command} ---")

                        # Flush buffer before sending command
                        print("  Flushing buffer...")
                        try:
                            while True:
                                flush_data = await asyncio.wait_for(reader.read(1024), timeout=0.1)
                                if not flush_data:
                                    break
                                print(f"  Flushed: {repr(flush_data)}")
                        except asyncio.TimeoutError:
                            pass

                        # Send command
                        writer.write(command + "\r\n")
                        await writer.drain()
                        print(f"  Sent: {command}")

                        # Wait a bit for processing
                        await asyncio.sleep(0.2)

                        # Read response
                        response = await asyncio.wait_for(reader.read(1024), timeout=timeout)
                        print(f"  Response: {repr(response)}")

                        if "=" in response:
                            data = response.split("=")[1].strip()
                            print(f"  Parsed data: {repr(data)}")
                            responses[command] = data
                        else:
                            print("  No data found in response")
                            responses[command] = None

                    print("\n" + "=" * 60)
                    print("FINAL RESULTS:")
                    print("=" * 60)

                    for command, data in responses.items():
                        print(f"{command:12} → {data}")

                    # Check if data is in correct fields now
                    print("\nField Assignment Check:")
                    firmware = responses.get("?Firmware", "")
                    model = responses.get("?Model", "")
                    serial = responses.get("?ServiceTag", "")
                    hostname = responses.get("?Hostname", "")

                    print(f"Firmware: {firmware} {'✅' if '.' in firmware and not firmware.startswith('WB-') else '❌'}")
                    print(f"Model:    {model} {'✅' if model.startswith('WB-') else '❌'}")
                    print(f"Serial:   {serial} {'✅' if serial.startswith('ST') else '❌'}")
                    print(f"Hostname: {hostname} {'✅' if not hostname.startswith('ST') and not hostname.startswith('WB-') else '❌'}")

                else:
                    print("❌ Login failed")
            else:
                print("❌ No password prompt")
        else:
            print("❌ No username prompt")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_telnet_sequencing())

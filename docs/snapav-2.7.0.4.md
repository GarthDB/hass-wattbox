![](data:image/jpeg;base64...)

# Overview

**SnapAV WattBox Integration Protocol Document**

Integration Protocol v3.0 rev20230330

This integration protocol details how a third-party system can be used to control a SnapAV WattBox. With the WattBox online, the integration protocol will be listening for connections on port 23 or SSH on port 22 at the controller's IP address. To get started, netcat or similar software can be used to initiate a connection and test any of the following protocol commands below.

# Important information:

The SSH feature was added with firmware 1.3.0.4. To connect with SSH you will need at least firmware version 1.3.0.4.

Only 10 simultaneous connections can be made at a time.

# Authentication

The protocol requires authentication before proceeding with commands. Once connected, a login prompt will be received, and the third-party system must provide a valid username and password. If correct, login will be successful and other commands can be issued. If incorrect, the third-party system will be prompted for login again.

# Important information:

If using SSH, you will need to set a new password for the WattBox. There is a 13-character limit on passwords used for SSH user credentials.

# Specification

THIRD-PARTY SYSTEM < > SnapAV WattBox

i.e. Wattbox IP: 192.168. 0.20 Port: 23

# Integration

|  |
| --- |
| **Message Structure** |
| Command and response messages are standard ASCII text. |
| ? – Request message |
| ! – Control message |
| # - Error message |
| ~ - Unsolicited message |
| \n – End of command message, ASCII hex: 0x0A dec: 10 |

**Protocol**

|  |  |
| --- | --- |
| **Protocol Command** | **Description/Response** |
| ?Help\n | Lists all possible commands. |
| ?Firmware\n | Request Firmware Version. |

|  |  |
| --- | --- |
|  | Response: ?Firmware=1.0.0.0\n WebServerSet |
| ?Hostname\n | Request Hostname.  Response: ?Hostname=WattBox\n |
| ?ServiceTag\n | Request the unit’s Service Tag.  Response: ?ServiceTag=ST191500681E8422\n |
| ?Model\n | Request Model Number.  Response: ?Model=WB-800-IPVM-6\n |
| ?OutletCount\n | Request Outlet Count.  Response: ?OutletCount=16\n |
| ?OutletStatus\n | Request Outlet States.  Response: ?OutletStatus=0,0,0,0,0,0,0,0,0,0,0,0\n  Where the array index plus one is the outlet number and the value at the index indicates state. 0 for off, 1 for on. |
| ?OutletPowerStatus=OUTLET\n  Where OUTLET is the Outlet number. | Request Outlet Power Status for a specific outlet.  *NOTE: Not supported on WB150/250.*  Response:  ?OutletPowerStatus=1,1.01,0.02,116.50\n  Where 1 is the outlet index you requested, 1.01 is the power in watts, 0.02 is the current in amps, and 116.50 is the voltage in volts. |
| ?PowerStatus\n | Request Power Status for the system.  *NOTE: Not supported on WB150/250.*  Response:  ?PowerStatus=60.00,600.00,110.00,1\n  Where 60.00 is the current in amps, 600.00 is the power in watts, 110.00 is the voltage in volts, and 1 is the safe voltage status. |
| !RebootSys\n | Request to reboot the device immediately using Linux system call. The client will lose the connection to the device until the device is back online.  Response: OK\n |
| ?AutoReboot\n | Request Auto Reboot Status for the system.  Response:  ?AutoReboot=1\n  Enabled = 1  Disabled = 0 |
| ?OutletName\n | Request Outlet Names for all outlets. The names will be sent with brackets around every NAME and comma delimited between each set.  Response:  ?OutletName={Outlet 1},{Outlet 2},{Outlet 3},{Outlet 4},{Outlet 5},{Outlet 6},{Outlet 7},{Outlet 8},{Outlet 9},{Outlet 10},{Outlet 11},{Outlet 12}\n |
| !OutletNameSet=OUTLET, NAME\n  Where OUTLET is the outlet number and NAME is the new  name. | Request to change the name of a specific outlet. Names can have a length up to 31 characters. Spaces are not allowed.  Response:  OK\n |
| !OutletNameSetAll={NAME},{NA ME},{NAME},{NAME},{NAME},{NA  ME},{NAME},{NAME},{NAME},{NA ME},{NAME},{NAME}\n  Where NAME is the new name. | Request to change the names for every outlet. Order matters and starts with Outlet 1. The brackets are required around every NAME with commas in- between each set. Names can have a length up to 31 characters.  Response:  OK\n |
| ?UPSStatus\n | Request UPS Status if there is a UPS attached.  Response:  ?UPSStatus=50,0,Good,False,25,True,False\n  Where 50 is the battery charge percentage, 0 is the battery load as a percentage, Good indicates battery health, False indicates power lost, 25 indicates battery runtime in minutes, True indicates alarm enabled, False indicates alarm muted.  Battery Charge: 0-100%  Battery Load: 0-100% Battery Health: Good/Bad Power Lost: True/False  Battery Runtime: Number in Minutes Alarm Enabled: True/False  Alarm Muted: True/False |
| ?UPSConnection\n | Request UPS Connection to find out if a UPS has been attached to the wattbox.  Response:  ?UPSConnection=0\n  Disconnected = 0  Connected = 1 |
| !OutletSet=OUTLET,ACTION,DELA  Y\n  Where OUTLET is the outlet number and ACTION is ON/OFF/TOGGLE/RESET. If action RESET, an optional third | Request to set a specific outlet to a new state. RESET does adhere to power on delay but one may override that value by passing a third optional parameter for DELAY. This delay must be in seconds and ranges from 1 – 600 seconds. To reset all outlets, set OUTLET to 0 and action to RESET. If this command is successful and the outlet is enabled, it will trigger an unsolicited ‘~OutletStatus’ message for each outlet state change. |
| parameter is provided for delaying the reset by x number of  seconds. | Response:  OK\n |
| !OutletPowerOnDelaySet=OUTLE T,DELAY\n  Where OUTLET is the outlet number and DELAY is the time in seconds. | Request to set the power on delay for a specific outlet. The power on delay is in seconds and accepts values between 1 and 600.  Response:  OK\n |
| !OutletModeSet=OUTLET,MODE\ n  Where OUTLET is the outlet number and MODE is the new mode represented as a number. | Request to set a specific outlet to a new operating mode. An operating mode will enable/disable control of a specific outlet. Reference the below table to determine the mode and send the corresponding number value. Any number sent outside of this range will be rejected.  Enabled = 0  Disabled = 1 Reset Only = 2  Response:  OK\n |
| !OutletRebootSet=OP, OP, OP, OP, OP, OP, OP, OP, OP, OP, OP,  OP\n  Where OP is the reboot operation taken during a host reboot. | Request to change the reboot operation of an outlet when a host goes offline and triggers a reboot. Reference the below table to determine the mode and send the corresponding number value. Any OP other than 0 and 1 will generate error message.  (Any selected hosts time-out) Or = 0 (All selected hosts time out) And = 1  Response:  OK\n |
| !AutoReboot=STATE\n  Where STATE is 1 for enabled or 0 for disabled | Request to set auto reboot to a new state. Any STATE other than 0 and 1 will generate error message.  Response:  OK\n |
| !AutoRebootTimeoutSet=TIMEO UT,TIMEOUT,PING\_DELAY,REBOO T\_ATTEMPTS\n  Where TIMEOUT is a number value in seconds, COUNT is a number value, PING\_DELAY is a number value and REBOOT ATTEMPTS is a number value. | Request to change the timeout settings for the device. Reference the below table for valid range values.  Timeout [1-60] – Select a value between 1 and 60 seconds. This is the amount of time the device will wait before timing out a host.  Count [1-10] – Select a value between 1 and 10. This is the number of consecutive time-outs that must occur before triggering auto-reboot.  Ping Delay [1-30] - Select a value between 1 and 30 minutes. This is the amount of time the device waits to retest the connection after auto-rebooting. |
|  | Reboot attempts [0 = unlimited, 1-10] - Select a value between 0 and 10. This is the number of times the device will auto-reboot. 0 represents infinite reboots.  Response:  OK\n |
| !FirmwareUpdate=URL\n  Where URL is the full path to the upgrade file. | Update firmware for the device. This API will respond OK right before the system shuts down. The client will lose the connection to the device until the device is back online.  Response:  OK\n |
| !Reboot\n | Request to reboot the device immediately. The client will lose the connection to the device until the device is back online.  Response:  OK\n |
| !AccountSet=USER,PASS\n  Where USER is the username and PASS is the password. | Request to change the login credentials for a given user and given password. If successful, the client will lose the connection and require a reconnect to login again. Invalid usernames or passwords will be rejected.  Response:  OK\n |
| !NetworkSet=HOSTNAME,IP,SUB NET,GATEWAY,DNS1,DNS2\n  Where HOST is the hostname, IP is the static address, SUBNET is subnet, GATEWAY is gateway, DNS1 is primary dns server, DNS2 is secondary dns server. | Request to change the network settings for the device. HOSTNAME only allows characters A-z,0-9, and ‘-’  If setting DHCP, do not send IP,SUBNET,GATEWAY,DNS1,DNS2.  If setting STATIC, IP,SUBNET,GATEWAY,DNS1 are required. DNS2 is optional and will be auto filled to 8.8.8.8 if nothing was entered.  If the settings are valid, the changes will be made and the device will reboot. The client will lose the connection to the device until the device is back online. Please note the device may come back at a different IP address depending on the settings sent.  Response:  OK\n |
| ?NetworkGet\n  *Minimum FW v2.3.0.8* | Request the network settings for the device  Response:  ?NetworkGet=  <DHCP>,<STATIC\_DNS>,<HOSTNAME>,<IP>,<SUBNET>,<GATEWAY>,<DNS1>,<D  NS2>\n  DHCP: 0 or 1, 1 – enabled, 0 - disabled  STATIC\_DNS: 0 or 1, 1 – enabled, 0 - disabled |
|  | HOSTNAME: Up to 64 characters IP: x.x.x.x  SUBNET: x.x.x.x GATEWAY: x.x.x.x  DNS1: x.x.x.x  DNS2: x.x.x.x |
| !ScheduleAdd={NAME},{OUTLET, OUTLET,OUTLET},{ACTION},{FREQ  },{DAY,DAY,DAY | DATE},{TIME}\n  Where NAME is the schedule name, OUTLET is an array of outlet numbers, ACTION is the action performed, FREQUENCY is once or recurring, DAYS or DATE are the days for recurring or date for once, TIME is the time. | Request to add a schedule to the scheduled events for the device. Brackets are required around every value with a comma delimiter between each set.  Parameter 2 is an array of outlets to indicate which outlets the ACTION will be performed on once the schedule is triggered. Reference the below table to determine the correct field and send the corresponding values. Values outside of any of these ranges will be rejected.  Outlet = {1,2,3} Would tie outlets 1,2,3 to this schedule. Action   * Off = 0 * On = 1 * Reset = 2   Frequency   * Once = 0 * Recurring = 1   If Recurring  Days [s,m,t,w,t,f,s] – This is an array where the index indicates the day of the week and if the value at the index is a 0, the day is not included, if the value at the index is 1, the day is included. The following example will recur every Monday, Wednesday, and Friday. {0,1,0,1,0,1,0}  If Once  Date [yyyy/mm/dd] – {2018/09/28}  Time [hh:mm] – 24-Hour based so 1:30pm would be represented as 13:30. Response:  OK\n |
| !HostAdd=NAME,IP,{OUTLET,OUT  LET}\n  Where NAME is the host name, IP is the Website or IP address to be tested, and OUTLET is an array of  outlet numbers. | Request to add a host to the list of hosts to be monitored by the device. Brackets are required around the outlets array. This array indicates which outlets should be tied to the host being added. |
| !SetTelnet=MODE\n  Where mode is 0 for disabled, 1 for enabled. | Request to enable or disable the telnet service. A reboot is required for settings to take effect. All MODE values other than 0 or 1 will generate error message.  Response: |
|  | OK\n |
| !WebServerSet=MODE\n  Where mode is 0 for disabled, 1 for enabled | Request to enable or disable the web server. A reboot is required for settings to take effect. All MODE values other than 0 or 1 will generate error message.  Response:  OK\n  Requires WattBox firmware 2.0 |
| !SetSDDP=MODE\n  Where mode is 0 for disabled, 1 for enabled | Request to enable or disable SDDP broadcasting. All MODE values other than 0 or 1 will generate error message.  Response:  OK\n  Requires WattBox firmware 2.0 |
| !Exit | Close the session gracefully. |
| ~OutletStatus=STATE, STATE, STATE, STATE, STATE, STATE, STATE, STATE, STATE, STATE  Where STATE can be 0 for OFF or 1 for ON. | Unsolicited outlet status message. This message is generated anytime an outlet changes its state. Where the array index plus one is the outlet number and the value at the index indicates STATE. |
| #Error\n | Sent whenever an invalid command was received, or an internal device error has  occurred. Please see the device log page for further detailed error messages. |
| ?FaceplatePresent  *Minimum FW v2.3.0.2* | Responds 0 or 1 to indicate presence |
| ?FaceplatePort  *Minimum FW v2.3.0.2* | Responds 0 if no faceplate, 1, 2 or 3 to indicate a faceplate port. |
| ?FaceplateLedLevel  *Minimum FW v2.3.0.2* | Responds with a level between 0 and 65535. 0 is dimmest. |
| !FaceplateLedLevelSet=LEVEL  *Minimum FW v2.3.0.2* | Level should be an integer between 0 and 65535. 0 is dimmest. |
| ?FaceplateUUID  *Minimum FW v2.3.0.2* | Responds with the UUID string |
| ?UPSVoltageRange  *Minimum FW v2.3.0.6* | Responds with N, W, G or U N – Normal |
|  | W – Wide  G – Generator  U – Unknown (ask again, UPS doesn’t always respond) |
| !UPSVoltageRange=RANGE  *Minimum FW v2.3.0.6* | Set RANGE to one of: N – Normal  W – Wide  G – Generator |
| ?AdapterSensorData  *Minimum FW v2.6.2.0* | Fetches Sensor Data for all WB-ACC-ADAPTER-800's. Each entry is separated by a semicolon. If no adapters are connected, then 'None' is returned.  Example Response:  ?AdapterSensorData= <a1\_tag>,<a1\_port>,<s1\_conn>,<s1\_unit>,<s1\_data>,  <s2\_conn>,<s2\_unit>,<s2\_data>  <a\*\_tag> - Service Tag of the connected WB-ACC-ADAPTER-800  <a\*\_port> - Port the device is connected to. 0 – Directly connected  <s\*\_conn> - 'True' means sensor probe is connected, 'False' otherwise.  <s\*\_unit> - 0 = Sensor units are tenths of degrees Celsius.  <s\*\_data> - Sensor data value in <s\*\_units>. Data is invalid if <s\*\_conn> is 'False'. |
| ?AdapterServiceTags | Fetches all connected WB-ACC-ADAPTER-800 service tags. If no adapters are connected, then 'None' is returned.  Example Response:  ?AdapterServiceTags=STXXXXXXXXXXXXXXXX |
| ?AdapterConfig=<service\_tag> | Fetches the config for a specific WB-ACC-ADAPTER-800.  Example Response:  ?AdapterConfig=<button\_type>,<button\_polarity\_when\_latching>,<dc\_out\_pin\_ mode>  <button\_type> configures what kind of button or signal is connected to the ‘Trigger’ Pin on the phoenix connector. 0-Momentary Button, 1-Latching Button |
|  | !<button\_polarity\_when\_latching>  <button\_polarity\_when\_latching> determines which part of the signal is active. 0-ActiveLow, 1-ActiveHigh. Only applies when <button\_type> is latching.  <dc\_out\_pin\_mode> determines the behavior of the ‘DC OUT’ pin on the phoenix connector. 0-Disabled, 1-Enabled, 2-ToggleDuringAction |
| !AdapterConfig=<service\_tag>,<b utton\_type>,<button\_polarity\_w hen\_latching>,<dc\_out\_pin\_mod e> | Sets the config for a specific WB-ACC-ADAPTER-800. Example Response: OK |

Example:

![](data:image/png;base64...)
KNOWLEDGE_BASE = """# WINDOWS OPERATING SYSTEM ISSUES

## Windows Update Problems

Problem: Windows Update stuck at 0% or specific percentage
Solution:
1. Press Windows + R and type 'services.msc', press Enter
2. Locate 'Windows Update' service and restart it
3. Clear Windows Update cache: Stop service, delete C:\\Windows\\SoftwareDistribution folder contents
4. Run Windows Update Troubleshooter from Settings > Update & Security > Troubleshoot
5. Run command: sfc /scannow in Command Prompt as Administrator
6. Run command: DISM /Online /Cleanup-Image /RestoreHealth
7. If still stuck, try manual update from Microsoft Update Catalog

Problem: Error code 0x80070422 - Windows Update cannot check for updates
Solution:
1. Open Services by pressing Windows + R and typing 'services.msc'
2. Find 'Windows Update' service in the list
3. Double-click to open properties
4. Set Startup type to 'Automatic'
5. Click 'Start' button to start the service
6. Also check 'Background Intelligent Transfer Service' and ensure it's running
7. Restart computer and try updating again

Problem: Error code 0x80240034 - Update files may be damaged
Solution:
1. Run Windows Update Troubleshooter
2. Delete Software Distribution folder contents
3. Reset Windows Update components using Command Prompt
4. Re-register Windows Update DLL files
5. Download updates manually from Microsoft Update Catalog

Problem: Windows Update taking too long to install
Solution:
1. Ensure stable internet connection
2. Free up disk space (at least 20GB recommended)
3. Disable third-party antivirus temporarily
4. Install updates one at a time if possible
5. Perform clean boot and try updating

## Blue Screen of Death (BSOD) Errors

Problem: STOP CODE: DRIVER_IRQL_NOT_LESS_OR_EQUAL
Solution:
1. Boot into Safe Mode by pressing F8 during startup
2. Update all device drivers, especially network and graphics drivers
3. Uninstall recently installed software that might be causing conflicts
4. Run memory diagnostic tool: Windows + R, type mdsched.exe
5. Check for disk errors: Open Command Prompt as admin and run chkdsk /f /r
6. Disable fast startup: Control Panel > Power Options > Choose what power buttons do
7. If using third-party antivirus, try uninstalling temporarily

Problem: STOP CODE: SYSTEM_SERVICE_EXCEPTION
Solution:
1. Update Windows to latest version
2. Update all device drivers from manufacturer websites
3. Run System File Checker: sfc /scannow
4. Check for corrupted system files using DISM commands
5. Uninstall problematic third-party software
6. Check RAM using Windows Memory Diagnostic
7. Scan for malware using Windows Defender

Problem: STOP CODE: PAGE_FAULT_IN_NONPAGED_AREA
Solution:
1. Check RAM modules - reseat or replace if faulty
2. Run Windows Memory Diagnostic
3. Update all device drivers
4. Check disk for errors using chkdsk
5. Disable hardware acceleration in applications
6. Update BIOS/UEFI firmware from manufacturer website
7. Test with minimal hardware configuration

Problem: STOP CODE: CRITICAL_PROCESS_DIED
Solution:
1. Run System File Checker: sfc /scannow
2. Run DISM repair commands
3. Update Windows and all drivers
4. Check for disk errors
5. Perform clean boot to identify conflicting software
6. Consider system restore to previous working state
7. As last resort, perform in-place upgrade or clean install

## System Performance Issues

Problem: Computer running very slow
Solution:
1. Check Task Manager (Ctrl+Shift+Esc) for resource-heavy processes
2. Disable startup programs: Task Manager > Startup tab, disable unnecessary items
3. Run Disk Cleanup utility: Search for 'Disk Cleanup' in Start menu
4. Defragment hard drive (not for SSD): Search 'Defragment and Optimize Drives'
5. Check for malware using Windows Defender full scan
6. Increase virtual memory: System Properties > Advanced > Performance Settings
7. Upgrade RAM if usage consistently above 80%
8. Check disk health using CrystalDiskInfo
9. Disable visual effects: System Properties > Advanced > Performance Settings > Adjust for best performance
10. Consider upgrading to SSD if using traditional hard drive

Problem: High CPU usage by specific process
Solution:
1. Identify the process in Task Manager
2. For Windows processes: Run sfc /scannow to repair system files
3. For third-party software: Update or reinstall the application
4. Check for malware if process is suspicious
5. Adjust power plan to Balanced instead of High Performance
6. Update device drivers from manufacturer websites
7. Disable unnecessary background services
8. Check Windows Event Viewer for error details

Problem: 100% disk usage in Task Manager
Solution:
1. Disable Windows Search temporarily: services.msc > Windows Search > Stop
2. Disable Superfetch/SysMain service: services.msc > SysMain > Stop
3. Check for malware using full system scan
4. Update storage controller drivers from Device Manager
5. Run disk check: chkdsk /f /r in Command Prompt as admin
6. Disable Windows Tips: Settings > System > Notifications & actions
7. Change power plan settings
8. Consider upgrading to SSD if using traditional hard drive
9. Check for pending Windows updates

Problem: High memory usage
Solution:
1. Close unnecessary programs and browser tabs
2. Check Task Manager for memory-hungry processes
3. Restart Windows Explorer: Task Manager > Windows Explorer > Restart
4. Clear page file at shutdown: Registry edit (advanced users only)
5. Increase virtual memory size
6. Disable startup programs
7. Update or uninstall problematic applications
8. Check for memory leaks in third-party software
9. Upgrade RAM if consistently maxed out

# NETWORK AND CONNECTIVITY ISSUES

## Wi-Fi Connection Problems

Problem: Cannot connect to Wi-Fi network
Solution:
1. Restart router and modem: Unplug power for 30 seconds, then plug back in
2. Restart computer
3. Forget the network: Settings > Network & Internet > Wi-Fi > Manage Known Networks
4. Reconnect by entering password again
5. Update network adapter drivers: Device Manager > Network Adapters > Update driver
6. Run Network Troubleshooter: Settings > Network & Internet > Status > Network Troubleshooter
7. Reset network settings: Settings > Network & Internet > Status > Network Reset
8. Check if Wi-Fi is enabled in BIOS/UEFI settings
9. Disable airplane mode if enabled

Problem: Wi-Fi connected but no internet access
Solution:
1. Restart router and modem
2. Run network troubleshooter
3. Flush DNS cache: Open Command Prompt as admin and run ipconfig /flushdns
4. Reset TCP/IP stack: netsh int ip reset in Command Prompt as admin
5. Reset Winsock: netsh winsock reset in Command Prompt as admin
6. Change DNS servers to Google (8.8.8.8, 8.8.4.4) or Cloudflare (1.1.1.1, 1.0.0.1)
7. Disable IPv6 temporarily: Network adapter properties
8. Check router settings and ensure internet works on other devices
9. Contact ISP if problem persists across all devices
10. Check for IP address conflicts

Problem: Slow Wi-Fi speed
Solution:
1. Move closer to the router to check if distance is the issue
2. Check if other devices experience same slow speeds
3. Restart router by unplugging for 30 seconds
4. Change Wi-Fi channel to less congested one (use Wi-Fi analyzer app)
5. Switch between 2.4GHz and 5GHz bands if router supports dual-band
6. Update router firmware from manufacturer website
7. Limit number of connected devices
8. Check for background downloads or uploads on your device
9. Run speed test at different times to identify patterns
10. Consider Wi-Fi extender or mesh network for large areas
11. Check for interference from other electronic devices

Problem: Wi-Fi keeps disconnecting
Solution:
1. Update network adapter drivers from Device Manager
2. Disable power saving for network adapter: Device Manager > Network Adapter > Properties > Power Management > Uncheck 'Allow computer to turn off this device'
3. Change router wireless mode (try different 802.11 standards like AC, N, G)
4. Update router firmware
5. Change wireless channel in router settings
6. Disable IPv6 on network adapter
7. Run network adapter troubleshooter
8. Reset network settings
9. Check for overheating router
10. Change wireless security type (WPA2 to WPA3 or vice versa)

## Ethernet Connection Issues

Problem: Ethernet not working or not detected
Solution:
1. Check cable connections - ensure firmly plugged in at both ends
2. Try different Ethernet cable
3. Test cable with another device to verify cable works
4. Check if network adapter is enabled: Device Manager > Network Adapters
5. Update network adapter drivers
6. Check router/switch port with another cable
7. Run network troubleshooter
8. Reset network adapter settings
9. Check cable for physical damage
10. Try different Ethernet port on router/switch

Problem: Limited connectivity with Ethernet
Solution:
1. Restart router/modem
2. Release and renew IP: ipconfig /release then ipconfig /renew in Command Prompt
3. Check DHCP settings on router
4. Manually assign static IP address if DHCP fails
5. Flush DNS and reset TCP/IP stack
6. Update network drivers
7. Check firewall settings
8. Disable IPv6 temporarily
9. Check Ethernet cable quality (Cat5e or higher recommended)

# SOFTWARE AND APPLICATION ISSUES

## Installation Problems

Problem: Access Denied or Permission Denied during software installation
Solution:
1. Right-click installer and select 'Run as Administrator'
2. Disable User Account Control (UAC) temporarily: Control Panel > User Accounts
3. Check user account has administrator permissions
4. Ensure sufficient disk space available (check drive properties)
5. Disable antivirus/security software temporarily
6. Install in different directory (not Program Files if permission issue)
7. Check if another instance is running in Task Manager
8. Use clean boot to eliminate software conflicts

Problem: Installation stuck or frozen
Solution:
1. Wait at least 15-20 minutes (some installations are genuinely slow)
2. Check Task Manager to see if installer is still active
3. End installation process in Task Manager if truly frozen
4. Delete temporary installation files: C:\\Users\\[Username]\\AppData\\Local\\Temp
5. Restart computer
6. Run installer in compatibility mode: Right-click > Properties > Compatibility
7. Try installation in Safe Mode
8. Check installation logs for errors (usually in Temp folder)
9. Download fresh installer copy

Problem: The system cannot find the file specified error
Solution:
1. Verify installer file is not corrupted - redownload if necessary
2. Check file path length (Windows has 260 character limit for paths)
3. Move installer to C:\\ drive root to shorten path
4. Run installer as administrator
5. Check disk for errors using chkdsk
6. Temporarily disable antivirus
7. Extract installer if it's compressed archive
8. Check if required dependencies are installed

Problem: Error code 1603 - Fatal error during installation
Solution:
1. Run installer as administrator
2. Ensure sufficient disk space and proper permissions
3. Install or repair Microsoft .NET Framework
4. Update Windows to latest version
5. Check Windows Installer service is running: services.msc
6. Repair or reinstall Windows Installer
7. Check installation logs in Event Viewer
8. Disable antivirus during installation
9. Clean up registry using CCleaner (advanced users)

## Application Crashes and Freezes

Problem: Application crashes immediately on startup
Solution:
1. Restart computer
2. Update application to latest version
3. Run application as administrator
4. Run in compatibility mode: Right-click > Properties > Compatibility tab
5. Reinstall application (uninstall completely first, then clean install)
6. Check Event Viewer for error details: eventvwr.msc
7. Update Windows and all drivers
8. Check if antivirus is blocking the application
9. Repair application installation if option available
10. Delete application configuration files and try again

Problem: Application freezes or becomes unresponsive
Solution:
1. Wait a few minutes to see if it resolves itself
2. Force close: Ctrl+Alt+Delete > Task Manager > Select app > End Task
3. Clear application cache and temporary files
4. Update application to latest version
5. Check system resources in Task Manager (CPU, RAM, Disk)
6. Disable hardware acceleration in application settings
7. Run application with minimal plugins or extensions
8. Increase virtual memory if RAM usage is high
9. Check for conflicts with other running software
10. Run system file checker: sfc /scannow

Problem: Application has stopped working error
Solution:
1. Update application and Windows
2. Run Windows Update
3. Update graphics drivers from manufacturer website
4. Check for .NET Framework issues, repair if necessary
5. Scan for malware using Windows Defender
6. Run system file checker: sfc /scannow
7. Check Event Viewer for specific error codes
8. Reinstall Visual C++ Redistributables (all versions)
9. Create new user profile and test application there
10. Check application compatibility with Windows version

# HARDWARE ISSUES

## Display Problems

Problem: No display or black screen on startup
Solution:
1. Check monitor power cable and ensure monitor is turned on
2. Check video cable connections (HDMI, DisplayPort, DVI, VGA)
3. Try different video cable or port
4. Test monitor with another device to verify monitor works
5. Boot into Safe Mode: Press F8 or Shift+F8 during startup
6. Reseat graphics card (desktop only): Power off, remove and reinsert GPU
7. Try onboard graphics if available (connect to motherboard video port)
8. Reset BIOS to default settings
9. Check for loose RAM modules, reseat them
10. Listen for beep codes that indicate hardware issues

Problem: Display flickering or visual artifacts
Solution:
1. Update graphics drivers from manufacturer website (NVIDIA, AMD, Intel)
2. Adjust refresh rate: Display Settings > Advanced Display Settings
3. Check cable connections, ensure firmly plugged in
4. Try different video cable
5. Test with another monitor
6. Lower screen resolution temporarily
7. Check GPU temperature using monitoring software
8. Disable hardware acceleration in applications
9. Rollback graphics driver if issue started after recent update
10. Test GPU in another computer if possible

Problem: Wrong resolution or display settings won't save
Solution:
1. Update graphics drivers from manufacturer website
2. Set resolution manually in Display Settings
3. Use graphics control panel (NVIDIA Control Panel, AMD Radeon Settings)
4. Create custom resolution if standard options not available
5. Check scaling settings in Display Settings
6. Reinstall display drivers using DDU (Display Driver Uninstaller) in Safe Mode
7. Check monitor's native resolution specifications
8. Update monitor drivers if available

## Audio Issues

Problem: No sound from speakers or headphones
Solution:
1. Check volume levels in system tray and application
2. Ensure audio is not muted (check system tray icon)
3. Verify correct playback device selected: Settings > System > Sound > Output
4. Update audio drivers: Device Manager > Sound, video and game controllers
5. Run Audio Troubleshooter: Settings > Update & Security > Troubleshoot > Playing Audio
6. Restart Windows Audio service: services.msc > Windows Audio > Restart
7. Check physical connections and cables
8. Test with different speakers or headphones
9. Reinstall audio drivers
10. Check if audio device is disabled in Device Manager

Problem: Microphone not working
Solution:
1. Check microphone is not muted physically (check hardware mute button)
2. Adjust microphone levels: Settings > System > Sound > Input
3. Set correct input device in Sound Settings
4. Check application permissions: Settings > Privacy > Microphone
5. Update audio drivers from Device Manager
6. Test microphone in Voice Recorder app
7. Run Audio Troubleshooter for recording
8. Check if microphone works on another computer
9. Disable audio enhancements that might interfere
10. Check microphone boost levels in Sound Control Panel

Problem: Audio crackling, popping, or distortion
Solution:
1. Update audio drivers to latest version
2. Change audio format: Sound > Playback device > Properties > Advanced tab
3. Disable audio enhancements: Sound > Playback > Properties > Enhancements > Disable all
4. Adjust buffer size in audio software or DAW
5. Close resource-heavy applications
6. Check DPC latency using LatencyMon tool
7. Update chipset drivers from motherboard manufacturer
8. Disable power saving for USB controllers (for USB audio devices)
9. Try different USB port (USB 2.0 instead of 3.0 sometimes helps)
10. Check for electrical interference from other devices

## Printer Issues

Problem: Printer not detected or not printing
Solution:
1. Check printer power and ensure it's turned on
2. Check USB or network cable connections
3. Restart printer and computer
4. Set as default printer: Settings > Devices > Printers & scanners
5. Update printer drivers from manufacturer website
6. Run Printer Troubleshooter: Settings > Update & Security > Troubleshoot
7. Clear print queue: services.msc > Print Spooler > Stop, clear folder, Start
8. Reinstall printer: Remove device, restart, then add printer again
9. Check for paper jams
10. Verify ink or toner levels
11. Disable bidirectional support in printer properties if network printer

Problem: Printer prints blank pages
Solution:
1. Check ink or toner levels
2. Clean print heads using printer maintenance utility
3. Run printer alignment from printer software
4. Check if correct paper type is selected in print settings
5. Update printer drivers
6. Try printing from different application
7. Check printer queue for errors
8. Reset printer to factory settings
9. Remove and reinstall ink cartridges
10. Run nozzle check pattern to diagnose

Problem: Printer printing slowly
Solution:
1. Change print quality to draft or normal instead of high quality
2. Print in black and white instead of color
3. Update printer drivers
4. Check printer memory if printing complex documents
5. Reduce document complexity (fewer graphics, lower resolution images)
6. Check network connection speed for network printers
7. Clear print queue of old jobs
8. Restart print spooler service
9. Check computer resources in Task Manager

## USB Device Problems

Problem: USB device not recognized
Solution:
1. Try different USB port (front and back ports)
2. Restart computer with device connected
3. Update USB drivers: Device Manager > Universal Serial Bus controllers
4. Disable USB selective suspend: Power Options > Change plan settings > Advanced > USB settings
5. Uninstall and reinstall USB controllers in Device Manager
6. Check if device works on another computer
7. Reset USB ports in BIOS settings
8. Check for physical damage to port or cable
9. Try device without USB hub (connect directly)
10. Update chipset drivers

Problem: USB device keeps disconnecting
Solution:
1. Try different USB port (prefer USB 2.0 for problematic devices)
2. Use powered USB hub for power-hungry devices
3. Update USB drivers and chipset drivers
4. Disable power management for USB: Device Manager > USB Root Hub > Properties > Power Management
5. Check power supply (ensure laptop is plugged in, not on battery)
6. Update device firmware if available
7. Check cable quality and length (longer cables can cause issues)
8. Check for loose connections
9. Disable USB Legacy Support in BIOS
10. Replace USB cable

# EMAIL AND BROWSER ISSUES

## Email Client Problems

Problem: Cannot send emails (receiving works fine)
Solution:
1. Check outgoing SMTP server settings in email client
2. Verify SMTP port (usually 587 for TLS/STARTTLS or 465 for SSL)
3. Ensure SMTP authentication is enabled
4. Check if antivirus is blocking outgoing mail
5. Verify email account username and password are correct
6. Check internet connection stability
7. Disable VPN temporarily and test
8. Check if mail server is down (try accessing webmail)
9. Increase SMTP timeout settings in email client
10. Check firewall settings

Problem: Cannot receive emails (sending works fine)
Solution:
1. Check incoming server settings (POP3 port 110/995 or IMAP port 143/993)
2. Verify SSL/TLS settings match server requirements
3. Check mailbox storage quota (might be full)
4. Verify login credentials are correct
5. Check spam or junk folder for missing emails
6. Disable firewall temporarily to test
7. Try accessing via webmail to see if emails are on server
8. Check email forwarding rules aren't redirecting mail
9. Verify correct email protocol (POP3 vs IMAP)
10. Contact email provider to verify account status

## Web Browser Issues

Problem: Browser running slow or freezing
Solution:
1. Clear browsing data: Settings > Privacy > Clear browsing data (cache, cookies, history)
2. Disable unnecessary extensions: Settings > Extensions
3. Update browser to latest version
4. Reset browser settings to default
5. Scan for malware using Windows Defender
6. Disable hardware acceleration: Settings > Advanced > System
7. Create new browser profile
8. Check for DNS issues, try changing DNS servers
9. Increase browser cache size in settings
10. Reinstall browser if necessary

Problem: Websites not loading or connection errors
Solution:
1. Check internet connection (try other websites)
2. Try different browser to isolate issue
3. Clear browser cache and cookies
4. Flush DNS cache: ipconfig /flushdns in Command Prompt
5. Change DNS servers to 8.8.8.8 and 8.8.4.4
6. Disable VPN or proxy temporarily
7. Disable browser extensions
8. Check firewall and antivirus settings
9. Reset browser to default settings
10. Check if specific website is down using downdetector.com

Problem: Your connection is not private or SSL/TLS errors
Solution:
1. Check system date and time settings (incorrect time causes SSL errors)
2. Clear browser cache and cookies completely
3. Disable antivirus SSL scanning temporarily
4. Update browser to latest version
5. Clear SSL state: Internet Options > Content tab > Clear SSL State button
6. Check for malware infection
7. Try incognito or private browsing mode
8. Temporarily disable all browser extensions
9. Reset browser to default settings
10. Check if certificate is actually invalid or expired

# SECURITY AND MALWARE

## Virus and Malware Removal

Problem: Computer infected with malware or virus
Solution:
1. Disconnect from internet immediately (unplug Ethernet or disable Wi-Fi)
2. Boot into Safe Mode with Networking (restart, press F8 repeatedly)
3. Run Windows Defender full scan (Windows Security > Virus & threat protection)
4. Download and run Malwarebytes free version
5. Use additional tools: AdwCleaner for adware, HitmanPro for rootkits
6. Check browser extensions in all browsers and remove suspicious ones
7. Check startup programs: Task Manager > Startup tab
8. Check scheduled tasks for malicious entries
9. Reset all browsers to default settings
10. Change all passwords after system is clean
11. Enable Windows Defender real-time protection permanently

Problem: Ransomware infection
Solution:
1. DO NOT pay the ransom (no guarantee of decryption)
2. Disconnect from network immediately to prevent spread
3. Identify ransomware variant using ID Ransomware website
4. Check if free decryption tools available (NoMoreRansom project)
5. Restore files from backup if available (disconnect backup drive first)
6. If no decryption or backup: may need to rebuild system
7. Report incident to local law enforcement
8. Contact cybersecurity professionals for critical business data
9. Document everything for insurance claims
10. Implement better backup strategy to prevent future incidents

Problem: Browser hijacker or unwanted search engine
Solution:
1. Uninstall suspicious programs: Control Panel > Uninstall a program
2. Remove unwanted browser extensions from all browsers
3. Reset browser settings to default (each browser has reset option)
4. Clear cache, cookies, and browsing history
5. Check hosts file for modifications: C:\\Windows\\System32\\drivers\\etc\\hosts
6. Check proxy settings: Internet Options > Connections > LAN Settings
7. Run AdwCleaner to remove adware
8. Scan with Malwarebytes
9. Reset DNS settings to automatic or use trusted DNS
10. Check homepage and search engine settings in browser

## Account Security

Problem: Forgot Windows login password
Solution:
1. Use password reset disk if you created one previously
2. Use another administrator account to reset password
3. Boot from Windows installation media, access Command Prompt (Shift+F10)
4. Use Microsoft account recovery online if linked
5. Use Offline NT Password & Registry Editor tool
6. Contact system administrator in work environment
7. Last resort: Reinstall Windows (will lose data if not backed up)
8. Set up PIN or Windows Hello for future easier recovery

Problem: Account locked due to too many failed login attempts
Solution:
1. Wait 30-60 minutes for automatic unlock (default policy)
2. Use another administrator account to manually unlock
3. Boot into Safe Mode with administrator account
4. Reset account lockout policy: secpol.msc > Account Lockout Policy
5. In domain environment: Contact IT administrator
6. Use password reset disk if available
7. Check Event Viewer for security logs showing lockout reason

# DATA RECOVERY AND BACKUP

## File Recovery

Problem: Accidentally deleted important files
Solution:
1. Check Recycle Bin first (most common location)
2. Use File History if enabled: Settings > Update & Security > Backup > Restore files
3. Use Previous Versions: Right-click parent folder > Properties > Previous Versions tab
4. Use free recovery software: Recuva, EaseUS Data Recovery Wizard, PhotoRec
5. Stop using the drive immediately to prevent overwriting deleted files
6. For critical data: Consider professional data recovery services
7. Check OneDrive, Google Drive, or other cloud services
8. Check shadow copies: vssadmin list shadows
9. Use Windows System Restore if files were deleted recently
10. Check email attachments if files were previously sent

Problem: Corrupted files or cannot open files
Solution:
1. Try opening with different application
2. Use file-specific repair tools (Office repair, PDF repair, etc.)
3. Restore from backup copy
4. Run System File Checker if system files: sfc /scannow
5. Check disk for errors: chkdsk /f /r
6. Try online file repair services (last resort, privacy concerns)
7. Contact original file creator for another copy
8. Try opening on different computer
9. Use data recovery software to extract partial data
10. Check if file is actually downloading completely

## Backup Issues

Problem: Windows Backup fails or stops working
Solution:
1. Ensure sufficient space on backup destination drive
2. Check backup drive connection and health
3. Run Windows Backup troubleshooter
4. Check Event Viewer for specific error messages
5. Disable antivirus temporarily during backup
6. Manually delete old backup files to free space
7. Use different backup location (different drive or network location)
8. Reset Windows Backup: Delete backup configuration, set up new
9. Check backup drive for errors: chkdsk on backup drive
10. Use alternative backup software (Macrium Reflect, EaseUS Todo Backup)

Problem: Restore from backup not working
Solution:
1. Verify backup files are intact and not corrupted
2. Check if backup software version matches
3. Ensure sufficient disk space for restoration
4. Try restoring specific files instead of full system
5. Use backup software's repair or rebuild catalog feature
6. Check backup drive connection and health
7. Try restoring to different location first
8. Use compatibility mode if backup is old
9. Extract files manually from backup archive if possible
10. Contact backup software support for assistance

# MISCELLANEOUS ISSUES

## System Time and Date

Problem: System time and date keeps resetting
Solution:
1. Replace CMOS battery on motherboard (CR2032 coin battery)
2. Enable Windows Time service: services.msc > Windows Time > Automatic
3. Sync with internet time server: Settings > Time & Language > Additional date, time & region settings
4. Select reliable time server (time.windows.com or time.nist.gov)
5. Check time zone settings are correct
6. Disable dual boot time UTC conflicts (if dual booting)
7. Update BIOS/UEFI firmware
8. Check for malware affecting system time
9. Run system file checker: sfc /scannow
10. Check motherboard health

## Activation and Licensing

Problem: Windows is not activated
Solution:
1. Check internet connection (activation requires internet)
2. Run activation troubleshooter: Settings > Update & Security > Activation > Troubleshoot
3. Verify product key is correct and not already used
4. Ensure product key matches Windows edition
5. Contact Microsoft support if hardware changed significantly
6. Check if digital license is linked to Microsoft account
7. Use phone activation if internet activation fails
8. Verify Windows is genuine and not pirated
9. Check if license is OEM (tied to motherboard)
10. Reactivate after hardware change using linked Microsoft account

Problem: Windows is not genuine message
Solution:
1. Verify Windows is properly licensed
2. Run genuine Windows validation from Microsoft
3. Check if Windows key has been used on multiple PCs (violation)
4. Reinstall Windows from official Microsoft ISO
5. Contact Microsoft support with proof of purchase
6. Check for malware that may modify system files
7. Restore system files: sfc /scannow and DISM commands
8. Check if recent Windows update caused activation issue
9. Verify Windows edition matches product key
10. Purchase legitimate license if currently using pirated copy
"""
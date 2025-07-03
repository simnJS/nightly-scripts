# 🤖 Nighty Selfbot Scripts Collection

A comprehensive collection of automation scripts for the Nighty Discord selfbot, featuring voice channel management, cryptocurrency utilities, server management, and system automation.

## 📋 Table of Contents

- [Features](#-features)
- [Scripts Overview](#-scripts-overview)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)

## ✨ Features

- **🎤 Auto Voice Channel Joining** - Automatically join voice channels when slots become available
- **💰 Cryptocurrency Address Info** - Lookup information for various cryptocurrency addresses
- **🏛️ Discord Server Management** - Manage and leave Discord servers with ease
- **📊 Message Counter** - Count messages for safe purging operations without damage

## 📦 Scripts Overview

### 🎤 Auto Voice Channel Joiner v2.0
**File:** `auto_voice_joiner.py`
**Author:** simnJS

Advanced voice channel auto-joiner with modern UI interface.

**Features:**
- Modern UI for configuration and monitoring
- Real-time status tracking and logging
- Configurable check intervals and attempt limits
- Smart channel validation and testing
- Automatic retry system
- Success/failure statistics tracking

**Usage:**
1. Open the "Auto Voice Joiner" tab in Nighty UI
2. Enter target voice channel ID
3. Configure check interval and max attempts
4. Click "Start Auto Joiner"

### 💰 Crypto Address Info v1.10
**File:** `cryptoinfo.py`
**Author:** simnJS

Comprehensive cryptocurrency address information lookup tool.

**Supported Currencies:**
- BTC (Bitcoin)
- LTC (Litecoin) 
- ETH (Ethereum)
- BCH (Bitcoin Cash)
- DOGE (Dogecoin)
- DASH (Dash)
- ZEC (Zcash)
- BTS (BitShares)

**Commands:**
```
<p>cryptoinfo <currency> <address>
```

**Examples:**
```
<p>cryptoinfo btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
<p>cryptoinfo eth 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
```

**Features:**
- Balance and transaction information
- EUR conversion rates
- Support for multiple blockchain APIs
- Clean error handling and logging

### 🏛️ Guilds Manager v1.0
**File:** `guild_manager.py`
**Author:** simnJS

Discord server management interface with visual guild listing.

**Features:**
- Visual server listing with names and icons
- One-click server leaving functionality
- Toast notifications for feedback
- Automatic interface updates
- Alphabetically sorted server list
- Two-column layout with scroll support

**Usage:**
Access the "Guilds Manager" tab in Nighty to view and manage servers.

### 📊 Message Counter v1.0
**File:** `message_counter.py`
**Author:** simnJS

Safe message counting tool for calculating purge operations without damage.

**Features:**
- Count messages from a specific message ID to current time
- Work from any channel/server with proper channel/server IDs
- Show detailed message information and timestamps
- Safe purge calculation with exact counts
- Error handling for invalid message IDs and inaccessible channels
- Cross-server counting with permissions validation

**Commands:**
```
<p>count <message_id>                              - Count in current channel
<p>count <channel_id> <message_id>                 - Count in specific channel  
<p>count <guild_id> <channel_id> <message_id>      - Count in specific server/channel
```

**Examples:**
```
<p>count 1234567890123456789
<p>count 987654321098765432 1234567890123456789
<p>count 111222333444555666 987654321098765432 1234567890123456789
```

**Usage Scenario:**
1. Find the message ID you want to purge FROM
2. Use `<p>count` with appropriate IDs to see how many messages would be affected
3. Use the count for safe purging operations from any channel/server

**Features:**
- Shows target message details (author, content preview, timestamp)
- Counts messages after the target message
- Provides total purge count (including target message)
- Displays time information and safety warnings

### 🚀 Nighty Auto Start
**File:** `Nighty Auto Start.py`
**Author:** Flixer (improved version)

Automatically adds Nighty to Windows startup and handles updates.

**Features:**
- Automatic Windows startup registration
- Auto-update startup entries for new Nighty versions
- Creates startup batch file in Windows startup folder
- Handles existing startup entries replacement

## 🛠️ Installation

1. Clone this repository to your Nighty scripts directory:
```bash
git clone <repository-url>
```

2. Ensure you have Nighty selfbot installed and running

3. Load the scripts through the Nighty interface or place them in the appropriate scripts directory

## 🎯 Usage

### For UI Scripts:
1. Load the script in Nighty
2. Access the corresponding tab in the Nighty interface
3. Configure settings through the UI
4. Use the provided controls to start/stop functionality

### For Command Scripts:
Use the designated command prefixes as specified in each script's documentation.

## ⚙️ Configuration

### Auto Voice Joiner
- **Target Channel ID**: Voice channel to automatically join
- **Check Interval**: Time between availability checks (seconds)
- **Max Attempts**: Maximum number of join attempts
- **Debug Mode**: Enable detailed logging

### Crypto Info
- **API Endpoints**: Uses blockchain.info and blockcypher.com APIs
- **Currency Support**: Configurable through SUPPORTED_CURRENCIES dictionary

### Guild Manager
- **Auto-refresh**: Automatically updates server list
- **Error Handling**: Built-in error handling for leave operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## ⚠️ Disclaimer

**Important:** This collection is designed for the Nighty Discord selfbot. Please ensure you comply with Discord's Terms of Service and your local laws when using these scripts. Self-bots operate in a legal gray area and may violate Discord's ToS.

**Use at your own risk.** The authors are not responsible for any consequences resulting from the use of these scripts.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Additional Notes:** This project is provided as-is for educational and automation purposes. Please respect Discord's Terms of Service and use responsibly.

---

**Made for the Nighty Community** 🌙

For support or questions, contact the respective script authors mentioned in each script's documentation. 
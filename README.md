# Home Assistant to Light Symphony iPort

[![Available in Marketplace](https://img.shields.io/badge/Marketplace-Available-41BDF5)](#installation-with-marketplace)
[![maintained](https://img.shields.io/maintenance/yes/2026.svg)](#)
[![maintainer](https://img.shields.io/badge/maintainer-%20%40petes--UK-blue.svg)](#)
[![version](https://img.shields.io/github/v/release/peteS-UK/iport)](#)

This custom component implements a device and switch entities for Home Assistant to allow for control of the Light Symphony iPort.  

The iPort doesn't communicate any state information about the lights - i.e. if they're turned on or off.  So, the integration maintains the state of the lights within Home Assistant.  This means that after a restart of HA, the state could be incorrect, until the lights have been turned On and Off - which will have the effect of syncing HA's state with the actual state of the lights.

## Installation with Marketplace

The [Marketplace](https://www.home-assistant.io/integrations/marketplace/) is built into **Home Assistant 2026.11 and later**; no separate store installation is needed.

1. As an administrator, open **Settings → Marketplace** and accept its first-use notice if prompted.
2. Search for **Light Symphony iPort** and open its page.
3. Choose **Install**, review the version, then confirm **Install**. Account setup opens when installation finishes; continue with [Configuration](#configuration). A fresh installation does not need a restart.

Existing HACS installations migrate automatically when you upgrade Home Assistant to 2026.11. Your installed integration and updates carry over; you do not need to reinstall it.

## Installation with HACS

For older versions of Home Assistant, you can install via Home Assistant Community Store - aka [HACS](https://hacs.xyz/).  Search for **Light Symphony iPort** and install the integration.

## Manual Installation
If you want to download the integration manually, create a new folder called iport under your custom_components folder in your config folder.  If the custom_components folder doesn't exist, create it first.  Once created, download the files and folders from the [github repo](https://github.com/peteS-UK/iport/tree/main/custom_components/iport) into this new iport folder.

Once downloaded either via HACS or manually, restart your Home Assistant server.

Configuration is done through the Home Assistant UI.  Once you're installed the integration, go into your Integrations (under Settings, Devices & Services), select Add Integration, and choose the Light Symphony iPort integration, or click the shortcut button below (requires My Homeassistant configured).

[![Add Integration to your Home Assistant
instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=iport)

This will display the configuration page.

## Configuration

You can select the IP address and name of the iPort.  You can also optionally name the areas, or leave them as their default values.

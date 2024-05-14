# Home Assistant to Light Symphony iPort

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)


This custom component implements a device and switch entities for Home Assistant to allow for control of the Light Symphony iPort.  

The iPort doesn't communicate any state information about the lights - i.e. if they're turned on or off.  So, the integration maintains the state of the lights within Home Assistant.  This means that after a restart of HA, the state could be incorrect, until the lights have been turned On and Off - which will have the effect of syncing HA's state with the actual state of the lights.

## Installation

The preferred installation approach is via Home Assistant Community Store - aka [HACS](https://hacs.xyz/).  The repo is installable as a [Custom Repo](https://hacs.xyz/docs/faq/custom_repositories) via HACS.

If you want to download the integration manually, create a new folder called iport under your custom_components folder in your config folder.  If the custom_components folder doesn't exist, create it first.  Once created, download the files and folders from the [github repo](https://github.com/peteS-UK/iport/tree/main/custom_components/iport) into this new iport folder.

Once downloaded either via HACS or manually, restart your Home Assistant server.

## Configuration

Configuration is done through the Home Assistant UI.  Once you're installed the integration, go into your Integrations (under Settings, Devices & Services), select Add Integration, and choose the Light Symphony iPort integration.

This will display the configuration page, where you can select the IP address and name of the iPort.  You can also optionally name the areas, or leave them as their default values.

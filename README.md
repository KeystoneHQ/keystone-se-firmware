# Keystone Secure Element Firmware

**The Keystone hardware wallet is simply relaunched from the Cobo Vault branding so both the code base and infrastructure are the same. For more info please checkout [here](https://blog.keyst.one/leaving-cobo-to-continue-the-cobo-vault-legacy-29bb2f8f026e)**


Keystone is an air-gapped, open source hardware wallet that uses completely transparent QR code data transmissions. Visit the [Keystone official website]( https://keyst.one)  to learn more about Keystone.

You can also follow [@Keystone](https://twitter.com/KeystoneWallet) on Twitter.

<div align=center><img src="https://keyst.one/c430c589a841d8b8379c66766e78c95d.png"/></div>

## Table of Contents

- [Clone](#clone)
- [Build](#build)
- [Code Structure](#code-structure)
- [Issues and PRs](#issues-and-prs)
- [License](#license)

## Clone

    git clone git@github.com:KeystoneHQ/keystone-se-firmware.git

## Build
    Currently, the source can only be compiled on Windows.
    You can build with ARM IDEs like "Keil MDK V4.x".
1. Download Keil MDK4.x [here](https://www.keil.com/demo/eval/armv4.htm).
2. Install MDK and register license.
3. Run MDK, and add firmware project. Open the dialog `Project - Open Project`, select `mason.uvproj` [here](./mason.uvproj).
4. Build the firmware project. Select the dialog `Project - Rebuild all target files` to compile the source files.
5. Find the firmware image `mason_app.hex` and `mason_app.bin` in directory `./`.

## Code Structure
Modules:

`source` : Source files for Secure Element firmware

`upgrade` : Python script for verifying update package

`*.bat`: Script file for compiling

`uvproj`: Project files for MDK IDE

## License
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](https://opensource.org/licenses/)
This project is licensed under the GPL License. See the [LICENSE](LICENSE) file for details.

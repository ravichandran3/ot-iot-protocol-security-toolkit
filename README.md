# Scripts for Pentesting & Red Teaming

A collection of standalone, dependency-light Python scripts for security research, penetration testing, and red teaming across various operational technology (OT), IoT, aviation, maritime, building automation, and communication protocols.

The scripts are organized by domain and are intended for educational purposes, security assessments, and authorized testing only.

## Overview

This repository provides practical tools for interacting with and analyzing systems that are often found in critical infrastructure, aviation, maritime, and building automation environments.

Each script is designed to be self-contained, often implementing protocol logic from scratch to aid in understanding and testing. The tools cover both offensive operations such as message forgery and unauthorized writes, and defensive analysis such as decoding, integrity checks, and clustering.

## Repository Structure

The repository is organized into directories, each focusing on a specific domain or protocol:

| Directory | Focus Area |
| :--- | :--- |
| `adsb` | ADS-B (Automatic Dependent Surveillance–Broadcast) for aviation |
| `ais` | AIS (Automatic Identification System) for maritime vessels |
| `avionics` | Avionics data bus protocols (ARINC 429, MIL-STD-1553) |
| `bacnet` | BACnet/IP for building automation and control systems |
| `cable` | Network topology analysis for submarine cable landing stations |
| `crypt` | Classical cryptography (Vigenère, XOR) analysis and recovery |
| `deepfake` | Perceptual hashing for media forensics and clustering |
| `dna` | DNA/biological data analysis scripts |
| `dp` | Data processing / differential privacy related scripts |
| `feed` | Feed parsing and processing scripts |
| `gnss` | GNSS / GPS signal processing scripts |
| `mesh` | Mesh network analysis scripts |
| `plc` | Programmable Logic Controller interaction scripts |
| `scada` | SCADA system testing scripts |
| `tc` | Traffic control or tactical communications scripts |

## Detailed Script Descriptions

### `adsb` - ADS-B (Aviation)

- **`adsb.py`**: Implements Mode S / ADS-B extended squitter processing, including CRC-24 calculation, aircraft identification encoding/decoding, and Compact Position Reporting (CPR) for latitude/longitude. It allows for the construction and parsing of ADS-B frames.
- **`chk.py`, `chk2.py`, `t3.py`**: Test scripts that validate the encoding, decoding, and CRC functions implemented in `adsb.py`.

### `ais` - AIS (Maritime)

- **`ais.py`**: Encodes and decodes AIS Type-1 position reports. It handles 6-bit armoring, checksum calculation, and payload packing/unpacking. It includes a function to forge AIS messages with arbitrary MMSI, position, speed, and course.

### `avionics` - Avionics Data Buses

- **`arinc.py`**: Provides encoding and decoding for ARINC 429 words and MIL-STD-1553 command words. It includes functions for bit-field manipulation, parity calculation, and BNR (Binary Coded Decimal) conversion. It also demonstrates how to forge an ARINC 429 word without updating the parity bit.

### `bacnet` - Building Automation

- **`bacnet.py`**: A low-level BACnet/IP frame builder. It constructs BVLC, NPDU, and APDU packets for services like Who-Is, ReadProperty, and WriteProperty.
- **`bms.py`**: A simple BACnet/IP device simulator that responds to Who-Is and ReadProperty requests and accepts WriteProperty commands without authentication.
- **`scan.py`**: A client script that discovers a BACnet device, reads a property, writes a new value, and verifies the change.

### `cable` - Network Topology Analysis

- **`cable.py`**: Uses NetworkX to model the network topology of a submarine cable landing station. It analyzes reachability from the internet to critical assets, calculates minimum edge cuts, and simulates the impact of removing nodes or edges.

### `crypt` - Cryptography

- **`crypt.py`**: Implements cryptanalysis techniques for classical ciphers. It includes functions for Vigenère cipher encoding/decoding, Index of Coincidence (IC) calculation, key length detection, and key recovery using chi-square scoring. It also provides repeating-key XOR encryption/decryption and Hamming distance calculation.
- **`dbg.py`, `dbg2.py`, `dbg3.py`**: Debugging and testing scripts that demonstrate the cryptanalysis functions on sample plaintext.

### `deepfake` - Media Forensics

- **`dhash.py`**: Generates perceptual hashes (dHash) for images. It simulates a set of near-duplicate images, as might be found in a deepfake campaign, and clusters them based on Hamming distance, demonstrating how to group media by visual similarity without relying on metadata.

## Installation

Most scripts require only the Python standard library. However, some scripts have additional dependencies:

- **`cable.py`**: Requires `networkx`.
- **`deepfake/dhash.py`**: Requires `numpy`.

You can install the optional dependencies with:

```bash
pip install networkx numpy
```

## Usage

Each script can be run directly from the command line. For example:

```bash
# Run the ADS-B CRC test
python adsb/t3.py

# Run the BACnet scanner (ensure a simulator is running)
python bacnet/bms.py &  # Start the device simulator in the background
python bacnet/scan.py

# Run the network topology analysis
python cable/cable.py

# Run the deepfake clustering demo
python deepfake/dhash.py
```

Many scripts also function as libraries, allowing you to import specific functions into your own tools.

## Disclaimer

**This repository is intended for educational and authorized security testing purposes only.**

The tools and techniques demonstrated here should only be used against systems you own or have explicit permission to test. Unauthorized use of these tools against production systems, critical infrastructure, or networks you do not own is illegal and unethical. The author assumes no liability for any misuse or damage caused by these scripts.

## Contributing

Contributions are welcome. If you have a script that fits the theme of the repository, please ensure it is well-documented, self-contained, and includes a clear explanation of its purpose and any ethical considerations. Submit a pull request with a description of your addition.

## License

This project is provided as-is for educational purposes. Please refer to the repository for any specific licensing information.

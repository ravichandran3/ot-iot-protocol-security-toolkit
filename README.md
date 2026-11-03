# OT-IoT Protocol Security Toolkit

> A collection of standalone, dependency-light Python scripts for security research, penetration testing, and red teaming across OT (Operational Technology), IoT, aviation, maritime, building automation, and communication protocols.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)](#license)
[![Focus](https://img.shields.io/badge/Focus-OT%20%7C%20IoT%20%7C%20ICS%20%7C%20Protocol%20Security-red.svg)](#overview)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

---

## Overview

**OT-IoT Protocol Security Toolkit** is a curated set of standalone Python scripts for interacting with and analyzing systems found in critical infrastructure, aviation, maritime, industrial control, and building automation environments.

Each script is self-contained and often implements protocol logic **from scratch** — CRC calculations, payload packing/unpacking, frame builders, checksum verification — so you can learn, test, and extend them without heavy dependencies.

The toolkit covers both **offensive** operations (message forging, unauthorized writes, spoofing) and **defensive** analysis (decoding, integrity checks, topology reachability, media clustering).

**Keywords:** pentesting · red teaming · OT security · IoT security · ICS security · SCADA · PLC · BACnet · ADS-B · AIS · ARINC 429 · MIL-STD-1553 · protocol fuzzing · GNSS · maritime security · aviation security · critical infrastructure · cyber security tooling

---

## Why This Toolkit

- **Protocol-level, not wrapper-level** — no `pip install` of a giant framework just to send one BACnet frame
- **Readable and auditable** — each script is a single file you can read end-to-end
- **Covers niches** — ADS-B CPR decoding, AIS 6-bit armoring, ARINC 429 parity, MIL-STD-1553 command words, submarine cable topology
- **Useful for both offense and defense** — forge on one side, decode/analyze on the other
- **Zero-to-minimal dependencies** — mostly Python standard library

---

## Repository Structure

| Directory | Focus Area |
| :--- | :--- |
| `adsb` | ADS-B (Automatic Dependent Surveillance–Broadcast) — aviation |
| `ais` | AIS (Automatic Identification System) — maritime vessels |
| `avionics` | Avionics data buses (ARINC 429, MIL-STD-1553) |
| `bacnet` | BACnet/IP — building automation and control systems |
| `cable` | Submarine cable landing station topology analysis |
| `crypt` | Classical cryptography (Vigenère, XOR) analysis and recovery |
| `deepfake` | Perceptual hashing for media forensics and clustering |
| `dna` | DNA / biological data analysis scripts |
| `dp` | Data processing / differential privacy scripts |
| `feed` | Feed parsing and processing scripts |
| `gnss` | GNSS / GPS signal processing scripts |
| `mesh` | Mesh network analysis scripts |
| `plc` | Programmable Logic Controller interaction scripts |
| `scada` | SCADA system testing scripts |
| `tc` | Traffic control / tactical communications scripts |

---

## Detailed Script Descriptions

### `adsb` — ADS-B (Aviation)

- **`adsb.py`** — Mode S / ADS-B extended squitter processing: CRC-24 calculation, aircraft identification encoding/decoding, and Compact Position Reporting (CPR) for latitude/longitude. Construct and parse ADS-B frames.
- **`chk.py`, `chk2.py`, `t3.py`** — Test scripts validating encoding, decoding, and CRC functions in `adsb.py`.

### `ais` — AIS (Maritime)

- **`ais.py`** — Encode and decode AIS Type-1 position reports. Handles 6-bit armoring, checksum, and payload packing/unpacking. Includes a function to **forge AIS messages** with arbitrary MMSI, position, speed, and course.

### `avionics` — Avionics Data Buses

- **`arinc.py`** — Encode/decode ARINC 429 words and MIL-STD-1553 command words. Bit-field manipulation, parity calculation, BNR conversion. Demonstrates forging an ARINC 429 word without updating the parity bit.

### `bacnet` — Building Automation

- **`bacnet.py`** — Low-level BACnet/IP frame builder: BVLC, NPDU, and APDU packets for Who-Is, ReadProperty, and WriteProperty.
- **`bms.py`** — BACnet/IP device simulator responding to Who-Is/ReadProperty and accepting WriteProperty without authentication.
- **`scan.py`** — Client that discovers a BACnet device, reads a property, writes a new value, and verifies the change.

### `cable` — Network Topology Analysis

- **`cable.py`** — Uses NetworkX to model a submarine cable landing station topology. Analyzes reachability from the internet to critical assets, computes minimum edge cuts, and simulates impact of node/edge removal.

### `crypt` — Cryptography

- **`crypt.py`** — Classical cryptanalysis: Vigenère encode/decode, Index of Coincidence (IC), key-length detection, chi-square key recovery, repeating-key XOR, and Hamming distance.
- **`dbg.py`, `dbg2.py`, `dbg3.py`** — Debugging scripts demonstrating cryptanalysis functions on sample plaintext.

### `deepfake` — Media Forensics

- **`dhash.py`** — Generates perceptual hashes (dHash) for images, simulates near-duplicate sets (as in a deepfake campaign), and clusters them by Hamming distance — grouping media by visual similarity without metadata.

---

## Installation

Most scripts require only the **Python 3.8+ standard library**.

Optional dependencies:

- **`cable.py`** → `networkx`
- **`deepfake/dhash.py`** → `numpy`

Install optional dependencies:

```bash
pip install networkx numpy
```

Clone and run:

```bash
git clone https://github.com/ravichandran3/ot-iot-protocol-security-toolkit.git
cd ot-iot-protocol-security-toolkit
```

---

## Usage

Each script runs directly from the command line:

```bash
# ADS-B CRC test
python adsb/t3.py

# BACnet scanner (start simulator first)
python bacnet/bms.py &
python bacnet/scan.py

# Submarine cable topology analysis
python cable/cable.py

# Deepfake perceptual hash clustering
python deepfake/dhash.py
```

Most scripts also work as importable libraries:

```python
from adsb.adsb import crc24
from ais.ais import encode_type1
```

---

## Ideal For

- Penetration testers working on **OT / ICS / IoT** engagements
- Red teamers targeting **aviation, maritime, building automation**
- Blue teamers building **protocol-aware detections**
- Researchers writing **conference PoCs, labs, and CTF challenges**
- Students learning **how protocols actually work on the wire**

---

## Disclaimer

**This repository is intended for educational and authorized security testing purposes only.**

Use these tools only against systems you own or have explicit permission to test. Unauthorized use against production systems, critical infrastructure, or networks you do not own is illegal and unethical. The author assumes no liability for misuse or damage.

---

## Contributing

Contributions are welcome. If you have a script that fits the toolkit:

1. Keep it **self-contained** and dependency-light
2. **Document** the protocol, the offensive/defensive use, and ethical considerations
3. Include a **usage example** in the file or a short note
4. Open a **pull request** with a description

---

## License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Star History & Support

If this toolkit helps your work, **⭐ star the repo** — it helps others in the OT/IoT security community find it.

For questions, ideas, or responsible disclosures, open an **issue** or reach out via GitHub.

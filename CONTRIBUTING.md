# Contributing

Thanks for your interest in improving **OT-IoT Protocol Security Toolkit**!

This repository is a curated collection of standalone, dependency-light Python scripts for OT / IoT / ICS protocol security research, pentesting, and red teaming.

## How to Contribute

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/ot-iot-protocol-security-toolkit.git
cd ot-iot-protocol-security-toolkit
```

### 2. Create a branch

```bash
git checkout -b feature/short-descriptive-name
```

### 3. Add your script

Follow these guidelines:

- **Self-contained** — one script per file, minimal external dependencies (standard library preferred)
- **Readable** — someone should be able to read it end-to-end and understand it
- **Documented** — include a short docstring at the top explaining:
  - What protocol / system it targets
  - What it does (offensive or defensive)
  - Any prerequisites (network, hardware, simulator)
- **Runnable** — include a `if __name__ == "__main__":` block with a usage example
- **Ethical** — no scripts that target real production systems without authorization

### 4. Update the README

If you add a new script or directory, add a corresponding entry to the **Repository Structure** table and the **Detailed Script Descriptions** section in `README.md`.

### 5. Open a Pull Request

In your PR description, include:

- **What** the script does
- **Why** it's useful (use case, scenario, or protocol gap it fills)
- **How** to run it (command or minimal example)
- **Ethical note** — confirm it's intended for authorized testing only

## Style Guidelines

- Python 3.8+
- 4-space indentation
- Follow PEP 8 where practical
- No hardcoded credentials, API keys, or private IPs
- Use descriptive variable names over single letters (except in tight loops)

## What We Accept

- New protocol implementations (encoding, decoding, framing, checksums)
- Offensive scripts (forging, spoofing, fuzzing, injection) with clear ethical framing
- Defensive scripts (parsers, integrity checks, detection logic, topology analysis)
- Test/validation scripts for existing tools
- Bug fixes and documentation improvements

## What We Don't Accept

- Scripts that require proprietary or pirated software
- Scripts targeting live systems without a clear ethical disclaimer
- Droppers, backdoors, ransomware, or malware of any kind
- Anything that violates laws or terms of service

## Code of Conduct

Be respectful, constructive, and ethical. This toolkit exists to **help defenders and authorized testers**, not to enable abuse.

## Questions?

Open an [issue](https://github.com/ravichandran3/ot-iot-protocol-security-toolkit/issues) or start a discussion.

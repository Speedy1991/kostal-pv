# This repo is WORK IN PROGRESS

## What is this
- Reading multiple registers from KSEM
- Reading multiple dxindexes from Inverters (tested with Piko15)
- Write datapoints to a influx db

## Requirements
- python3.6+
- git

## Setup
- Clone this respo with `git clone https://github.com/Speedy1991/kostal-pv.git`
- `pip[3] install -r requirements.txt`
- You only need to modify the `config.ini` file

## Docs
You can run each submodule on it's own like this:
```bash
python[3] ksem.py
python[3] piko15.py
```

or for a full run with influxdb:
```bash
python[3] main.py
```

Based on:
- https://www.kostal-solar-electric.com/en-gb/products/accessories/-/media/document-library-folder---kse/2020/12/15/13/45/ksem_ba_en.pdf
- https://github.com/kilianknoll/kostal-ksem
- https://www.msxfaq.de/sonst/iot/kostal15.htm

## Disclaimer
Warning

Please note that any incorrect or careless usage of this module as well as errors in the implementation may harm your Smart Energy Manager !

Therefore, the author does not provide any guarantee or warranty concerning to correctness, functionality or performance and does not accept any liability for damage caused by this module, examples or mentioned information.

Thus, use it on your own risk!

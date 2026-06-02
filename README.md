# Computer Architecture Lab Manual Generator

Generates a PDF lab manual from Verilog HDL code and simulation waveform screenshots.

## Required File Structure

Each experiment folder must contain image pairs following this naming convention:

```
<folder>/
├── <NAME>_CODE.<ext>      # Verilog code screenshot
└── <NAME>_OUTPUT.<ext>    # Simulation waveform screenshot
```

Example (`ADDER/`):
```
ADDER/
├── HALF_ADDER_CODE.png
├── HALF_ADDER_OUTPUT.png
├── FULL_ADDER_CODE.png
└── FULL_ADDER_OUTPUT.png
```

Supported image formats: `.png`, `.jpeg`, `.jpg`. The script automatically pairs files by matching everything before `_CODE` and `_OUTPUT`.

## Experiments

| # | Experiment | Folder |
|---|---|---|
| 1 | Basic & Universal Logic Gates | `GATES/` |
| 2 | Half Adder | `ADDER/` |
| 3 | Full Adder | `ADDER/` |
| 4 | Half Subtractor | `SUBTRACTOR/` |
| 5 | Full Subtractor | `SUBTRACTOR/` |
| 6 | 2:1 Multiplexer | `MUX/` |
| 7 | 4:1 Multiplexer | `MUX/` |
| 8 | 8:1 Multiplexer | `MUX/` |
| 9 | 1:2 Demultiplexer | `DEMUX/` |
| 10 | 1:4 Demultiplexer | `DEMUX/` |
| 11 | 1:8 Demultiplexer | `DEMUX/` |

## Setup

```bash
git clone https://github.com/MRWICKJ/COMPUTER_ARCHITECTURE_WORKS.git
cd COMPUTER_ARCHITECTURE_WORKS
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Output: `Computer_Architecture_Lab_Manual.pdf`



## Adding Experiments

1. Create a subfolder (e.g., `ENCODER/`)
2. Add `XXX_CODE.png` and `XXX_OUTPUT.png` screenshots
3. Add the folder name to `folders` list and an objective to the `objectives` dict in `main.py`
4. Regenerate the PDF

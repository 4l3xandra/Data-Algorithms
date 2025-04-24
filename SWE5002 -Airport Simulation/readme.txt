# Airport Flight Request Simulation ✈️

This Python simulation models how a small airport handles flight operations using queue-based scheduling. It prioritizes emergency landings first, then regular landings, and finally takeoffs.

---

## Features

- 🧠 Intelligent flight queue system
- 🚨 Emergency landings override normal requests
- ⏱️ Realistic delays between control actions
- 📊 Live queue status logging
- 📝 Generates a `control_log.txt` for analysis/reporting

---

## How It Works

1. Random flight requests (landing, takeoff, emergency landing) are generated.
2. Requests are stored in separate lists.
3. The system processes:
   - All emergency landings first
   - Then normal landings
   - Then takeoffs (only when skies are clear)
4. All actions are printed and saved to a log file.

---

## Requirements

- Python 3.6+

No external libraries are needed.

---

## How to Run

```bash
python airport_simulation.py

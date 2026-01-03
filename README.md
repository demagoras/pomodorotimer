# Pomodoro Timer

A PyQt6-based Pomodoro timer with customizable work/break intervals.

## Features
- 25-minute work sessions with 5-minute breaks
- Editable timer with intuitive digit-only input
- Grace period between work and break
- Non-intrusive audio notifications
- Keyboard shortcuts (spacebar/Enter to start & resume) - **currently disabled**

## Installation

### Prerequisites
- Python 3.9+ (tested with Python 3.14.2)
- PyQt6

### Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/demagoras/pomodorotimer.git
   ```
2. **Open the project folder:**
   ```sh
   cd pomodorotimer
   ```
3. **(Optional but recommended) Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Run the application:**
   ```
   python app.py
   ```

## Known Issues
- Fast-clicking timer in edit mode can highlight text unexpectedly
- Resetting during grace and break periods crashes the program at a later stage

## Contributing
See [TODO.md](TODO.md) for planned features and improvements.

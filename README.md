# Beginning
## UI
- Small, always-on-top window
- Positioned in a screen corner
- Displays:
    - Task name (text)
    - Countdown timer (MM:SS)
## Timer behavior
- Pomodoro-style by default (e.g. 25 min work / 5 min break)
- Start / pause / reset
- Switches between “Work” and “Break”
- Optional sound or visual cue when time ends

# Basic architecture
Timer Logic
 ├── current_mode (work / break)
 ├── remaining_time
 ├── start()
 ├── pause()
 └── reset()

UI
 ├── Task name input/display
 ├── Timer label
 ├── Buttons
 └── Always-on-top behavior

 ## UI behavior tips
- Always-on-top window flag (most UI frameworks support this)
- Remove window decorations (optional)
- Allow dragging the window
- Use a large, readable font
- Color-code modes:
    - Work = red / orange
    - Break = green / blue

# Expansion ideas
- Task history
- Daily stats (time per task)
- Configurable durations
- Keyboard shortcuts
- Tray icon
- Multiple timers
- Auto-start next session

# High-level architecture
**Do NOT** dump everything into `renderer.js`.

```
main.js        → window management, OS stuff
preload.js    → safe bridge (contextBridge)
renderer/     → UI + timer logic
```
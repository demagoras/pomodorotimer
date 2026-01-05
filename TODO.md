# Pomodoro Timer

A PyQt6-based Pomodoro timer with customizable work/break intervals.

## In Progress
- [ ] Fix bug when resetting during grace or break periods (something with `self.topic_label.textChanged.disconnect()`)
  - `TypeError: disconnect() failed between 'textChanged' and all its connections`

## Backlog
- [ ] Modularize code structure
  - Separate edit mode handlers into own class/module
- [ ] Long break (15 min.) after 4 work sessions
- [ ] Auto-delete whole input on first click of edit mode
- [ ] System tray integration
- [ ] Desktop notifications for state transitioning

### Completed Column ✓
- [x] Prevent `if not self.parse_manual_input():` from running in `exit_edit_mode()` when not in focus mode
- [x] Disable text highlighting on fast-click 2026-01-05
- [x] Force valid time input (specifically when 00:00:00) 2026-01-05
- [x] Refactor `handle_transition()` 2026-01-03
- [x] Disable editing time when paused 2026-01-03
- [x] Use enum for work states 2026-01-03
- [x] Fix Enter key conflict with QLineEdit 2026-01-03
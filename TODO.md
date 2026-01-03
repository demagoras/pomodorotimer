# Pomodoro Timer

A PyQt6-based Pomodoro timer with customizable work/break intervals.

## In Progress
- [ ] Fix bug when resetting during grace or break periods (something with `self.topic_label.textChanged.disconnect()`)
  - `TypeError: disconnect() failed between 'textChanged' and all its connections`
- [ ] Force valid time input
  - Don't allow 00:00:00, require actual time value without merely falling back on the default time
- [ ] Disable text highlighting on fast-click
- [ ] Disable editing time when paused

## Backlog
- [ ] Modularize code structure
  - Separate edit mode handlers into own class/module
- [ ] Prevent `if not self.parse_manual_input():` from running in `exit_edit_mode()` when not in focus mode
  - Note that "focus mode" is triggered even by just clicking on the widget. Look into possibly bypassing this
  - Thus screen shakes even when not editing

### Completed Column ✓
- [x] Fix Enter key conflict with QLineEdit 2026-01-03
- [x] Use enum for work states 2026-01-03
- [x] Refactor `handle_transition()` 2026-01-03
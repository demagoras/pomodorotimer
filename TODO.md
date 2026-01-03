# Pomodoro Timer

A PyQt6-based Pomodoro timer with customizable work/break intervals.

## In Progress
- [ ] Use enum for work states
  - Replace `is_working` and `is_grace` booleans
  - Use `WorkState.WORKING`, `WorkState.GRACE`, `WorkState.BREAK`

## Backlog
- [ ] Refactor `handle_transition()`
  - Break into `start_work()`, `start_grace()`, `start_break()` methods
- [ ] Modularize code structure
  - Separate edit mode handlers into own class/module
- [ ] Force valid time input
  - Don't allow 00:00:00, require actual time value
  - Don't just fall back on default time value
- [ ] Disable text highlighting on fast-click
- [ ] Disable editing time when paused
- [ ] Prevent `if not self.parse_manual_input():` from running in `exit_edit_mode()` when not in focus mode
  - Focus mode means merely clicking on the widget, perhaps bypass this

### Completed Column ✓
- [x] Fix Enter key conflict with QLineEdit 2026-01-03
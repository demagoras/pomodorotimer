# Pomodoro Timer

A PyQt6-based Pomodoro timer with customizable work/break intervals.

## In Progress
- [ ] Fix Enter key conflict with QLineEdit #bug
  - Check if QLineEdit has focus before toggling timer

## Backlog
- [ ] Use enum for work states #refactor
  - Replace `is_working` and `is_grace` booleans
  - Use `WorkState.WORKING`, `WorkState.GRACE`, `WorkState.BREAK`
- [ ] Refactor `handle_transition()` #refactor
  - Break into `start_work()`, `start_grace()`, `start_break()` methods
- [ ] Modularize code structure #refactor
  - Separate edit mode handlers into own class/module
- [ ] Force valid time input #enhancement
  - Don't allow 00:00:00, require actual time value
  - Don't just fall back on default time value
- [ ] Disable text highlighting on fast-click #bug
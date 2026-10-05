# Website revision notes — v21

- Repaired Theoretical Market Framework feedback progress tracking.
- Either **Open discussion** or **No further feedback / Recorded: no further feedback** completes the related pillar.
- Each pillar contributes exactly 20%, regardless of repeated clicks or use of both actions.
- Progress now uses session-scoped shared state so it survives internal navigation, refreshes, and browser back/forward navigation during the same review visit.
- A fresh browsing session starts at 0%.
- Added pageshow/focus/visibility synchronization so the main progress bar refreshes when returning from pillar subpages.
- Preserved the 100% celebration and made it fire only on the first transition from below 100% to 100% in the current review session.

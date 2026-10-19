# Sheet

A side panel that slides from the right for details and quick edits without leaving a table: 480px wide (640px for forms), full height, `card` ground, `border` on its left edge, `shadow-md`, over a 40% scrim. Header: `title`, an `mono` ID line, a close button; body scrolls with `space-4` padding; footer actions as in Dialog. Sheets are for reading and light editing of one row; anything with more than ~8 fields becomes a page. The consumer provides header, body and actions. Escape closes; unsaved changes prompt a Dialog.

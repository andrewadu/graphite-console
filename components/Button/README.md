# Button

Actions in a console, sized for mouse and keyboard, never a pill. Four variants: primary (one per view), secondary, ghost (toolbars, table rows) and destructive. Heights 32px default and 28px small; label in `body-medium`; icon 16px with a `space-1` gap. The consumer provides the label, an optional leading icon and the handler; the system fixes padding (`space-2` by `space-3`), `radius-md`, the `ring` focus style and the disabled state (`muted` fill, `muted-foreground` text, no pointer). In dark, destructive text is `destructive-foreground` (ink) over `destructive`, not white.

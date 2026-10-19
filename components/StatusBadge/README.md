# StatusBadge

A small state label for tables, headers and detail panes: a status dot plus text, or a tinted chip. Five tones map to tokens: neutral (`muted` / `foreground`), success, warning, destructive, and info (`chart-2`). Text is `label` style, 12px, in `foreground` for the dot form; the tinted form uses the tone colour at 14% over the ground with the tone colour as text, except warning, whose text stays `foreground` because amber fails contrast. `radius-sm`, padding `space-1` by `space-2`, height 20px. The consumer provides the label and tone; it never invents a sixth tone.

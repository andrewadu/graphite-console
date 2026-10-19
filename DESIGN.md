# Graphite Console

A design system for backoffice consoles and system-admin tools: user management, audit logs, queues, configuration, dashboards. It starts from the **Graphite** theme of the Artifact Next.js + shadcn/ui admin kit and keeps that kit's token names, so a Next.js console built on shadcn/ui can adopt it by pasting `tokens.css` into `globals.css`.

Graphite is deliberately quiet. The whole chrome is grey; the single hue (a slate teal, `chart-2`) belongs to data, and red, green and amber belong to state. On an admin screen the thing that should pull the eye is the row that failed, not the button.

## Principles

**Data first, chrome second.** Backgrounds, cards, sidebar and primary are all greys within a narrow band. Anything coloured on screen means something: a status, a delta, a series.

**Borders, not shadows.** Surfaces are separated by `border` hairlines and one-step lightness changes (`background` → `card` → `secondary`). Shadow appears only on things that float (menus, dialogs).

**Dense but legible.** Base text is 14px/20px, tables can drop to 13px/18px, labels sit at 12px. Nothing goes below 12px and nothing in `muted-foreground` goes below 13px in long runs.

**Both themes, one file.** Every component renders in light and dark from the same markup; the themes swap only CSS variables. Dark is not an afterthought: admins run these consoles for hours, often at night.

**Keyboard is a first-class input.** Every interactive element shows the `ring` focus style (2px, 2px offset). Tables are navigable row by row; dialogs trap focus.

## Colour

| Token | Light | Dark | Role |
| --- | --- | --- | --- |
| `background` | `#f0f0f0` | `#1a1a1a` | page ground |
| `card` | `#f5f5f5` | `#202020` | panels, tiles, tables |
| `sidebar` | `#eaeaea` | `#1f1f1f` | navigation rail |
| `foreground` | `#333333` | `#d9d9d9` | ink |
| `muted-foreground` | `#666666` | `#808080` | secondary text |
| `primary` | `#606060` | `#a0a0a0` | the one emphasis grey |
| `border` | `#d0d0d0` | `#353535` | hairlines |
| `destructive` | `#cc3333` | `#e06666` | errors, destructive actions |
| `success` | green (lab) | green (lab) | healthy, completed |
| `warning` | amber (lab) | amber (lab) | pending, degraded |
| `chart-2` | `#476666` | `#7e9ca0` | the only hue: comparison series |

Rules that name tokens:

- Text is `foreground` on `background`, `card`, `secondary` or `sidebar`. Secondary text is `muted-foreground`, which clears 4.5:1 on all four grounds in both themes.
- `primary` is used for one filled button per view, the active nav item, checked controls and the focus `ring`. Two filled primary buttons side by side is a smell.
- Status colours appear as a dot plus a `foreground` label, or as a tint (colour at 12–15% over the ground) with the status colour as the text. `warning` is never body text: it fails contrast on both grounds.
- `destructive` buttons in dark use `destructive-foreground` (ink) rather than white, because white on `#e06666` fails.
- Charts use `chart-1` … `chart-5`; series differ by lightness, so a greyscale print still reads. `chart-2` is reserved for the comparison series (previous period) because it is the one series that must be told apart at a glance.

## Typography

Inter for the interface, Fira Code for data. Both are hosted faces (Google Fonts), so there are no font files in this system; the source kit loads Inter in its dark preset and Montserrat in its light one, and this system standardises on Inter for both since its narrower set width suits dense tables.

| Style | Size / line | Weight | Where |
| --- | --- | --- | --- |
| `display` | 24 / 32 | 600 | page title, stat-tile number |
| `title` | 16 / 24 | 500 | card and dialog headings |
| `body` | 14 / 20 | 400 | everything by default |
| `body-medium` | 14 / 20 | 500 | buttons, nav items, key cells |
| `small` | 13 / 18 | 400 | dense tables, helper text |
| `label` | 12 / 16 | 500 | column headers, form labels, badges |
| `mono` | 13 / 20 | 400 | IDs, amounts, keys, logs |

Use `font-variant-numeric: tabular-nums` on any column of numbers. Right-align amounts; left-align everything else.

## Spacing and shape

A 4px grid: `space-1` 4, `space-2` 8, `space-3` 12, `space-4` 16, `space-6` 24, `space-8` 32. Controls are 32px tall by default (`space-2` vertical padding around a 20px line), 28px in dense tables. Cards pad with `space-4` and sit `space-6` apart.

Radii are tight: `radius-md` (4px) on controls, `radius-lg` (6px) on cards, `radius-sm` (2px) on badges and checkboxes, `radius-full` only for avatars and status dots. No pill buttons.

## Iconography

Lucide icons at 16px inside controls and table cells, 20px in the sidebar and empty states, stroke 1.75 in `currentColor`. An icon never carries meaning alone in a table: pair it with text or a tooltip. Status dots are 8px circles in the status colour, vertically centred on the label's x-height.

## Components

The system ships guideline-and-preview cards for the pieces every console needs. Actions: `Button`, `Kbd`. Forms: `TextField`, `Textarea`, `FormControls` (checkbox, radio, switch, select), `Combobox`, `TagInput`, `DateRangePicker`, `FileUpload`, `SettingsRow`. Data display: `DataTable`, `FilterBar`, `Pagination`, `StatusBadge`, `StatTile`, `ChartCard`, `DescriptionList`, `Timeline`, `CodeBlock`, `Avatar`. Navigation: `SidebarNav`, `PageHeader` (with breadcrumb), `Tabs`, `Stepper`, `Accordion`. Overlays: `Dialog`, `Sheet`, `DropdownMenu`, `CommandPalette`, `NotificationPanel`, `Tooltip`, `Toast`. Feedback: `Alert`, `Banner`, `EmptyState`, `Skeleton`, `ProgressBar`. Pages: `LoginScreen` (sign-in and 2FA). The previews are plain HTML on the tokens, so they double as reference markup for a shadcn/ui implementation. Each card's README says what the consumer provides (labels, data, handlers) and what the system fixes (sizes, colours, states).

## Content

Write like a competent operator talking to another one. Labels are nouns (`Users`, `Audit log`), buttons are verbs (`Suspend user`, `Export CSV`), destructive buttons name the object (`Delete key`, never just `Delete`). Empty states say what is missing and what to do (`No failed jobs in the last 24 hours`). Timestamps show relative time with the absolute time in a tooltip. Numbers use thin-space or comma grouping and the user's locale.

## Source and status

Values were read from the live Graphite preset of the Artifact admin kit on 2026-10-15; names and values match that kit's CSS variables except `destructive-foreground` in dark (overridden for contrast) and the two shadow tokens (the kit defines shadow by parts; these are the composed values). Not yet in this system: the kit's full Tailwind colour scale, its chart category colours, iconography assets and a component bundle. Add a logo to `assets/Logos` when one exists; until then the name is set in plain type.

# Numerica — Design Reference

Source of truth: https://na-project-anaszarqawi.vercel.app/
Apply this aesthetic across **every page** of the project (Intro, Methods list, Method workspace, History, Saved, Settings).

## 1. Aesthetic Summary

A clean, **minimal, monospaced, paper-white** interface. No gradients, no glow,
no neon. Everything sits on a near-white canvas with very subtle borders and
a generous amount of negative space. The personality comes entirely from
**monospace typography** + **soft pill-shaped controls**.

Think: a math notebook rendered in code-editor type.

## 2. Color Tokens

Use OKLCH in `src/styles.css`. Replace the current indigo/violet palette.

### Light (default)
| Token | Value | Usage |
|---|---|---|
| `--background` | `oklch(0.985 0.002 260)` | App canvas (very light gray, almost white) |
| `--foreground` | `oklch(0.18 0.01 260)` | Primary text (near-black) |
| `--card` | `oklch(0.97 0.003 260)` | Pills, input backgrounds, list rows |
| `--card-foreground` | `oklch(0.18 0.01 260)` | Text on cards |
| `--muted` | `oklch(0.94 0.004 260)` | Hover states, secondary surfaces |
| `--muted-foreground` | `oklch(0.5 0.01 260)` | Labels, hints, footer text |
| `--border` | `oklch(0.9 0.004 260)` | Hairline dividers (1px) |
| `--input` | `oklch(0.97 0.003 260)` | Input/pill background |
| `--primary` | `oklch(0.22 0.01 260)` | Buttons, accent text (near-black) |
| `--primary-foreground` | `oklch(0.99 0 0)` | Text on primary |
| `--accent` | `oklch(0.94 0.004 260)` | Active toolbar icon background |
| `--ring` | `oklch(0.7 0.01 260)` | Focus ring (subtle gray) |

### Dark
| Token | Value |
|---|---|
| `--background` | `oklch(0.15 0.005 260)` |
| `--foreground` | `oklch(0.95 0.005 260)` |
| `--card` | `oklch(0.2 0.006 260)` |
| `--muted` | `oklch(0.23 0.006 260)` |
| `--muted-foreground` | `oklch(0.65 0.008 260)` |
| `--border` | `oklch(0.28 0.006 260)` |
| `--primary` | `oklch(0.95 0.005 260)` |
| `--primary-foreground` | `oklch(0.15 0.005 260)` |

**Remove**: `--gradient-primary`, `--gradient-hero`, `--gradient-card`,
`--shadow-glow`, `--violet`, `--glow`. Remove `body { background-image: var(--gradient-hero) }`.

## 3. Typography

- **All UI text uses monospace.** Set the body `font-family` to
  `"JetBrains Mono", "Fira Code", ui-monospace, monospace`.
- Headings = monospace, normal weight (400–500), letter-spacing slightly tight.
- Labels (`F(x)`, `Xl`, `Xu`, `ES`, `MAXi`) are **uppercase-style mono** in muted color.
- No serif fonts anywhere.
- Sizes: base 14–15px; section titles 18–20px; hero 28–32px.

## 4. Layout

- Centered single column, `max-width ≈ 960px`, with 16–24px horizontal padding.
- Header bar: small logo on the left, page title centered (often subtly faded /
  blurred-looking), icon toolbar on the right.
- Thin 1px divider under the header and above the footer.
- Footer: copyright on left, version chip in center, social icons on right —
  all in `--muted-foreground`.

## 5. Components

### Header
- Logo: small monogram, ~32px tall.
- Centered title: monospace, slightly washed out (e.g. `opacity-60`).
- Right toolbar: 5 icon buttons spaced `gap-2`:
  Settings (gear), History (clock), Saved (bookmark),
  Methods (`fx`), Theme toggle (sun/moon).
- Active icon = pill with `--accent` background (light gray rounded rect).
- Icon size: 18–20px, color `--muted-foreground`, hover → `--foreground`.

### Pills / Inputs / List rows  (THE signature element)
- Background: `--card`
- Border: none (or 1px `--border` on focus only)
- Radius: `rounded-full` for short controls (buttons, list rows, inputs of one line)
- Padding: `px-4 py-2.5`
- Text: monospace, `--foreground`
- Placeholder: `--muted-foreground`
- Focus: subtle `--ring` outline, no glow
- No drop shadows. No gradients.

### Buttons
- Same pill shape as inputs.
- Default: `--card` background, `--foreground` text, leading lucide icon (16px).
- Primary action ("Calculate"): same pill but slightly darker (`--muted`)
  and bold-weighted icon. Avoid colored buttons.
- Spacing between buttons: `gap-3`.

### Method list (Methods page)
- Section heading: `Chapter 1`, `Chapter 2` in monospace, with optional small
  dark "New" badge on the right.
- Each method = full-width pill row with the method name left-aligned in mono.
- Vertical gap between rows: 8–10px.
- Hover: row background shifts from `--card` to `--muted`.

### Test Me! / Saved / History rows
- Pill rows split: left = expression in mono, right = parameter chip
  (`xl: 0 | xu: 1 | es: 10`) in `--muted-foreground`.

### Tables (iteration results)
- Monospace, hairline borders only (`--border`), zero shadow.
- Header row uses `--muted` background, regular weight.
- Alternating row tint OFF — keep it flat.
- Numbers right-aligned.

### Plot
- White (or `--card`) background, 1px border, no glow.
- Axis lines and ticks in `--muted-foreground`.
- Function curve in `--foreground` (near-black) at 1.5px.
- Root marker: small filled circle in `--foreground`.
- No gradients under the curve.

## 6. Motion

- Almost none. Hover transitions on background-color only, 120ms ease.
- No scale / glow / shimmer effects.

## 7. Iconography

- Lucide React, stroke-width 1.75, size 16–20px depending on context.
- Icons inherit `currentColor` — never colored.

## 8. Do / Don't

✅ Monospace everywhere, pill-shaped controls, lots of whitespace, hairline borders.
❌ No indigo/violet, no gradient hero, no glow shadows, no serif, no sans-serif body, no colored buttons.

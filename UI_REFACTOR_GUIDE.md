# UI System Guide

## Purpose

This document defines the visual and interaction direction for the app.

The goal is to make the interface feel:
- minimalist
- polished
- technical
- modern
- calm
- premium

The app should not feel like a cluttered prototype, a gamer HUD, or a generic sci-fi dashboard. It should feel closer to a disciplined product experience: clean layout, strong hierarchy, careful spacing, subtle motion, and confident restraint.

The design direction should lean toward a modern tech product aesthetic inspired by the simplicity, clarity, and refinement often seen in high-end Apple- or Google-style interfaces, while still fitting the product's own identity.

---

## Core Design Principles

### 1. Simplicity over decoration
Do not add visual noise just because the subject matter is space or technology.

Avoid:
- excessive glow
- random gradients
- too many floating cards
- heavy borders everywhere
- overdone shadows
- busy backgrounds
- flashy animations that distract from use

Prefer:
- clean surfaces
- careful spacing
- limited accent usage
- restrained color
- elegant typography
- clear information grouping

The UI should feel intentionally reduced, not empty.

---

### 2. The product should feel advanced without looking chaotic
A technical product does not need to look crowded to feel powerful.

The interface should communicate sophistication through:
- precision
- consistency
- clean structure
- high-quality motion
- strong readability
- thoughtful component behavior

The app should feel like a premium modern tool, not a concept demo.

---

### 3. The main visualization is the hero
The central 3D or data visualization area is the primary experience.

UI should support it, not fight it.

That means:
- keep important content visible
- avoid blocking the center of the screen with large panels
- dock or collapse secondary controls
- only surface detail when it is useful
- reduce persistent clutter

Every UI element should justify the space it occupies.

---

### 4. Minimalist does not mean weak
Minimalism here should still feel sharp and technical.

That means:
- clear hierarchy
- well-defined surfaces
- precise alignment
- crisp controls
- intelligent density
- good information architecture

Do not confuse minimalism with oversized empty layouts or vague interfaces with hidden functionality.

---

### 5. Motion should be subtle, clean, and purposeful
Animation should improve clarity and polish.

Motion should:
- explain transitions
- confirm actions
- make state changes feel smooth
- improve perceived quality
- help the interface feel alive without becoming distracting

Avoid motion that feels bouncy, loud, delayed, exaggerated, or ornamental for its own sake.

---

## Visual Style Direction

## Overall Aesthetic

The visual tone should be:
- dark or neutral
- elegant
- precise
- crisp
- modern
- refined
- slightly futuristic, but grounded

The interface should feel like a premium software product first, and a space app second.

Good reference qualities to aim for:
- clean Apple-like restraint
- organized Google-like usability
- premium product-level spacing and surface design
- controlled, tasteful motion
- minimal but strong component systems

Do not directly imitate another company's branding. Instead, capture the qualities:
- clarity
- discipline
- restraint
- polish
- consistency

---

## Color Principles

### Base palette
Use a restrained palette built around:
- dark neutrals
- soft grays
- muted cool tones
- one controlled accent color

The palette should support readability first.

### Accent usage
Accent colors should be used intentionally:
- active states
- focus states
- selected objects
- important metrics
- primary actions

Avoid using bright accents everywhere. If everything is highlighted, nothing is important.

### Contrast
Maintain strong enough contrast for readability without making the interface harsh.

Avoid:
- washed out low-contrast text
- neon-on-black everywhere
- over-bright highlights
- muddy gray-on-gray text

---

## Typography

Typography should feel modern, clean, and structured.

### Rules
- use a clean sans-serif system
- establish obvious hierarchy
- avoid too many font sizes
- avoid overly small labels
- use spacing and weight more than decoration

### Tone
Text should feel:
- concise
- product-like
- confident
- readable

### Hierarchy
At minimum, define consistent styles for:
- page/app title
- panel title
- section label
- body text
- metadata / secondary text
- button labels
- small helper text

Typography should help the interface feel premium more than effects do.

---

## Layout Principles

### 1. Stable structure
The layout should feel anchored and predictable.

Recommended shell:
- top bar for global search, mode switching, status
- left rail for navigation and major tools
- right panel for contextual details
- bottom strip for timeline/time controls when relevant
- center reserved for the main visualization

Avoid random floating placement unless it clearly improves usability.

---

### 2. Protect the main view
Panels should not constantly cover the core content.

Rules:
- avoid large default-open overlays in the center
- use collapsible side panels
- minimize nonessential UI
- keep the main camera/view unobstructed by default

---

### 3. Clear hierarchy of surfaces
Not every surface should have equal visual weight.

Use a hierarchy such as:
- primary surface: main content
- secondary surface: persistent controls
- tertiary surface: contextual details
- transient surface: popovers, tooltips, dialogs

This keeps the interface calm and understandable.

---

### 4. Spacing is part of the design
Spacing should make the product feel expensive.

Use consistent spacing for:
- panel padding
- gaps between controls
- section separation
- toolbar groups
- text blocks

Avoid cramped stacking and inconsistent spacing rhythms.

---

## Component Behavior

## Panels

Panels should be:
- docked or intentionally placed
- collapsible
- scrollable when needed
- predictable in behavior
- visually consistent

Each panel should have a clear purpose.

Do not create many competing floating windows.

### Panel rules
- every panel needs a clear title
- every panel needs an obvious close/collapse affordance
- every panel should have sensible width limits
- large panels should not stack in ways that hide content
- contextual panels should open only when relevant

---

## Toggles and Controls

Controls should be easy to understand at a glance.

Prefer:
- segmented controls
- tab groups
- compact toggle rows
- icon + label combinations
- clear selected states

Avoid:
- mystery icon-only clusters
- scattered toggles across many corners
- inconsistent switch styles
- controls with unclear consequences

---

## Search

Search should be:
- easy to find
- visually prominent enough to matter
- not oversized
- consistent with the rest of the UI

It should feel like part of the product shell, not an afterthought.

---

## Detail Views

When an object is selected, details should appear in a consistent place.

Detail panels should:
- prioritize the most useful information first
- group metadata logically
- support scrolling
- avoid overly dense walls of text
- make actions easy to find

---

## Animation and Motion

## Motion philosophy

Animation should be subtle, clean, and fast.

The motion language should feel:
- refined
- smooth
- controlled
- modern
- understated

Think product polish, not spectacle.

---

## What motion should do

Use animation to:
- ease panel opening and closing
- transition between states
- smooth layout changes
- confirm selection
- guide attention gently
- make camera/view changes feel intentional

Motion should make the interface easier to understand.

---

## What motion should not do

Do not use:
- large bouncy spring animations
- dramatic overshoot
- slow cinematic delays for ordinary UI actions
- constant pulsing elements
- flashing highlights
- overly elastic menus
- decorative movement with no UX value

If an animation draws more attention than the content, it is too much.

---

## Motion guidelines

### Timing
- keep most UI motion fast and responsive
- transitions should feel immediate, not sluggish
- use slightly slower timing only for larger scene or view transitions

### Easing
Prefer smooth, subtle easing.
Avoid playful or exaggerated easing for core UI.

### Common motion patterns
Use subtle animation for:
- panel slide-in/slide-out
- fade + slight translate for popovers
- tab/content transitions
- hover feedback
- button press states
- list reordering or filter changes
- detail panel state changes

### Camera and scene transitions
Camera transitions should feel elegant and controlled.
Do not snap abruptly unless the user explicitly requests it.

---

## Visual Effects

Effects should be restrained.

Acceptable effects:
- soft blur in moderation
- subtle glass treatment where useful
- gentle shadows
- faint borders
- controlled highlights
- restrained glow for selected space objects or key data

Avoid:
- thick glows around everything
- overpowered glassmorphism
- heavy blur on all panels
- multiple layered shadows
- noisy depth effects

Effects should enhance structure, not replace it.

---

## Responsiveness

This UI must remain usable on smaller laptop screens, not just large monitors.

### Requirements
- panels should resize intelligently
- content should not overflow off-screen
- internal panel scrolling must work
- important controls should remain reachable
- the interface should degrade gracefully at smaller widths

### Smaller-screen behavior
On smaller screens:
- collapse secondary panels sooner
- reduce persistent surface count
- prioritize the main view
- move lower-priority controls into tabs, drawers, or menus

---

## Interaction Standards

### Hover states
Hover states should be subtle and informative, not flashy.

### Focus states
Keyboard and focus states should be visible and clean.

### Active states
Selection and active states must be obvious.

### Loading states
Loading states should feel polished and calm, not broken or empty.

### Error states
Error states should be readable, compact, and non-destructive to layout.

### Empty states
Empty states should still look intentional and designed.

---

## What to Avoid

Do not introduce:
- cluttered sci-fi HUD styling
- giant glowing borders
- random animations
- overlapping windows by default
- too many simultaneous panels
- inconsistent component styles
- multiple competing accent colors
- weak text contrast
- cramped information blocks
- controls placed without layout logic

---

## Refactor Priorities

### Priority 1
- fix overlapping UI
- protect the main visualization area
- create a stable layout shell
- improve panel/toggle behavior

### Priority 2
- establish a coherent minimalist visual system
- standardize spacing, typography, and controls
- improve search, filters, and detail panel layout

### Priority 3
- add subtle, premium motion
- improve transitions and visual polish
- refine responsive behavior

---

## Implementation Guidance

When making UI changes:

1. simplify before adding
2. remove weak UI instead of stacking more on top
3. use consistent component patterns
4. preserve clarity over visual novelty
5. keep motion subtle and purposeful
6. maintain a premium minimalist style throughout

Every new UI choice should satisfy this question:

Does this make the interface clearer, calmer, and more polished?

If not, it probably should not be added.

---

## Definition of Done

The UI direction is successful when:
- the interface feels clean and modern
- the product looks premium without being loud
- the main view remains unobstructed
- panel behavior is predictable
- controls are easy to find and understand
- typography and spacing feel intentional
- motion feels subtle and refined
- the overall experience feels closer to a disciplined modern product than a messy prototype
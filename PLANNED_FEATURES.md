# Planned Features — Not Started

Logged 2026-09-16. Nothing here has been built yet — for terminal Claude to plan and implement.

---

## 1. Intro logo animation (splash video)
- 6-second logo animation plays on first visit, then transitions to the landing page
- Assets ready: 9:16 (portrait/mobile) and 16:9 (landscape/desktop) versions
- Requirements:
  - Play once only (gate with `sessionStorage` or `localStorage`, not on every page load)
  - Must have a visible "Skip" button
  - Respect `prefers-reduced-motion` (skip animation entirely for those users)
  - Video must be muted to autoplay reliably across browsers
  - Pick aspect ratio by viewport orientation, not device type
  - Keep file size small (compressed mp4/webm, target <2-3MB) — a heavy intro video will hurt LCP/Core Web Vitals and SEO if not handled carefully

## 2. Leadership page — image section height
- Current image container is cutting off uploaded leadership photos
- Increase height / fix `object-fit`/`aspect-ratio` so images aren't cropped

## 3. Branches section — drill-down hierarchy
- Restructure from flat list to: Continent → Country → Branches
- Within a country, split further into "places with regions" vs "places without regions" so users don't have to search blindly
- Applies to all continents, not just Africa/Ghana
- Note: this is the biggest item — needs a data model change (Branch needs continent/country/region structure), migration of existing branch data, admin updates, and multi-level frontend navigation (breadcrumbs). Should be scoped as its own phase with a schema plan before frontend work starts.

### Phase 2 (visual upgrade, after schema/data model is done): decorative rotating globe
- Globe is purely decorative/reactive — NOT clickable itself. All selection happens via real buttons/list items (continent buttons, then a country list). This avoids raycasting/hit-testing on 3D geometry entirely.
- Library: lightweight canvas dot-matrix globe (e.g. `cobe`, ~5KB) — NOT a full WebGL polygon-rendering globe (`react-globe.gl`/three.js, ~500KB+). No country border/outline data needed.
- Country selection is shown via a **pin marker + pulsing glow** at the country's lat/lng, not a full country-shape highlight. Rationale (compared side by side): a pin needs only one coordinate per country (cheap, easy to maintain when new branches/countries are added), vs. full outline highlighting which needs a GeoJSON/TopoJSON boundary dataset plus fragile name-matching between the DB's country field and the dataset (e.g. "USA" vs "United States of America"). Pin gets ~80% of the visual payoff for a fraction of the cost/risk, and fits the fact that selection is already list-driven, not exploratory map-clicking.
- No second "flat map" needed anywhere — country/branch level is a normal list/grid with breadcrumbs (Continent → Country → Branches), same as any drill-down UI. The globe never needs to "become" a flat map.

**Animation choreography:**
1. **Idle**: globe gently auto-rotates (screensaver-style) beside/behind the continent buttons; nothing selected yet.
2. **Continent clicked** (e.g. Africa): button gets active state instantly. Globe stops idle rotation and eases (`easeInOutCubic`, ~1–1.5s) until Africa is centered facing the viewer. Optional subtle glow/tint wash over the landmass once centered. Country list cross-fades in below/beside the globe, staggered ~40ms per item.
3. **Country clicked** (e.g. Ghana): globe does NOT re-rotate or zoom — already facing the right continent, that's enough context. A pin scales in with slight spring overshoot (`0 → 1.15 → 1`, ~400ms) at Ghana's coordinates, with a looping pulse/ripple (Google-Maps-ping style). A small label fades in near the pin ("Ghana — 3 branches"), positioned to avoid clipping off the globe edge. Branch list panel (Accra, Kumasi, etc.) slides/fades in with the same staggered treatment.
4. **Different country, same continent** (e.g. Nigeria): old pin fades/shrinks out (~150ms) while new pin animates in — no re-rotation.
5. **Different continent** (e.g. Asia): pin/label fade out first (~150ms), then globe rotates to the new continent, then country list repopulates.
- **Timing hierarchy**: rotation = the "big" motion (continent switches, ~1–1.5s, deliberate), pin drop = the "small" motion (country switches, ~300–400ms, snappy). Keeping these visually distinct in weight is what avoids the interaction feeling janky/uniform.
- **Perf guardrails**: code-split/lazy-load the globe component so it only loads when the branches section scrolls into view — must never block initial page load/LCP.
- **Open question to resolve before building**: mobile/small-screen behavior — whether rotation still makes sense at small sizes or the globe should be simplified/half-globe framing on mobile.

## 4. Main branches section — horizontal scrolling country bar
- Decorative horizontal scroll/ticker of countries for an "international" feel
- Suggestion: once #3 exists, source this list from actual branch data instead of a hardcoded list so it doesn't drift out of sync

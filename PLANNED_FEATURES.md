# Planned Features — Not Started

Logged 2026-09-16. Nothing here has been built yet — for terminal Claude to plan and implement.

---

## 1. Intro logo animation (splash video) — DONE
- 6-second logo animation plays on first visit, then transitions to the landing page
- Assets ready: 9:16 (portrait/mobile) and 16:9 (landscape/desktop) versions
- Requirements:
  - Play once only (gate with `sessionStorage` or `localStorage`, not on every page load)
  - Must have a visible "Skip" button
  - Respect `prefers-reduced-motion` (skip animation entirely for those users)
  - Video must be muted to autoplay reliably across browsers
  - Pick aspect ratio by viewport orientation, not device type
  - Keep file size small (compressed mp4/webm, target <2-3MB) — a heavy intro video will hurt LCP/Core Web Vitals and SEO if not handled carefully

## 2. Leadership page — image section height — DONE
- Current image container is cutting off uploaded leadership photos
- Increase height / fix `object-fit`/`aspect-ratio` so images aren't cropped

## 3. Branches section — drill-down hierarchy

### Phase 1 — DONE
- Restructured from flat list to: Continent → Country → Region (optional) → Branches
- Ghana seeded with 3 real regions (Greater Accra, Ashanti, Western), all editable in Django admin
- New `Country`/`Region` models, `Branch.country`/`Branch.region` FKs (migrations 0017-0021)
- New `CountryViewSet`/`RegionViewSet` endpoints (`/api/countries/`, `/api/regions/`) with `?continent=`/`?country=` filters and annotated `branch_count`/`has_regions`
- `BranchViewSet` extended with `?continent=`/`?country=`/`?region=` filters
- Frontend `/branches` rewritten as a URL-param-driven drill-down (`ContinentGrid` → `CountryList` → `RegionOrBranchList`) with breadcrumbs; Main Branch stays pinned at top always
- All 7 continents always shown, even with zero branches
- Backend tests added for hierarchy filtering (14 new tests, all passing in isolation)

### Phase 2 — DONE: decorative rotating globe
- Built with `cobe` v2 (canvas/WebGL, imperative `.update()` API driven by our own `requestAnimationFrame` loop)
- `Country` model got auto-populated `latitude`/`longitude` (migrations 0022-0023) via a `pre_save` signal + a static offline reference dataset (`api/country_coordinates.py`, ~195 countries, commonly-used names incl. Taiwan/Kosovo/Western Sahara). `Country.name` is now a `choices` dropdown in admin — no manual coordinate entry, ever, and no typo risk.
- Frontend: `BranchesGlobe.tsx` (canvas + rotation/pin animation), lazy-loaded via `next/dynamic` + a new `useInView` IntersectionObserver hook so the `cobe` chunk never loads until the globe scrolls into view
- Idle auto-rotation → eased ~1.2s rotation to continent centroid (shortest-path, ease-in-out cubic) → pulsing gold pin + name badge on country selection (spring scale-in, no re-rotation) → crossfade on country switch → fade-then-rotate on continent switch
- Antarctica rotates to a polar view (no pin) for consistency with the penguin easter egg
- Placed as a full-width navy band between the hero header and the continent picker on `/branches`

### Phase 3 — DONE: Region became fully auto-derived (no manual creation)
- `Region` is no longer manually created anywhere — removed entirely from the Django admin sidebar (no standalone section, not even read-only)
- New `api/region_data.py`: static offline dataset of every country's real first-level administrative divisions (states/provinces/etc.), mirroring the same country keys as `country_coordinates.py`. Empty list for genuine city-states/micro-nations (Monaco, Vatican City) and Western Sahara (disputed territory, no neutral list to assign)
- New `post_save` signal on `Country` (`api/signals.py`) auto-creates all of that country's real `Region` rows the moment it's saved — runs on every save (idempotent via `get_or_create`), so expanding `region_data.py` later just needs a re-save to backfill, no migration required
- Migration `0024` backfilled all pre-existing countries (Ghana went from 3 to its full 16 real regions, with zero disruption to the 3 existing branches' FK links — same region IDs preserved)
- `BranchAdmin`'s Region field is now a plain dependent dropdown (no new package): picking a Country live-filters the Region options to just that country's real regions, via a small custom AJAX endpoint (`api/static/admin/js/branch_region_filter.js`) — no manual region typing anywhere, ever
- Sensitive/disputed subdivisions (e.g. Crimea) follow the same "commonly recognized, not disputed annexations" principle already used for country naming
- No frontend or API changes needed — the existing hierarchy endpoints/components already worked generically off real `Region` rows regardless of how they got created

### Original Phase 2 planning notes (superseded by the above, kept for history):
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

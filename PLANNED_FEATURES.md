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

## 4. Main branches section — horizontal scrolling country bar
- Decorative horizontal scroll/ticker of countries for an "international" feel
- Suggestion: once #3 exists, source this list from actual branch data instead of a hardcoded list so it doesn't drift out of sync

# Handoff: TGA Church — Home Page Redesign

## Overview
Redesign of the TGA Church home page to move from a generic Bootstrap-style layout to a premium, editorial, modern design rooted in the TGA brand (white / gold / blue). The ivory/champagne base tones down the previous "all white" feel, navy + gold carry the brand identity, and the events/sermons sections use a 6-item peek carousel (3 visible, middle card enlarged) instead of the static 3-card grid.

## About the Design Files
The file in this bundle — `TGA Home.html` — is a **design reference** created as a static HTML prototype. It shows the intended look, spacing, typography, motion and interactions of the new home page.

**It is NOT production code to copy directly.** Your task is to **recreate this design inside the existing Next.js 14 frontend** (see `frontend/` in the project root), reusing the current component structure, React Query hooks, TypeScript types, and Tailwind setup. Do not replace the frontend folder.

## Fidelity
**High-fidelity.** Colors, typography, spacing, shadows, and motion in the HTML are intentional and should be matched closely. Where the HTML uses placeholder images, wire up the real data from the existing hooks (`useBanners`, `useChurchInfo`, `useHeadPastor`, `useFeaturedEvents`, `useFeaturedSermons`, `useTestimonies`).

## Target Codebase
- **Framework:** Next.js 14 (app router), TypeScript, Tailwind CSS
- **Data:** React Query + Axios (`@tanstack/react-query`, already wired via `QueryProvider`)
- **Forms:** `react-hook-form` + `zod`
- **Icons:** `lucide-react`
- **Animation:** `framer-motion` available
- **Carousel:** `embla-carousel-react` + `embla-carousel-autoplay` already installed (use these; don't hand-roll)

## Files to Modify (touch list)
```
frontend/
├── tailwind.config.ts                         ← update color tokens + fonts
├── src/app/layout.tsx                         ← add Google Font imports
├── src/app/globals.css                        ← base background + font-family
└── src/components/
    ├── layout/Navbar.tsx                      ← restyle, gold hover underline
    ├── layout/Footer.tsx                      ← restyle to dark navy, 4-col
    └── home/
        ├── HeroBanner.tsx                     ← split-layout, scripture card
        ├── ChurchInfoSection.tsx              ← dark navy service times card
        ├── HeadPastorSection.tsx              ← 4:5 portrait, editorial bio
        ├── FeaturedEvents.tsx                 ← peek carousel (6 items, 3 visible)
        ├── FeaturedSermons.tsx                ← peek carousel on dark bg
        ├── TestimonialsCarousel.tsx           ← oversized italic pull-quote
        └── CTASection.tsx                     ← "Get Involved" 3-card, middle featured
```

Do **not** touch data hooks, types, or api layer — they're correct.

---

## Design Tokens

Update `tailwind.config.ts` to use these (keep old keys as aliases if something still references them, or rename globally):

```ts
colors: {
  // brand
  navy:       "#0b1e3f",
  "navy-2":   "#152a52",
  "navy-ink": "#0a1530",
  gold:       "#c9a24a",
  "gold-2":   "#b28a30",
  "gold-soft":"#e6cf91",

  // surfaces (tones down the old "all white")
  bg:         "#f1ebde",   // warm champagne ivory — page background
  "bg-2":     "#e9e1cf",
  paper:      "#f6efe0",   // card cream

  // text
  ink:        "#1a1a1a",
  muted:      "#6b6458",

  // legacy aliases (optional, for pages not yet migrated)
  primary:    "#0b1e3f",   // was #1E3A8A
  accent:     "#c9a24a",   // was #F59E0B
  dark:       "#0a1530",
  light:      "#f1ebde",
  "text-main":"#1a1a1a",
},
fontFamily: {
  display: ['Fraunces', 'serif'],
  sans:    ['Inter', 'sans-serif'],
  mono:    ['"JetBrains Mono"', 'monospace'],
},
```

Add to `src/app/layout.tsx` (in `<head>` or via `next/font`):

```
Fraunces (wght 300..700, italic, optical size 9..144)
Inter (wght 300..700)
JetBrains Mono (wght 400..500)
```

### Typography scale
- **Display (hero h1):** Fraunces 400, clamp(48px, 6.6vw, 92px), letter-spacing -0.02em, line-height 1.02
- **Display (section h2):** Fraunces 400, clamp(36px, 4.6vw, 64px)
- **Eyebrow:** JetBrains Mono 400, 11px, uppercase, letter-spacing 0.22em, color gold-2
- **Body:** Inter 400, 16px, line-height 1.75, color #3d3a32
- **Small/meta:** Inter 400, 13px, color muted

### Spacing / radii
- Section vertical padding: 80–100px desktop
- Card radius: 3px (intentionally small — feels editorial, not playful)
- Hero image radius: `3px 3px 120px 3px` (asymmetric, soft bottom-right)
- Button radius: 999px (pill)

### Shadows
- Card lift (featured center card): `0 40px 60px -30px rgba(11,30,63,.35)`
- Hero image: `0 40px 80px -30px rgba(11,30,63,.5)`

---

## Screens

### Home Page (`src/app/page.tsx`)
Same component order, restyled sections:

1. **HeroBanner** — see below
2. **ChurchInfoSection** — Welcome + Service Times
3. **HeadPastorSection** — Portrait + bio
4. **FeaturedEvents** — Peek carousel
5. **FeaturedSermons** — Peek carousel (dark bg)
6. **TestimonialsCarousel** — Pull-quote
7. **CTASection** — Get Involved

### Component specs

#### Navbar (`layout/Navbar.tsx`)
- Sticky, height 72px
- Background: `rgba(241,235,222,0.78)` with `backdrop-blur-[10px]`
- Border-bottom: 1px solid `rgba(11,30,63,0.12)`
- Logo: navy circle mark with gold "T", "TGA·Church" in Fraunces 21px
- Links: Inter 13.5px weight-500, active has gold underline (1px, positioned 2px from bottom)
- Give button: pill, `bg-navy text-white`, hover `bg-gold text-navy`

#### HeroBanner (`home/HeroBanner.tsx`)
- Two-column grid: `1.05fr 0.95fr`, gap 60px, min-height 640px
- **Left:** eyebrow "Welcome to TGA" → h1 with `<em>` italic gold second phrase → 17px lede (max 520px) → two CTAs (Plan a visit primary navy, Watch latest sermon ghost) → stats row (3 columns: Branches / Weekly worshippers / Est. year) divided by 1px top border
- **Right:** asymmetric image card with corners `3px 3px 160px 3px`, dark overlay, pagination dots on right edge (vertical, 6×22px, active is gold 6×36px)
- **Scripture overlay** (bottom-left of image, overlapping): cream card 320px wide, eyebrow "Today's Word" in gold, italic Fraunces quote, mono reference "Ephesians 2 : 8"
- Banner data from `useBanners()` — rotate every 5s, keep that logic from existing component

#### ChurchInfoSection (`home/ChurchInfoSection.tsx`)
- Two-column: welcome copy left, service-times card right
- **Left:** eyebrow "01 — Welcome" with 28px gold bar prefix, display h2 with italic emphasis word, body copy, signature block ("Pastor John Doe" in Fraunces italic + "Senior Pastor" in mono small)
- **Right:** full navy card (`bg-navy text-[#e9dfc6]`, rounded 3px, padding 38px 36px). Gold eyebrow "Service Times", white Fraunces 32px heading "Join us this week.", list where each row is: mono day tag (gold, 54px min-width) + Fraunces time + meta-right service name. 1px white/10 separator between rows. Decorative gold radial glow top-right.

#### HeadPastorSection (`home/HeadPastorSection.tsx`)
- Two-column: portrait left (1fr), bio right (1.1fr)
- **Portrait:** aspect-ratio 4/5, radius 3px. Bottom-left overlay with Fraunces 28px name + mono gold uppercase role. Top-right: gold mono "02"
- **Right:** eyebrow kicker → display h2 with italic emphasis → mono uppercase role line → 16px body → social links as 42px circular outlined pills (hover inverts to navy bg + gold text)

#### FeaturedEvents / FeaturedSermons (`home/FeaturedEvents.tsx`, `home/FeaturedSermons.tsx`)

**Use Embla Carousel** (`embla-carousel-react`) — already installed.

- 6 cards total, 3 visible per page (2 pages: 01/02)
- **Middle card (index 1 of visible 3) is larger:** flex-basis ~36%, sides ~30%
- Middle lifts `translateY(-18px)`, has cream-gold background (`#fff8e8`) and shadow
- Sides at `scale(0.94)` opacity `0.78`
- Transition 0.55s `cubic-bezier(.22,.8,.3,1)`

**Card content:**
- **Event card:** 4:3 image placeholder with date badge (top-left, cream background, Fraunces day + mono month). Body: gold eyebrow category, Fraunces 22px (26px on center) title, meta row with location + time separated by 1px top border
- **Sermon card:** 4:3 image with play button top-right (44px glass circle) + duration chip bottom-right (mono, navy/70 bg). Body identical to event.

**Controls** (section header, right side):
- Counter `01 / 02` in mono
- Prev/Next: 48px circle buttons, outlined 1px hairline, hover → navy bg + gold arrow
- Progress bar below footer: 1px hairline, gold 3px indicator grows with page

**Dark variant** for sermons: whole section `bg-navy`, card bg `#0f2349`, center card `#152c57`, white text.

#### TestimonialsCarousel (`home/TestimonialsCarousel.tsx`)
- Centered, max-width 840px
- Oversized gold `"` (120px, line-height 0.6)
- Fraunces italic 300 weight, clamp(26px, 3.4vw, 42px), line-height 1.4
- 52px avatar circle with gold border
- Name Fraunces 18px + location mono 12px
- Dots: 6×6px circle, active is `24×6px gold bar`
- Prev/next same 48px circle buttons as carousels

#### CTASection (`home/CTASection.tsx`)
- Centered heading + eyebrow + subtext
- 3-col grid, 24px gap, min-height 300px cards
- Each card: `num` (mono gold "01/02/03"), Fraunces 36px heading, body, arrow CTA at bottom
- **Middle card is pre-featured:** `bg-navy text-white`, num + CTA in gold. Hover inverts to gold bg + navy text
- Side cards: paper bg, hover → navy bg + white text (gold accents)

#### Footer (`layout/Footer.tsx`)
- Bg `navy-ink` (`#0a1530`)
- Top section: 4-column grid `1.4fr 1fr 1fr 1fr`, 40px gap, bottom border `rgba(255,255,255,0.08)`
- Column headers: mono gold "DISCOVER / GROW / CONTACT"
- Socials: 38px circle, 1px border, mono text "yt / fb / ig / tw / wa / tt"
- Bottom: mono 11px, "© 2026 TGA CHURCH" left, "BUILT ON GRACE" right

---

## Interactions & Behavior

- **Hero dots / banner rotation:** keep existing 5s interval logic from `HeroBanner.tsx`; restyle dots only
- **Carousel:** prev/next moves by a full page of 3 cards; keyboard arrows optional but nice. Wrap around (last page → first)
- **Hover states:** all links should have a 200ms transition. Buttons translate arrow +3px on hover
- **Motion:** consider `framer-motion` scroll-reveal (`whileInView`) for section entries — subtle fade + 12px y-offset, 0.5s

## Responsive rules
- `max-width: 1100px` — all two-column grids collapse to single column (50px gap). Nav links hide, hamburger visible (implement per existing pattern).
- `max-width: 780px` — carousel shifts to 1-up (80% card width), center card effect disabled, footer 1-col.

## State Management
No new state. Reuse:
- `useBanners()` — hero
- `useChurchInfo()` — welcome text + service times
- `useHeadPastor()` — pastor section
- `useFeaturedEvents()` + `useFeaturedSermons()` — carousels (slice to 6 instead of 3)
- `useTestimonies()` — quote section

If `useFeaturedEvents()` currently returns only 3, either bump the backend limit to 6 or add a new hook `useHomeEvents(6)`.

## Assets
- Placeholder images stay as placeholders until real ones are uploaded to the CMS — the existing `getImageUrl()` util handles fallbacks
- No new icons needed beyond lucide-react set already in use (`ArrowRight`, `Clock`, `Play`, `Calendar`, `MapPin`, `Heart`, `MessageCircle`, `ChevronLeft`, `ChevronRight`, `Quote`)

## Files
- `TGA Home.html` — the primary design reference. Open in a browser and inspect alongside the codebase while implementing.

## Acceptance checklist
- [ ] Tailwind tokens updated; fonts loaded
- [ ] Home page uses warm ivory background, not pure white
- [ ] Hero: split layout with scripture card overlap on image
- [ ] Service times: dark navy card with gold accents
- [ ] Pastor: 4:5 portrait with inline name tag
- [ ] Events carousel: 6 items, 3 visible, middle is clearly larger + lifted
- [ ] Sermons carousel: same mechanic, on navy background
- [ ] Testimonies: oversized italic pull-quote, no card
- [ ] CTA: 3 cards, middle is pre-featured (navy)
- [ ] Footer: dark navy, 4-col, mono eyebrows
- [ ] All existing data hooks still wired; no regression in search/filter on other pages
- [ ] Responsive at 1100px and 780px breakpoints

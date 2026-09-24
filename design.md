# UI/UX & Visual Design System
## PhD Professor Review & Cold Outreach Intelligence CRM

---

### 1. UI/UX

- **Clean and Intuitive Interface**:
  - High-density, professional academic aesthetic that avoids cluttered visuals while displaying all relevant research and outreach metrics.
  - Information hierarchy centered on the professor dossier and email composition workflow.
- **Consistent User Experience**:
  - Predictable placement of primary action buttons (e.g., "Add Professor", "Generate AI Draft", "Send Email").
  - Unified modal patterns for paper reviews, settings, and confirmations.
- **Mobile-First Approach**:
  - Responsive layouts using Tailwind CSS flex and grid utilities.
  - Collapsible sidebar navigation that transforms into a smooth drawer overlay on mobile screens.
  - Compact cards replacing wide data tables on small viewports.
- **Easy Navigation and Accessibility**:
  - High color contrast meeting WCAG AA standards.
  - Full keyboard accessibility for form inputs and modal closures (`Esc`).
  - Clear visual focus rings on all interactive elements.
- **Component Reuse and Consistency**:
  - Centralized component library (`Button`, `Badge`, `Modal`, `InputField`, `Card`, `StatusPill`).
  - Standardized state indicators (loading spinners, empty states, skeleton placeholders).

---

### 2. COLOR & THEME

#### 2.1 Color Palette
- **Primary Color**: Deep Academic Indigo (`#4338CA` / `indigo-700`) — represents scholarly authority, trust, and focus.
- **Secondary Color**: Slate Blue (`#6366F1` / `indigo-500`) — used for active tabs, secondary buttons, and highlighted selections.
- **Accent Color**: Vivid Violet / Purple (`#8B5CF6` / `violet-500`) — used exclusively for AI-powered actions (e.g., "Gemini AI Draft", "Synthesize Papers").

#### 2.2 Background & Surface Colors
- **Light Mode**:
  - Background: Crisp off-white (`#F8FAFC` / `slate-50`).
  - Surface Cards: Pure white (`#FFFFFF`) with subtle border (`#E2E8F0` / `slate-200`) and soft elevation shadow (`shadow-sm`).
- **Dark Mode**:
  - Background: Deep Obsidian (`#0F172A` / `slate-900`).
  - Surface Cards: Charcoal Slate (`#1E293B` / `slate-800`) with refined border (`#334155` / `slate-700`).

#### 2.3 Text Colors
- **Light Mode**:
  - Primary Text: Deep Charcoal (`#0F172A` / `slate-900`).
  - Muted Text: Slate Grey (`#64748B` / `slate-500`).
- **Dark Mode**:
  - Primary Text: Bright White (`#F8FAFC` / `slate-50`).
  - Muted Text: Soft Muted Slate (`#94A3B8` / `slate-400`).

#### 2.4 Semantic Status Colors
- **Success (Sent / Accepted / Replied)**: Emerald Green (`#10B981` / `emerald-500`).
- **Warning (Follow-Up Due / Queued)**: Amber Orange (`#F59E0B` / `amber-500`).
- **Error (Failed Send / Rejected)**: Rose Red (`#EF4444` / `rose-500`).
- **Informational (Reviewing / Identified)**: Sky Blue (`#0EA5E9` / `sky-500`).

#### 2.5 Light & Dark Theme Support
- Native dark mode support toggled via a persistent client-side state stored in `localStorage`.
- Smooth CSS color transitions (`transition-colors duration-200`).

---

### 3. FONTS & TYPOGRAPHY

#### 3.1 Primary Font Family
- **Font Stack**: `'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`.
- Modern, clean, geometric sans-serif offering maximum legibility for dense academic tables and long-form email drafts.

#### 3.2 Heading Styles
- **H1 (Page Titles)**: `24px` (`1.5rem`), font-weight: `Bold` (`700`), line-height: `1.2`, tracking: `-0.02em`.
- **H2 (Section Headers / Modals)**: `18px` (`1.125rem`), font-weight: `SemiBold` (`600`), line-height: `1.3`.
- **H3 (Card Titles / Subsections)**: `15px` (`0.9375rem`), font-weight: `SemiBold` (`600`), line-height: `1.4`.

#### 3.3 Body Text & Data Styles
- **Body Regular**: `14px` (`0.875rem`), font-weight: `Regular` (`400`), line-height: `1.5`.
- **Body Medium (Labels & Table Headers)**: `13px` (`0.8125rem`), font-weight: `Medium` (`500`), line-height: `1.4`.
- **Captions & Metadata (Timestamps, DOIs)**: `12px` (`0.75rem`), font-weight: `Regular` (`400`), line-height: `1.4`, tracking: `0.01em`.
- **Code / Placeholders**: `'JetBrains Mono', 'Fira Code', monospace`, `12px`, font-weight: `Medium` (`500`).

#### 3.4 Font Weights
- Regular: `400`
- Medium: `500`
- SemiBold: `600`
- Bold: `700`

---

### 4. MEMORY (UI PREFERENCES)

- **Remember User Preferences**:
  - Automatically persist user interface states in browser `localStorage`.
- **Theme Mode**:
  - Store `theme: 'light' | 'dark' | 'system'` to persist across page reloads.
- **Sidebar / Layout State**:
  - Persist sidebar collapse state (`sidebar_collapsed: boolean`) so power users enjoy maximum screen real estate.
- **Table & Pipeline Filters**:
  - Remember last active filters (e.g., specific department filter, sort field, or pipeline view: Table vs. Kanban).
- **Composer Defaults**:
  - Remember the candidate's last chosen email draft tone and word count settings.

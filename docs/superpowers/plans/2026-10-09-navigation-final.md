# Final navigation implementation plan

**Goal:** Single-click cards, consistent 17-page navigation, and clear onward routes.
**Architecture:** Static HTML and scoped CSS; a separate navigation controller progressively enhances a native details menu. documentary.js and all existing player markup remain unchanged.
**Spec:** UIUX-SPEC.md and the user's 2026-10-09 instructions and decisions.
**Execution:** Inline, using executing-plans and verification-before-completion.

## Constraints
- Preserve prose, names, intro appearance, existing work content order and player markup.
- Work only on uiux-polish; three feature commits plus one test alignment commit; no merge/push/deploy.
- Reuse literal existing fallback URLs, never construct one from an ID.
- Report player baseline differences without changing baseline or documentary.js.

## Tasks
- [ ] Compare main and branch legacy failures; classify each in a report.
- [ ] Phase 1: one title link per card, fine-pointer hover, active/touch feedback, verified fallback URLs. Test link structure and preserved content/player markup; commit.
- [ ] Phase 2: common header/footer and five-item details menu, separate focus/scroll controller, fieldwork local menu and breadcrumbs. Test all 17 pages and menu behavior; commit.
- [ ] Phase 3: primary page sequence cards, work switcher before content, work previous/next cards and mobile safe-area action bar. Test route graph and ordering; commit.
- [ ] Align tests only for approved content changes and obsolete navigation expectations; retain player checks. Commit independently.
- [ ] Verify seven widths and touch hit testing where browser access permits; explicitly report any blocked browser verification.

## Review focus
- Native links work without JavaScript, and all visible card surfaces share one target.
- Mobile menu traps focus, restores focus, and restores background scroll after resize/close.
- Fixed controls do not cover video, reflections or footer.
- Index/404 relative URL and canonical behavior remain correct.
- Existing content and player bytes are protected against unrelated changes.

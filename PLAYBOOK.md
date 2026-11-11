# Weekly run playbook

Runs every Sunday morning (Asia/Jerusalem) for the coming Monday-Sunday. `<week>` = the ISO week of the coming Monday, e.g. `2026-W48`.

1. **Analyst** writes `reports/<last-week>.md` from Metricool data.
2. **Strategist** writes `content/<week>/brief.md` (max 5 posts).
3. **Creator** writes `plan.json`, renders media with `tools/render.py`, writes `posts.json`.
4. **Reviewer** (a separate agent that didn't make the content) writes `review.md`. Creator fixes every FIX item; Reviewer re-checks until all PASS.
5. **Publisher** pushes media, verifies the public URLs, and creates every post in Metricool as a **draft** (`draft: true`). Saves ids to `scheduled.json`.
6. **Owner approval:** send the owner ONE message (SendUserMessage + a push notification if available) with a short summary table of the week (day, platform, hook) and the Metricool planner link, and ask them to reply "approve" or list changes.
7. On "approve": Publisher flips each draft to `draft: false`. On changes: apply them, re-review, ask again. If no reply, leave everything as drafts. **Never publish without approval.**
8. Commit `content/<week>/` and `reports/` (text and media only) with a short message.

## Content mix that works for printables
- Carousels: "5 screen-free ideas for a rainy day", "Watch it pop/bloom/spin", "What's inside the workbook", "Grown-up + Me challenge of the week".
- Short videos: one project per video, the WOW moment in the first 2 seconds, CTA at the end.
- Every 3rd post points to the free sampler; at most 1 in 5 is a direct "buy" post.

## Formats
- Carousel images 1080x1350 (Instagram POST carousel; TikTok photo post).
- Videos 1080x1920 mp4 (Instagram REEL, TikTok, YouTube short). Cover image `<id>-cover.jpg`.

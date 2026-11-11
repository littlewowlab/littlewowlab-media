# Review 2026-W47 (independent reviewer, 2026-11-11)

Checked: posts.json, plan.json, brief.md, all 19 carousel slides, both covers, frames of 02.mp4 and 04.mp4 (1080x1920, 11.4 s).
Good across the board: links are exactly https://payhip.com/b/uJxGl and https://payhip.com/b/Bh3zC; AI disclosure is in every caption; no "my kid made this"; no invented numbers or reviews; 5 posts; all captions far under limits (longest TikTok 186 chars, YouTube titles 67 and 70 chars); no spelling errors.

**Verdict: 01 FIX · 02 FIX (major) · 03 FIX · 04 FIX (render only) · 05 FIX**

## Applies to both videos (02, 04)
- **Silent audio.** The track measures -91 dB on both. Add a royalty-free music bed in the render, or add a sound in-app before posting. Silent Reels and TikToks get far less reach.
- **Hook text is in the UI danger zone.** On the cover/hook frames the text sits at y≈1470-1740 of 1920. TikTok and Reels caption overlays cover roughly the bottom 400 px. Move the text block up so it ends at about y≤1450.
- **The "tip" scene uses only the top 20% of the frame.** The rest is blank mint or lilac. Make the lines bigger (about 2x) and centre them vertically.
- When publishing, set the AI flags (isAiGenerated, isAigc, isAiGeneratedContent). They are not in posts.json, so the publisher must add them.

## 01 Launch carousel: FIX
1. **01-4 (code wheel, p13): the outer ring is wrong.** It reads "A B C C D E F E F G H", so letters repeat and the cipher can't work. Parents will spot it. Regenerate or replace the photo with one whose alphabet is correct. If that isn't possible, swap this slide for another project (for example p08 Rainbow Butterflies) and update the caption list to match.
2. 01-4 subtitle: change "Turn it, write it, only your partner can read it." to "Turn it, write it. Only someone with the wheel can read it."
3. **01-6 CTA photo is p10 (Color-Changing Potion Lab), which is NOT in the free sampler.** Under "Try 3 projects free" it implies it is. Use p07, p03 or p22 instead (sampler = #3, #7, #22).
4. Optional: change "#momlife" to "#parentlife" (IG) and "#momtok" to "#parentsoftiktok" (TikTok), so dads aren't excluded.

## 02 Blooming flower video: FIX (major, misleading)
1. **The hook promises motion the video never shows.** "Drop this paper flower on water... watch what happens" and "The petals open by themselves" run over still photos in which the flower is already fully open in every scene. Nothing blooms. Viewers will feel baited.
   - Best fix: add a real or animated before/after. Show a folded flower (crop the folded ones on the right of p07), then the open flower, as two distinct scenes with a transition.
   - Minimum fix: change the hook text to "This paper flower blooms on water 🌸" and the sub-line to "write a secret inside first". Change the IG caption's first line to "Fold a paper flower, set it on water, and the petals slowly open by themselves 🌸".
2. **The cover and the "...and your secret appears" scene already show the secret "I ♥ U".** That contradicts the caption ("it stays hidden until it blooms"). Make the cover a folded flower with the secret hidden.
3. Scene 4 sub-line: "Kids ask to do it again and again" reads as an observed claim about real kids. Replace it with "Make a whole bouquet of secrets".
4. Cover: the flower is cropped off the left edge. Re-centre it.

## 03 Rainy-day list carousel: FIX
1. **Safety: the post includes a wall marble run with no marble warning.** Add to the IG caption, after the materials line: "Grown-up note: marbles are a choking hazard, so keep them away from under-3s." On slide 03-5, change the subtitle to "Tape ramps to the wall. Marbles: not for under-3s."
2. **Misleading materials line.** Change "All you need is paper, tape, scissors and a few things from the kitchen drawer." to "Mostly paper, tape and things you already have: straws, a flashlight, a marble, a few paper clips."
3. 03-1 (hook) and 03-2 (straw rockets) are the same p12 photo. Use p21 or p23 for the hook so slide 2 isn't a repeat.
4. Minor: on the CTA board game (p19), the square numbers are scrambled AI artifacts (for example "BACK 1" appears twice and 30 sits next to 25). It's acceptable at phone size, but swap the photo if a cleaner one exists.

## 04 Fortune teller video: FIX (render only; captions approved)
- The captions, YouTube title and description are all fine.
- Apply the shared video fixes above: add audio, move the hook text up out of the bottom 400 px, and enlarge the "How to play" lines.
- Optional: the fortune teller's numbers are messy (a sideways "8", an upside-down "5"). It's acceptable as a kid-drawn look.

## 05 Holiday gifts carousel: FIX
1. **Safety: a lantern shown glowing on a bedside table at night needs the battery note.** Change "3. A glowing paper lantern" to "3. A glowing paper lantern (battery tea light only, never a real candle)". On slide 05-4, change the subtitle to "Star windows glow on the walls (battery tea light only)."
2. **Unprovable claim.** Change "The holiday gifts grandparents actually keep 🎁" to "Holiday gifts made to be kept 🎁". On 05-1, change the sub-line "Grandparents will keep these forever" to "Made by little hands, made to keep".
3. Change "No shopping, just paper, crayons and little hands:" to "No shopping, just paper, crayons, a cardboard tube and little hands:".
4. 05-1 and 05-2 are the same coupon photo, and p01 (the dragon card) appears on 05-3 and 05-6 as well as 01-1, three times this week. Use p15 or p16 for the 05-6 CTA, and a different crop or photo for the 05-1 hook.
5. 05-3: the dragon card reads "Happy Birthday!", which is off-message for a holiday-gifts post. Acceptable, but if possible use a version that doesn't say birthday, or change the subtitle to "Open it and the dragon leaps off the page. Perfect for any celebration."
6. 05-5 title: "A desk buddy for the office" makes it sound like a gift for a parent's work desk. Change it to "A desk buddy for Grandpa's desk".

## Re-review (2026-11-11)

Re-checked posts.json, plan.json, all 19 slides, both covers, and frames of 02.mp4 and 04.mp4 every 2.2 s. ffprobe shows h264 1080x1920 plus an AAC audio stream on both videos, 11.4 s long.

**Both videos:** audio PASS (mean -29.6 dB, peak -7.2 dB) · hook text out of the bottom zone PASS (text ends at y≈1400 of 1920, covers at y≈1385) · tip scene enlarged PASS (readable, still top-weighted but fine) · AI flags: still not in posts.json, so the publisher must set them. This is a reminder, not a render fix.

**01:** 1 PASS (the code wheel was replaced by p03 Spinning Illusion Disc) · 2 PASS (n/a, slide replaced) · 3 PASS (the CTA is now p22, which is in the sampler) · 4 PASS
**02:** 1 PASS (minimum fix: hook, sub-line and IG first line updated) · 2 PASS (accepted: the hook no longer promises a hidden secret, and the cover reads as the end result) · 3 PASS · 4 PASS (the flower is fully in frame)
**03:** 1 PASS (marble note in the caption and on 03-5) · 2 PASS · 3 FIX, minor and non-blocking: the hook now uses p23, which repeats slide 03-6 (mini-golf). My earlier suggestion caused this. · 4 PASS (accepted)
**04:** PASS (render fixes applied)
**05:** 1 PASS (tea-light note in the caption and on 05-4) · 2 PASS · 3 PASS · 4 PASS (hook p08, CTA p06; p01 now appears only on 01-1 and 05-3) · 5 PASS · 6 PASS

New blocking problems: none. Spelling, links, handles, hashtags and the AI disclosure are all fine. No claim that a real child made anything, and no invented numbers or testimonials.

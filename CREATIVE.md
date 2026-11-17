# Creative standard (read before planning or making anything)

The first two posts (W47 slideshows) were rejected by the owner as generic. This is the bar now.

## The four tests. A post that fails any one is not made.
1. **Scroll-stop:** the first 2 seconds show real motion of the WOW moment (flower opening, rocket leaving the straw, card popping up). Never open on a title card, logo or still photo.
2. **Value without buying:** the viewer can do the craft tonight from the post alone, with plain paper. The printable template is the shortcut, not the gate.
3. **Story:** setup -> tension -> payoff. Something is hidden, promised or attempted in second 1 and resolved by the end ("Write a secret inside. Drop it in water. Wait.").
4. **Save or share reason:** a parent would save it for a rainy day or send it to another parent.

## Video anatomy (9:16, 12-20 s)
- 0-2 s: the WOW clip itself, mid-action, with a hook of 8 words or fewer on screen.
- 2-12 s: 3 fast steps, each a moving clip or a tight close-up, one short line of text each.
- Payoff: the WOW moment again, completed.
- Last 2 s: one CTA ("Free template in bio"). No logo outro.
- Text sits in the middle band (clear of the top 12% and bottom 28%).

## Hooks
Strategist writes 5 hooks per post and picks one, noting why. Good patterns: a command with a withheld result ("Don't throw away your toilet roll tubes"), a curiosity gap ("This flower hides a secret"), a relatable moment ("For the next 'I'm bored'"), a tiny challenge ("Bet your kid can't land it in the cup"). Banned: "30 screen-free crafts...", product-first openers, anything that reads like an ad.

## Clips
Motion clips are AI-generated (Gemini video) from prompts in `content/<week>/clips.md`, stored in `brand/clips/`. Hands only, no faces, no on-screen text in the clip. Reject clips with warped hands, impossible physics or garbled writing. Every post keeps the AI label and the caption disclosure.

## Carousels
Only as full tutorials ("Save this: bloom-on-water flowers in 5 minutes", every step shown) or a genuinely useful list. Slide 1 must work as a hook on its own.

## Captions
Line 1 repeats the hook's promise in different words. Then the steps in 3 short lines. Then one CTA. No walls of hashtags (5-6).

## Audio and covers (research 2026-11-17)
What the top "kids crafts" reels on Instagram actually do (explore results checked in the browser: e.g. diy_shorts_45 caterpillar 92.9K likes, geniokid.app snail 12K, craftooria frog 2.1K):
- **Audio:** almost all use *Original audio*: the craft's own sounds or a playful/funny voice track, not chart songs. Weekly "trending audio" lists (Metricool, SocialPilot) are dominated by holiday/pop tracks used for gift guides, couples and dance trends.
- **So:** every video keeps its natural craft sound (normalised, no generic music bed). On Instagram, where the API can attach licensed catalog audio, add a seasonal trending track at low volume under the craft sound when it fits the post (e.g. Christmas-break content in Nov/Dec). Never bake copyrighted songs into the file.
- **Covers:** `tools/cover.py`. Hands + the finished craft filling the frame, plain background, saturated colour, ONE short bold line (3-5 words) inside the centre 1080x1080 square so it survives the grid crops. No logo, no frames, no collage. Check the 9:16, 4:5 and 1:1 crops before posting.
- TikTok (personal account) ignores custom covers and API audio: the first frame is the cover, so open on the WOW moment.

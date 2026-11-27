# chennaiminnal-autopost - project context

Automatic Chennai-district news reels for the Instagram page **சென்னை மின்னல்** (`@chennaiminnal`; hashtag `#ChennaiMinnal`;
`post_to` value in the Sheet: `Chennai Minnal`), also shared to its Facebook Page. Copied on 11 Nov 2026 from the friend's working
project github.com/news360-tn/coimbatore360-autopost (page "Chennai 360") as it ran that day, with our name, images and accounts.
Internal page key stays `chennai` and the file structure / function names are unchanged, so upstream fixes can be ported by diff.
Everything runs on GitHub Actions; the Google Sheet (through the Apps Script bridge) is the working store.
Setup from zero: `docs/SETUP_CHENNAI_MINNAL.md`. Brand images: `python3 tools/make_brand.py`.

**Status: not live** (no `LIVE` file, no `research_free/ENABLED`). See the owner setup checklist in `README.md`.

## How it works (end to end)

```
every 2 h    research_free.yml  collect news (newspaper sites incl. Dinamalar Chennai page, Google/Bing News, Chennai searches)
                                 -> open + check each article -> only Chennai-district news of today/yesterday
                                 -> queue by priority (research_free/archive/queue.json)
every 20 min write_stories.yml  write each queued news by priority (free LLM chain only) -> ONE AI image of the main scene
                                 (Cloudflare FLUX schnell -> NVIDIA FLUX -> paid FAL only if both fail) -> story saved in the Sheet
                                 -> starts posting at once
every 5 min  post.yml           checks (Chennai only, not stale, no duplicate, daily cap 50; posts at once) -> reel (reel/reel4.py,
                                 Valluvar voice) -> Instagram (one page, no collab)
daily        insights.yml       Instagram insights -> learned topic weights (writer priority)
```

## Rules the owner decided (keep them)

| Area | Rule |
|---|---|
| News scope | Only Chennai-district news, published today or yesterday (Chennai town, its taluks and the villages). Tiruppur, Nilgiris, Erode, Palakkad and every other district are not ours, even when close. "Avinashi Road" is a Chennai city road: a headline that also names a Chennai place is ours |
| One page | Only சென்னை மின்னல். No second page, no collaborator, no Rasipuram routing |
| Priority | power cut (TNEB) > crime > accident > civic > the rest |
| Never miss news | Everything eligible is queued and written; duplicates and other-district news are skipped; nothing eligible is dropped |
| Daily cap | 50 reels a day (Instagram's limit) (`DAILY_CAP` in post.yml, also in the collector / writer); urgent news first |
| Posting time | No fixed times (owner 29 Oct): every reel posts the moment it is made (`poster/config.json` `prime_time.enabled: false`) |
| Format | Reel only (no carousel) |
| Voice | **Valluvar only** (free edge-tts `ta-IN-ValluvarNeural`). Google voices are never used, even if a Google key exists |
| Follow line | Spoken: மேலும் செய்திகளுக்கு சென்னை மின்னல் பக்கத்தை பின்தொடருங்கள். Caption: சென்னை செய்திகளைத் தவறவிடாமல் இருக்க Save செய்து Follow செய்யுங்கள் 📌 |
| Images | ONE new photo-realistic AI image per reel (main scene of THIS news, no text/logos); the reel uses different camera moves / crops of it. Free first: Cloudflare FLUX schnell -> NVIDIA FLUX; paid FAL `flux/schnell` -> `flux/dev` only as the last fallback. Picture check (free Gemini) as in Namakkal |
| Writing | Free LLM chain only; Claude backup OFF (`CLAUDE_MAX_CALLS=0`, no `ANTHROPIC_API_KEY`) |
| Reel language | Formal news Tamil, no slang; everyday Tamil Nadu words in voice, subtitles and cards (பஸ், டூவீலர், போலீசார், கலெக்டர் ...); dates always with the month |
| Website | Off for now (later). `poster/website.py` does nothing without `WEBSITE_INGEST_KEY`; workflows do not pass it |
| Separation | Own accounts and keys, so Namakkal's free API limits are never used; bridge e-mails tagged `CHENNAIMINNAL` |
| Privacy | Personal project; bot commits as `chennaiminnal-bot`; no office account, office email or Claude lines in commits |

## Main files

| Path | What |
|---|---|
| `research_free/collect.py`, `allnews.py`, `sources.py` | collection, Chennai district checks, queue, writer, image |
| `research_free/rules.md`, `examples.json`, `names.py` | writing rules and spoken-word fixes |
| `poster/post.py` | posting checks, prime time, daily cap, Instagram publishing |
| `poster/freshness.py` | stale / duplicate / power-cut timing rules |
| `poster/config.json` | voice (Valluvar), prime time, design switches |
| `reel/reel4.py` | reel renderer (one image, camera moves, voice, opening, dates) |
| `apps_script/Code.gs` | Google Sheet bridge for the Chennai Minnal account (set the `..._HERE` values; redeploy after changes) |
| `tests/test_regressions.py` | regression tests (run before every push) |

## Sheet bridge (apps_script/Code.gs)

- Page key `chennai`, label `சென்னை மின்னல்`, `post_to` `Chennai Minnal`, token property `IG_TOKEN_CHENNAI` (refreshed weekly).
- Columns: same 31 as Namakkal; column 25 `spare_link` (unused), column 26 `chennai_link` (carousel link, unused while reel only),
  27 `reel_link`.
- GET actions: `queue`, `posted_rows`, `token`, `voice`, `recent`, `ping`, `autoPending`.
  POST actions: `posted`, `error`, `addStories`, `archiveNews`, `reoffer`, `setImages`, `repost`.
- E-mail subjects: `CHENNAIMINNAL STORY`, `CHENNAIMINNAL REEL`, `[CHENNAIMINNAL IMAGES NEEDED]` ...

## Secrets (GitHub -> Settings -> Secrets -> Actions; values never in the repo)

BRIDGE_URL, BRIDGE_KEY, GEMINI_API_KEY, GROQ_API_KEY, NVIDIA_API_KEY, CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID,
CLOUDINARY_CLOUD, CLOUDINARY_PRESET; optional MISTRAL_API_KEY, OPENROUTER_API_KEY, GH_MODELS_TOKEN, FAL_KEY (paid image fallback).
Not used: ANTHROPIC_API_KEY, GOOGLE_TTS_API_KEY, WEBSITE_INGEST_KEY. Local copies live only in `.env` (git-ignored).

## Run and check

```
python3 -m unittest discover -s tests        # regression tests (also run by tests.yml on every code push)
python3 tools/repost.py RN-158               # (Actions: repost) post a reel again after it was removed from Instagram
```

## Recent changes
<!-- recent-changes:start (updated automatically by .github/workflows/context.yml - do not edit by hand) -->
| Date | Commit | Change |
|---|---|---|
| 2026-11-27 | `fb4af00` | powercut: notices written |
| 2026-11-27 | `4b06eb9` | powercut: notices written |
| 2026-11-27 | `1f10e61` | pick: written and posted |
| 2026-11-27 | `e1dd7d6` | facebook RN-327 |
| 2026-11-27 | `2da78e9` | goldrate posted |
| 2026-11-27 | `1db037d` | facebook RN-324 |
| 2026-11-27 | `d44cca5` | facebook RN-328 |
| 2026-11-27 | `56644b0` | facebook RN-302 |
| 2026-11-27 | `88defa0` | facebook RN-325 |
| 2026-11-27 | `6056747` | pick: picked news saved |
| 2026-11-27 | `bb4eb23` | pick: picked news saved |
| 2026-11-27 | `77975a7` | pick: list sent |
| 2026-11-27 | `bf728c7` | powercut: notices written |
| 2026-11-27 | `21dec84` | facebook RN-321 |
| 2026-11-27 | `b3d2e81` | facebook RN-318 |
| 2026-11-27 | `3d018da` | powercut: notices written |
| 2026-11-27 | `d238467` | facebook RN-317 |
| 2026-11-27 | `3200db1` | facebook RN-310 |
| 2026-11-27 | `ce1773d` | powercut: notices written |
| 2026-11-27 | `281adcb` | facebook RN-311 |
| 2026-11-27 | `6f98ba4` | facebook RN-277 |
| 2026-11-27 | `9ecc95b` | facebook RN-322 |
| 2026-11-27 | `50d3be9` | facebook RN-323 |
| 2026-11-27 | `f0289a5` | facebook RN-319 |
| 2026-11-27 | `00a6550` | facebook RN-320 |
| 2026-11-27 | `a70023a` | facebook RN-315 |
| 2026-11-27 | `9770b5a` | powercut: notices written |
| 2026-11-26 | `46ffcc0` | pick: written and posted |
| 2026-11-26 | `aa2c17f` | pick: picked news saved |
| 2026-11-26 | `cb4db3f` | pick: picked news saved |
<!-- recent-changes:end -->

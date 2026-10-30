# YouTube Scraper

[![ci](https://github.com/quantumproxies/youtube-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/youtube-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape YouTube from Python or the command line: search results for a query, a channel's uploads with its subscriber and video counts, and full metadata per video, with exact views and likes, length, category, tags and caption languages, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no YouTube Data API key to set up, no proxy to rotate and no headless browser to keep alive: sign in once and run a command. AI agents can call the same collectors from Claude or any MCP client, and no-code flows from n8n.

```bash
pip install git+https://github.com/quantumproxies/youtube-scraper
youtube-scraper login
youtube-scraper channel @NASA --max-results 50 -o nasa.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `youtube-scraper search` | query | Views, channel, duration, 18 fields per row ([fields and price](https://quanticdata.io/collectors/youtube-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper)) | up to 100 |
| `youtube-scraper channel` | handle, channel id or URL | A channel's uploads with views, duration and channel stats, 23 fields per row ([fields and price](https://quanticdata.io/collectors/youtube-channel-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper)) | up to 150 |
| `youtube-scraper videos` | video ids or URLs | Exact views and likes, length, category, captions, 31 fields per row ([fields and price](https://quanticdata.io/collectors/youtube-video-data-api/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper)) | up to 20 |

`search` orders results with `--sort` (relevance, upload_date, view_count or rating); `channel` reads the tab picked with `--tab` (videos, shorts or streams). `--country` sets the region and, on search, `--lang` the interface language.

## Sample output

A real row from `youtube-scraper search "python tutorial" --country us --max-results 3` (2026-10-22):

```json
{
  "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
  "live": false,
  "rank": 2,
  "title": "Python Full Course for Beginners",
  "views": "49,412,017 views",
  "badges": [
    "CC"
  ],
  "channel": "Programming with Mosh",
  "duration": "6:14:07",
  "video_id": "_uQrJ0TkZlc",
  "published": "7y ago",
  "thumbnail": "https://i.ytimg.com/vi/_uQrJ0TkZlc/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLA9oKvpSRnVyO4qbY3eQJe_4mWM2w",
  "channel_id": "UCWv7vMbMWH4-V0ZXdmDpPBA",
  "channel_url": "https://www.youtube.com/@programmingwithmosh",
  "description": "Learn Python for AI, machine learning, and web development with this beginner-friendly course! Get 6 months of PyCharm ...",
  "views_short": "49M",
  "views_value": 49412017,
  "channel_verified": true,
  "duration_seconds": 22447
}
```

## Python

```python
from quanticdata_youtube_scraper import YouTubeScraper

youtube = YouTubeScraper()  # saved login, or QUANTICDATA_API_KEY

results = youtube.search("python tutorial", sort="view_count", max_results=50)
for v in results:
    print(v["video_id"], v["views_value"], v["duration"], v["channel"], v["title"])

uploads = youtube.channel("@NASA", tab="videos", max_results=50)
print(uploads.rows[0]["channel_subscribers"], uploads.rows[0]["channel_videos"])
uploads.to_csv("nasa_uploads.csv")

stats = youtube.videos([v["video_id"] for v in uploads][:20], max_results=20)
for v in stats:
    print(v["video_id"], v["views"], v["likes"], v["category"], v["captions_available"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Channel uploads to CSV**: Export the latest videos, shorts or streams of one or more channels, with views, duration, publish age and each channel's subscriber count, to one CSV. See [`examples/channel_to_csv.py`](examples/channel_to_csv.py).
- **Video stats tracker**: Record the exact views and likes of a list of videos every few hours and keep the history in a CSV to chart how they grow. See [`examples/video_stats_tracker.py`](examples/video_stats_tracker.py).
- **Topic research**: Run a set of search queries and see which videos and channels own them, by views and recency. See [`examples/search_topics.py`](examples/search_topics.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `youtube-scraper run <id> -o out.csv` collects it later.

### `youtube-scraper search`

YouTube search results without the Data API — views, channel, duration.

```
youtube-scraper search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search on YouTube. |
| `--sort` | relevance / upload_date / view_count / rating | `relevance` | Result order. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | Interface language (hl), e.g. en, it, de. |
| `--max-results` | integer | `20` | How many videos to deliver at most (1–100). You pay only for delivered videos. |

### `youtube-scraper channel`

A channel's uploads with views, duration and channel stats.

```
youtube-scraper channel CHANNEL [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `CHANNEL` | string |  | Handle (@NASA), channel id (UC…) or channel URL. |
| `--tab` | videos / shorts / streams | `videos` | Which uploads tab to read. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `30` | How many videos to deliver at most (1–150). You pay only for delivered videos. |

### `youtube-scraper videos`

Full metadata per video id — exact views and likes, length, category, captions.

```
youtube-scraper videos VIDEOS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `VIDEOS` | string[] |  | Video ids or watch/shorts/youtu.be URLs. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `5` | How many videos to deliver at most (1–20). You pay only for delivered videos. |

## Output fields

<details><summary><code>youtube-scraper search</code>: 18 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `video_id` | string | YouTube video id. |
| `title` | string | Video title. |
| `url` | string | Watch URL. |
| `channel` | string or null | Channel name. |
| `channel_url` | string or null | Channel URL. |
| `views` | string or null | View count as shown. |
| `views_value` | integer or null | View count as a number (null for live viewer counts). |
| `published` | string or null | Publish age ("6 months ago"). |
| `duration` | string or null | Duration (m:ss). |
| `live` | boolean | True for live streams. |
| `description` | string or null | Description snippet. |
| `thumbnail` | string or null | Thumbnail URL. |
| `badges` | string[] | Badges (4K, CC, New…). |
| `channel_id` | string or null | Channel id (UC…). |
| `channel_verified` | boolean | Channel has the verified badge. |
| `views_short` | string or null | Compact view count as shown on the tile (26K views). |
| `duration_seconds` | integer or null | Duration in seconds. |

</details>

<details><summary><code>youtube-scraper channel</code>: 23 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position on the tab. |
| `channel` | string or null | Channel name. |
| `channel_id` | string or null | Channel id (UC…). |
| `channel_url` | string or null | Canonical channel URL. |
| `channel_description` | string or null | Channel description (trimmed). |
| `channel_subscribers` | integer or null | Subscribers (15.1M → 15100000). |
| `channel_videos` | integer or null | Total videos on the channel. |
| `video_id` | string | Video id. |
| `title` | string | Video title. |
| `url` | string | Watch URL. |
| `views` | string or null | Views as shown. |
| `views_value` | integer or null | Views as a number. |
| `published` | string or null | Publish age. |
| `duration` | string or null | Duration (m:ss). |
| `live` | boolean | True for live/premiere items. |
| `thumbnail` | string or null | Thumbnail URL. |
| `channel_handle` | string or null | Channel handle (@NASA). |
| `channel_avatar` | string or null | Channel avatar URL. |
| `channel_keywords` | string or null | Channel keywords. |
| `published_label` | string or null | Publish age spelled out (3 days ago). |
| `duration_seconds` | integer or null | Duration in seconds. |
| `upcoming` | boolean | Scheduled stream or premiere that has not started. |
| `is_short` | boolean | True for rows from the shorts tab. |

</details>

<details><summary><code>youtube-scraper videos</code>: 31 fields</summary>

| Field | Type | Description |
|---|---|---|
| `video_id` | string | 11-char video id. |
| `url` | string | Canonical watch URL. |
| `title` | string | Video title. |
| `channel` | string or null | Channel name. |
| `channel_id` | string or null | Channel id (UC…). |
| `channel_url` | string or null | Channel URL. |
| `views` | integer or null | Exact view count. |
| `likes` | integer or null | Exact like count (when public). |
| `length_seconds` | integer or null | Duration in seconds. |
| `publish_date` | string or null | Publish date. |
| `upload_date` | string or null | Upload date. |
| `category` | string or null | YouTube category. |
| `keywords` | string[] | Video keywords/tags. |
| `description` | string or null | Description (first 1500 chars). |
| `thumbnail` | string or null | Largest thumbnail URL. |
| `is_live` | boolean | Live content flag. |
| `family_safe` | boolean | Family-safe flag. |
| `captions_available` | boolean | Whether captions exist. |
| `caption_languages` | string[] | Caption language codes. |
| `rank` | integer | 1-based delivery order. |
| `description_full` | string or null | Description with line breaks kept (up to 5 000 chars). |
| `hashtags` | string[] | Hashtags used in the description. |
| `channel_subscribers` | integer or null | Channel subscribers (4.55M → 4550000). |
| `is_short` | boolean | Eligible as a Short. |
| `is_unlisted` | boolean | Unlisted video. |
| `is_private` | boolean | Private video. |
| `allow_ratings` | boolean | Likes enabled. |
| `live_started_at` | string or null | Live broadcast start (ISO 8601). |
| `live_ended_at` | string or null | Live broadcast end (ISO 8601). |
| `embed_url` | string or null | Embed player URL. |
| `available_countries` | integer or null | Number of countries where the video is available. |

</details>

## Sign-in and API keys

- `youtube-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `youtube-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `youtube-scraper login --api-key`.
- `youtube-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/youtube_search/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "python tutorial", "country": "us", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this YouTube scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a query, a channel or a list of videos and get rows back; the requests run on QuanticData's side. No YouTube Data API key is needed either.

**What does videos return that search does not?**

Exact view and like counts, length in seconds, publish and upload dates, category, tags, hashtags, caption languages, the channel's subscriber count and the live, short, unlisted and family-safe flags: 31 fields per video, against 18 on a search row.

**How many results can one run return?**

Up to 100 search results, 150 channel uploads or 20 videos per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as tags, badges and caption languages are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/video_stats_tracker.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [TikTok Scraper](https://github.com/quantumproxies/tiktok-scraper): TikTok scraper for Python and the command line.
- [Instagram Scraper](https://github.com/quantumproxies/instagram-scraper): Instagram scraper for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=youtube-scraper).

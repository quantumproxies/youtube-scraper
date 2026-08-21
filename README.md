# YouTube scraper API — search results and channel uploads as JSON, in Node.js

Two collectors, no API quota, no OAuth, no `key=` in a query string:

- [`youtube_search`](https://quanticdata.io/collectors/youtube-scraper-api/) — a query and a sort
  order → ranked videos with `video_id`, title, URL, channel, channel URL, view label **and**
  `views_value` as an integer, published label, duration, live flag, description and badges.
  **$0.0008 per video**, up to 40 per run.
- [`youtube_channel`](https://quanticdata.io/collectors/youtube-channel-scraper-api/) — a channel
  handle and a tab (`videos`, `shorts`, `streams`) → that tab's uploads, each row also carrying
  the channel's subscriber and video counts. **$0.0008 per video**, up to 60 per run.

```bash
export QUANTICDATA_API_KEY=qd_live_your_key_here

node search.mjs "residential proxies explained" --sort view_count --max 40
node channel.mjs "@NASA" --tab videos --max 60 --csv nasa.csv
node velocity.mjs channels.txt        # views per day since publication, per channel
```

Node.js 18+, zero dependencies.

## Files

| File | What it does |
|---|---|
| [`qd.mjs`](qd.mjs) | collector client + CSV writer |
| [`search.mjs`](search.mjs) | keyword search, four sort orders, view/duration stats |
| [`channel.mjs`](channel.mjs) | one channel's uploads, shorts or streams |
| [`velocity.mjs`](velocity.mjs) | which uploads are outperforming their channel's baseline |
| [`topic_map.mjs`](topic_map.mjs) | one keyword set → which channels own the topic |

## Rows

```jsonc
// youtube_search
{ "rank": 1, "video_id": "dQw4…", "title": "…", "url": "https://www.youtube.com/watch?v=dQw4…",
  "channel": "…", "channel_url": "https://www.youtube.com/@…",
  "views": "1.2M views", "views_value": 1200000,
  "published": "3 years ago", "duration": "12:04", "live": false,
  "description": "…", "thumbnail": "https://…", "badges": ["4K", "CC"] }

// youtube_channel adds
{ "channel_id": "UC…", "channel_description": "…",
  "channel_subscribers": 12400000, "channel_videos": 4821 }
```

`views` keeps YouTube's abbreviation, `views_value` is the integer — always aggregate on the
integer. `published` is relative ("3 years ago"); `velocity.mjs` shows how to turn it into an
approximate age when you need views-per-day.

## Sort orders change the question

| `sort` | What you get |
|---|---|
| `relevance` (default) | what a viewer searching this term sees today |
| `view_count` | the all-time winners for the term — good for topic research |
| `upload_date` | what is being published right now — good for monitoring |
| `rating` | the well-received tail, often much smaller channels |

Running the same query under two sorts and diffing the channel sets is the cheapest
"who is new here" signal there is.

## Related

- [YouTube scraper API](https://quanticdata.io/collectors/youtube-scraper-api/) · [YouTube channel scraper API](https://quanticdata.io/collectors/youtube-channel-scraper-api/)
- [Video search API](https://quanticdata.io/collectors/search-videos-api/) · [All collectors](https://quanticdata.io/collectors/)
- [Market research data](https://quanticdata.io/market-research-data/)

MIT licensed.

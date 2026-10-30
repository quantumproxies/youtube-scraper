"""Uploads of one or more YouTube channels, in one CSV.

    python channel_to_csv.py @NASA @ESA --tab videos --max 100

Each row is one upload with its views, duration and publish age, plus the
channel's subscriber and video counts, so several channels compare side by
side in a sheet. A one-line summary per channel is printed as it goes.
"""

import argparse

from quanticdata_youtube_scraper import YouTubeScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("channels", nargs="+", help="handles (@NASA), channel ids (UC...) or channel URLs")
    parser.add_argument("--tab", choices=["videos", "shorts", "streams"], default="videos")
    parser.add_argument("--max", type=int, default=50, help="uploads per channel (max 150)")
    parser.add_argument("--out", default="channel_uploads.csv")
    args = parser.parse_args()

    youtube = YouTubeScraper()
    rows = []
    for channel in args.channels:
        run = youtube.channel(channel, tab=args.tab, max_results=args.max)
        views = sorted(r["views_value"] for r in run if r.get("views_value") is not None)
        median = views[len(views) // 2] if views else 0
        subscribers = run.rows[0].get("channel_subscribers") if run.rows else None
        print(f"{channel}: {len(run)} {args.tab}, median {median:,} views, {subscribers or 0:,} subscribers")
        rows.extend(run)

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()

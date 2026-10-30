"""Track the views and likes of YouTube videos over time.

Reads video ids or URLs from videos.txt (one per line), fetches their exact
view and like counts and appends one row per video to video_stats.csv with a
UTC timestamp, printing how many views each gained since the last check. Run
it from cron to build a growth curve:

    0 */6 * * *  cd /path/to/here && python video_stats_tracker.py

Needs a login (`youtube-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_youtube_scraper import YouTubeScraper

FIELDS = ["checked_at", "video_id", "title", "channel", "views", "likes", "length_seconds", "publish_date",
          "channel_subscribers"]


def last_views(path):
    latest = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row.get("views"):
                    latest[row["video_id"]] = int(row["views"])
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--videos", default="videos.txt", help="file with one video id or URL per line")
    parser.add_argument("--out", default="video_stats.csv")
    args = parser.parse_args()

    with open(args.videos, encoding="utf-8") as fh:
        videos = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    youtube = YouTubeScraper()
    before = last_views(args.out)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        # The video collector takes up to 20 videos per run.
        for i in range(0, len(videos), 20):
            for video in youtube.videos(videos[i:i + 20], max_results=20):
                writer.writerow({"checked_at": checked_at, **video})
                written += 1
                views = video.get("views")
                if views is not None and video["video_id"] in before:
                    print(f"{video['video_id']}: {views:,} views ({views - before[video['video_id']]:+,})")
    print(f"{written} rows appended to {args.out}")


if __name__ == "__main__":
    main()

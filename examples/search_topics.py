"""Who owns a set of YouTube searches: top videos and channels per query.

    python search_topics.py "python tutorial" "fastapi tutorial" "pandas tutorial" --top 20

Writes youtube_search.csv with every result and the query that found it, then
prints the channels that show up most often across the queries, with the
views their videos add up to.
"""

import argparse
from collections import defaultdict

from quanticdata_youtube_scraper import YouTubeScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("queries", nargs="+")
    parser.add_argument("--sort", choices=["relevance", "upload_date", "view_count", "rating"], default="relevance")
    parser.add_argument("--country", default="us")
    parser.add_argument("--top", type=int, default=20, help="results per query (max 100)")
    parser.add_argument("--out", default="youtube_search.csv")
    args = parser.parse_args()

    youtube = YouTubeScraper()
    rows = []
    channels = defaultdict(lambda: {"videos": 0, "views": 0})
    for query in args.queries:
        run = youtube.search(query, sort=args.sort, country=args.country, max_results=args.top)
        print(f"{query!r}: {len(run)} videos")
        for video in run:
            rows.append({"query": query, **video})
            stats = channels[video.get("channel") or "(no channel)"]
            stats["videos"] += 1
            stats["views"] += video.get("views_value") or 0

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}\nChannels that appear most:")
    ranked = sorted(channels.items(), key=lambda item: (-item[1]["videos"], -item[1]["views"]))
    for name, stats in ranked[:10]:
        print(f"  {stats['videos']:3d} videos  {stats['views']:>14,} views  {name}")


if __name__ == "__main__":
    main()

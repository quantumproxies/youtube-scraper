"""YouTube Scraper: YouTube scraper for Python and the command line: search results, a channel's uploads with its stats, and full video metadata with exact views and likes, as JSON or CSV. Free and open source; sign in with your QuanticData account, no YouTube Data API key, proxies or headless browser to run.

    from quanticdata_youtube_scraper import YouTubeScraper

    scraper = YouTubeScraper()   # saved login (`youtube-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # YouTube search results for a query
    run = scraper.channel(...)   # a channel's videos, shorts or streams with channel stats
    run = scraper.videos(...)   # full metadata for one or more videos
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["YouTubeScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class YouTubeScraper:
    """YouTube Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="youtube-scraper/0.1.0 (+https://github.com/quantumproxies/youtube-scraper)", timeout=timeout)

    def search(
        self, query: str,
        *,
        sort: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """YouTube search results without the Data API — views, channel, duration.

        Args:
            query: What to search on YouTube.
            sort: Result order. One of: relevance, upload_date, view_count, rating.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: Interface language (hl), e.g. en, it, de.
            max_results: How many videos to deliver at most (1–100). You pay only for delivered videos.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per video: see ``types.YoutubeSearchRow``.
        """
        payload = {
            "query": query,
            "sort": sort,
            "country": country,
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("youtube_search", payload, wait=wait, timeout=timeout)

    def channel(
        self, channel: str,
        *,
        tab: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """A channel's uploads with views, duration and channel stats.

        Args:
            channel: Handle (@NASA), channel id (UC…) or channel URL.
            tab: Which uploads tab to read. One of: videos, shorts, streams.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many videos to deliver at most (1–150). You pay only for delivered videos.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 150 rows, one per video: see ``types.YoutubeChannelRow``.
        """
        payload = {
            "channel": channel,
            "tab": tab,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("youtube_channel", payload, wait=wait, timeout=timeout)

    def videos(
        self, videos: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Full metadata per video id — exact views and likes, length, category, captions.

        Args:
            videos: Video ids or watch/shorts/youtu.be URLs.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many videos to deliver at most (1–20). You pay only for delivered videos.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 20 rows, one per video: see ``types.YoutubeVideoRow``.
        """
        payload = {
            "videos": _as_list(videos),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("youtube_video", payload, wait=wait, timeout=timeout)

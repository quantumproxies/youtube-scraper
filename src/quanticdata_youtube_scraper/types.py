"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class YoutubeSearchRow(TypedDict, total=False):
    """One row of `youtube-scraper search` (youtube_search v1.1.1)."""

    rank: int
    """1-based position."""
    video_id: str
    """YouTube video id."""
    title: str
    """Video title."""
    url: str
    """Watch URL."""
    channel: Optional[str]
    """Channel name."""
    channel_url: Optional[str]
    """Channel URL."""
    views: Optional[str]
    """View count as shown."""
    views_value: Optional[int]
    """View count as a number (null for live viewer counts)."""
    published: Optional[str]
    """Publish age ("6 months ago")."""
    duration: Optional[str]
    """Duration (m:ss)."""
    live: bool
    """True for live streams."""
    description: Optional[str]
    """Description snippet."""
    thumbnail: Optional[str]
    """Thumbnail URL."""
    badges: List[str]
    """Badges (4K, CC, New…)."""
    channel_id: Optional[str]
    """Channel id (UC…)."""
    channel_verified: bool
    """Channel has the verified badge."""
    views_short: Optional[str]
    """Compact view count as shown on the tile (26K views)."""
    duration_seconds: Optional[int]
    """Duration in seconds."""

class YoutubeChannelRow(TypedDict, total=False):
    """One row of `youtube-scraper channel` (youtube_channel v1.1.1)."""

    rank: int
    """1-based position on the tab."""
    channel: Optional[str]
    """Channel name."""
    channel_id: Optional[str]
    """Channel id (UC…)."""
    channel_url: Optional[str]
    """Canonical channel URL."""
    channel_description: Optional[str]
    """Channel description (trimmed)."""
    channel_subscribers: Optional[int]
    """Subscribers (15.1M → 15100000)."""
    channel_videos: Optional[int]
    """Total videos on the channel."""
    video_id: str
    """Video id."""
    title: str
    """Video title."""
    url: str
    """Watch URL."""
    views: Optional[str]
    """Views as shown."""
    views_value: Optional[int]
    """Views as a number."""
    published: Optional[str]
    """Publish age."""
    duration: Optional[str]
    """Duration (m:ss)."""
    live: bool
    """True for live/premiere items."""
    thumbnail: Optional[str]
    """Thumbnail URL."""
    channel_handle: Optional[str]
    """Channel handle (@NASA)."""
    channel_avatar: Optional[str]
    """Channel avatar URL."""
    channel_keywords: Optional[str]
    """Channel keywords."""
    published_label: Optional[str]
    """Publish age spelled out (3 days ago)."""
    duration_seconds: Optional[int]
    """Duration in seconds."""
    upcoming: bool
    """Scheduled stream or premiere that has not started."""
    is_short: bool
    """True for rows from the shorts tab."""

class YoutubeVideoRow(TypedDict, total=False):
    """One row of `youtube-scraper videos` (youtube_video v1.1.1)."""

    video_id: str
    """11-char video id."""
    url: str
    """Canonical watch URL."""
    title: str
    """Video title."""
    channel: Optional[str]
    """Channel name."""
    channel_id: Optional[str]
    """Channel id (UC…)."""
    channel_url: Optional[str]
    """Channel URL."""
    views: Optional[int]
    """Exact view count."""
    likes: Optional[int]
    """Exact like count (when public)."""
    length_seconds: Optional[int]
    """Duration in seconds."""
    publish_date: Optional[str]
    """Publish date."""
    upload_date: Optional[str]
    """Upload date."""
    category: Optional[str]
    """YouTube category."""
    keywords: List[str]
    """Video keywords/tags."""
    description: Optional[str]
    """Description (first 1500 chars)."""
    thumbnail: Optional[str]
    """Largest thumbnail URL."""
    is_live: bool
    """Live content flag."""
    family_safe: bool
    """Family-safe flag."""
    captions_available: bool
    """Whether captions exist."""
    caption_languages: List[str]
    """Caption language codes."""
    rank: int
    """1-based delivery order."""
    description_full: Optional[str]
    """Description with line breaks kept (up to 5 000 chars)."""
    hashtags: List[str]
    """Hashtags used in the description."""
    channel_subscribers: Optional[int]
    """Channel subscribers (4.55M → 4550000)."""
    is_short: bool
    """Eligible as a Short."""
    is_unlisted: bool
    """Unlisted video."""
    is_private: bool
    """Private video."""
    allow_ratings: bool
    """Likes enabled."""
    live_started_at: Optional[str]
    """Live broadcast start (ISO 8601)."""
    live_ended_at: Optional[str]
    """Live broadcast end (ISO 8601)."""
    embed_url: Optional[str]
    """Embed player URL."""
    available_countries: Optional[int]
    """Number of countries where the video is available."""

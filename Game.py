from dataclasses import dataclass, field
from typing import Optional
from wrapper import IGDBWrapper

import datetime

def safe_get(data, *keys, default=None):
    if data is None:
        return default

    if isinstance(data, list):
        return [safe_get(entry,*keys,default=default) for entry in data]

    if len(keys) > 0:
        if keys[0] in data.keys():
            return safe_get(data[keys[0]],*keys[1:],default=default)
        else:
            return default
    return data

@dataclass
class Game:
    id: int
    name: str
    url: str
    platforms: list[str] = field(default_factory=list)
    cover: Optional[str] = None
    aggregated_rating: Optional[float] = None
    aggregated_rating_count: Optional[int] = None
    alternative_names: list[str] = field(default_factory=list)
    artworks: list[str] = field(default_factory=list)
    bundles: list[str] = field(default_factory=list)
    collections: list[str] = field(default_factory=list)
    dlcs: list[str] = field(default_factory=list)
    expanded_games: list[str] = field(default_factory=list)
    expansions: list[str] = field(default_factory=list)
    first_release_date: Optional[datetime.datetime] = None
    forks: list[str] = field(default_factory=list)
    franchise: Optional[str] = None
    franchises: list[str] = field(default_factory=list)
    game_engines: list[str] = field(default_factory=list)
    game_localizations: list[str] = field(default_factory=list)
    game_modes: list[str] = field(default_factory=list)
    game_status: Optional[str] = None
    game_type: Optional[str] = None
    genres: list[str] = field(default_factory=list)
    hypes: Optional[int] = None
    involved_companies: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    language_supports: set[str] = field(default_factory=set)
    multiplayer_modes: list[dict] = field(default_factory=list)
    parent_game: Optional[str] = None
    player_perspectives: list[str] = field(default_factory=list)
    ports: list[str] = field(default_factory=list)
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    release_dates: list[datetime.datetime] = field(default_factory=list)
    remakes: list[str] = field(default_factory=list)
    remasters: list[str] = field(default_factory=list)
    screenshots: list[str] = field(default_factory=list)
    similar_games: list[str] = field(default_factory=list)
    slug: Optional[str] = None
    standalone_expansions: list[str] = field(default_factory=list)
    storyline: Optional[str] = None
    summary: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    total_rating: Optional[float] = None
    total_rating_count: Optional[int] = None
    version_parent: Optional[str] = None
    version_title: Optional[str] = None
    videos: list[str] = field(default_factory=list)
    websites: list[str] = field(default_factory=list)

    @classmethod
    def from_igdb(cls,wrapper: IGDBWrapper, name: str, platform: str = "") -> Optional["Game"]:
        FIELDS = [
            "name","url","platforms.name","cover.url","aggregated_rating",
            "aggregated_rating_count","alternative_names.name","artworks.url","bundles.name",
            "collections.name","dlcs.name","expanded_games.name","expansions.name",
            "first_release_date","forks.name","franchise.name","franchises.name",
            "game_engines.name","game_localizations.name","game_modes.name","game_status.status",
            "game_type.type","genres.name","hypes","involved_companies.company.name",
            "keywords.name","language_supports.language.name","multiplayer_modes","parent_game.name",
            "player_perspectives.name","ports.name","rating","rating_count","release_dates.date",
            "remakes.name","remasters.name","screenshots.url","similar_games.name","slug",
            "standalone_expansions.name","storyline","summary","tags","themes.name",
            "total_rating","total_rating_count","version_parent.name","version_title",
            "videos.video_id","websites.url"
        ]

        fields = ",".join(FIELDS)
        platform_txt = f"&(platforms.name ~ *\"{platform}\"* | platforms.abbreviation ~ *\"{platform}\"*)" if platform else ""

        query = f'fields {fields}; where name ~ *\"{name}\"*{platform_txt}; sort rating desc; limit 100;'

        result = wrapper.request('games', query)
        if not result:
            print("No game found!")
            return None
        data = result[0]

        return cls(
            id=safe_get(data, "id"),
            name=safe_get(data, "name"),
            url=safe_get(data, "url"),
            platforms=[p["name"] for p in data.get("platforms",[])],
            cover=("https:" + safe_get(data, "cover", "url",default="")) if safe_get(data, "cover","url",default="") else None,
            aggregated_rating=safe_get(data, "aggregated_rating",default=None),
            aggregated_rating_count=safe_get(data, "aggregated_rating_count",default=None),
            alternative_names=safe_get(data, "alternative_names","name",default=[]),
            artworks=["https:" + str(url).replace("t_thumb", "t_1080p") for url in safe_get(data, "artworks","url",default=[])],
            bundles=safe_get(data, "bundles","name",default=[]),
            collections=safe_get(data, "collections","name",default=[]),
            dlcs=safe_get(data, "dlcs","name",default=[]),
            expanded_games=safe_get(data, "expanded_games","name",default=[]),
            expansions=safe_get(data, "expansions","name",default=[]),
            first_release_date=datetime.datetime.fromtimestamp(safe_get(data, "first_release_date",default=0), datetime.UTC) if safe_get(data, "first_release_date",default=0) else None,
            forks=safe_get(data, "forks","name",default=[]),
            franchise=safe_get(data, "franchise","name",default=None),
            franchises=safe_get(data, "franchises","name",default=[]),
            game_engines=safe_get(data, "game_engines","name",default=[]),
            game_localizations=safe_get(data, "game_localizations","name",default=[]),
            game_modes=safe_get(data, "game_modes","name",default=[]),
            game_status=safe_get(data, "game_status","status",default=None),
            game_type=safe_get(data, "game_type","type",default=None),
            genres=safe_get(data, "genres","name",default=[]),
            hypes=safe_get(data, "hypes",default=None),
            involved_companies=safe_get(data, "involved_companies","company","name",default=[]),
            keywords=safe_get(data, "keywords","name",default=[]),
            language_supports=safe_get(data, "language_supports","language","name",default=[]),
            multiplayer_modes=safe_get(data, "multiplayer_modes",default=[]),
            parent_game=safe_get(data, "parent_game","name",default=None),
            player_perspectives=safe_get(data, "player_perspectives","name",default=[]),
            ports=safe_get(data, "ports","name",default=[]),
            rating=safe_get(data, "rating",default=None),
            rating_count=safe_get(data, "rating_count",default=None),
            release_dates=[datetime.datetime.fromtimestamp(d, datetime.UTC) for d in safe_get(data, "release_dates","date",default=[]) if d],
            remakes=safe_get(data, "remakes","name",default=[]),
            remasters=safe_get(data, "remasters","name",default=[]),
            screenshots=["https:" + str(url).replace("t_thumb", "t_1080p") for url in safe_get(data, "screenshots","url",default=[])],
            similar_games=safe_get(data, "similar_games","name",default=[]),
            slug=safe_get(data, "slug",default=None),
            standalone_expansions=safe_get(data, "standalone_expansions","name",default=[]),
            storyline=safe_get(data, "storyline",default=None),
            summary=safe_get(data, "summary",default=None),
            tags=safe_get(data, "tags",default=[]),
            themes=safe_get(data, "themes","name",default=[]),
            total_rating=safe_get(data, "total_rating",default=None),
            total_rating_count=safe_get(data, "total_rating_count",default=None),
            version_parent=safe_get(data, "version_parent","name",default=None),
            version_title=safe_get(data, "version_title",default=None),
            videos=[f'https://www.youtube.com/watch?v={vid}' for vid in safe_get(data, "videos","video_id",default=[])],
            websites=safe_get(data, "websites","url",default=[])
        )

    def __str__(self):
        return f"ID:{self.id} Game({self.name}) on {', '.join(self.platforms) if self.platforms else 'Unknown platform'}"

    def to_full_string(self):
        return (
            f"Game({self.name}):\n"
            f"  ID: {self.id}\n"
            f"  Name: {self.name}\n"
            f"  URL: {self.url}\n"
            f"  Platforms: {', '.join(self.platforms)}\n"
            f"  Cover URL: {self.cover}\n"
            f"  Aggregated Rating: {self.aggregated_rating}\n"
            f"  Aggregated Rating Count: {self.aggregated_rating_count}\n"
            f"  Alternative Names: {self.alternative_names}\n"
            f"  Artworks: {self.artworks}\n"
            f"  Bundles: {self.bundles}\n"
            f"  Collections: {self.collections}\n"
            f"  DLCs: {self.dlcs}\n"
            f"  Expanded Games: {self.expanded_games}\n"
            f"  Expansions: {self.expansions}\n"
            f"  First Release Date: {self.first_release_date}\n"
            f"  Forks: {self.forks}\n"
            f"  Franchise: {self.franchise}\n"
            f"  Franchises: {self.franchises}\n"
            f"  Game Engines: {self.game_engines}\n"
            f"  Game Localizations: {self.game_localizations}\n"
            f"  Game Modes: {self.game_modes}\n"
            f"  Game Status: {self.game_status}\n"
            f"  Game Type: {self.game_type}\n"
            f"  Genres: {self.genres}\n"
            f"  Hypes: {self.hypes}\n"
            f"  Involved Companies: {self.involved_companies}\n"
            f"  Keywords: {self.keywords}\n"
            f"  Language Supports: {self.language_supports}\n"
            f"  Multiplayer Modes: {self.multiplayer_modes}\n"
            f"  Parent Game: {self.parent_game}\n"
            f"  Player Perspectives: {self.player_perspectives}\n"
            f"  Ports: {self.ports}\n"
            f"  Rating: {self.rating}\n"
            f"  Rating Count: {self.rating_count}\n"
            f"  Release Dates: {self.release_dates}\n"
            f"  Remakes: {self.remakes}\n"
            f"  Remasters: {self.remasters}\n"
            f"  Screenshots: {self.screenshots}\n"
            f"  Similar Games: {self.similar_games}\n"
            f"  Slug: {self.slug}\n"
            f"  Standalone Expansions: {self.standalone_expansions}\n"
            f"  Storyline: {self.storyline}\n"
            f"  Summary: {self.summary}\n"
            f"  Tags: {self.tags}\n"
            f"  Themes: {self.themes}\n"
            f"  Total Rating: {self.total_rating}\n"
            f"  Total Rating Count: {self.total_rating_count}\n"
            f"  Version Parent: {self.version_parent}\n"
            f"  Version Title: {self.version_title}\n"
            f"  Videos: {self.videos}\n"
            f"  Websites: {self.websites}\n"
        )
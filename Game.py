import inspect
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
    wrapper: IGDBWrapper

    id: int
    name: str
    url: str
    platforms: list[str] = field(default_factory=list)
    cover: Optional[str] = None

    _cache: dict = field(default_factory=dict, init=False,repr=False)

    @property
    def aggregated_rating(self):
        return self._lazy_load('aggregated_rating')

    @property
    def aggregated_rating_count(self):
        return self._lazy_load('aggregated_rating_count')

    @property
    def alternative_names(self):
        return self._lazy_load('alternative_names.name')

    @property
    def artworks(self):
        return [('https:' + url).replace('t_thumb','t_1080p') for url in self._lazy_load('artworks.url')]

    @property
    def bundles(self):
        return self._lazy_load('bundles.name')

    @property
    def collections(self):
        return self._lazy_load('collections.name')

    @property
    def dlcs(self):
        return self._lazy_load('dlcs.name')

    @property
    def expanded_games(self):
        return self._lazy_load('expanded_games.name')

    @property
    def expansions(self):
        return self._lazy_load('expansions.name')

    @property
    def first_release_date(self):
        if self._lazy_load('first_release_date'):
            return datetime.datetime.fromtimestamp(self._lazy_load('first_release_date'), datetime.UTC)
        return None

    @property
    def forks(self):
        return self._lazy_load('forks.name')

    @property
    def franchise(self):
        return self._lazy_load('franchise.name')

    @property
    def franchises(self):
        return self._lazy_load('franchises.name')

    @property
    def game_engines(self):
        return self._lazy_load('game_engines.name')

    @property
    def game_localizations(self):
        return self._lazy_load('game_localizations.name')

    @property
    def game_modes(self):
        return self._lazy_load('game_modes.name')

    @property
    def game_status(self):
        return self._lazy_load('game_status.status')

    @property
    def game_type(self):
        return self._lazy_load('game_type.type')

    @property
    def genres(self):
        return self._lazy_load('genres.name')

    @property
    def hypes(self):
        return self._lazy_load('hypes')

    @property
    def involved_companies(self):
        return self._lazy_load('involved_companies.company.name')

    @property
    def keywords(self):
        return self._lazy_load('keywords.name')

    @property
    def language_supports(self):
        return self._lazy_load('language_supports.language.name')

    @property
    def multiplayer_modes(self):
        return self._lazy_load('multiplayer_modes')

    @property
    def parent_game(self):
        return self._lazy_load('parent_game.name')

    @property
    def player_perspectives(self):
        return self._lazy_load('player_perspectives.name')

    @property
    def ports(self):
        return self._lazy_load('ports.name')

    @property
    def rating(self):
        return self._lazy_load('rating')

    @property
    def rating_count(self):
        return self._lazy_load('rating_count')

    @property
    def release_dates(self):
        return self._lazy_load('release_dates.date')

    @property
    def remakes(self):
        return self._lazy_load('remakes.name')

    @property
    def remasters(self):
        return self._lazy_load('remasters.name')

    @property
    def screenshots(self):
        return [('https:' + url).replace('t_thumb','t_1080p') for url in self._lazy_load('screenshots.url')]

    @property
    def similar_games(self):
        return self._lazy_load('similar_games.name')

    @property
    def slug(self):
        return self._lazy_load('slug')

    @property
    def standalone_expansions(self):
        return self._lazy_load('standalone_expansions.name')

    @property
    def storyline(self):
        return self._lazy_load('storyline')

    @property
    def summary(self):
        return self._lazy_load('summary')

    @property
    def tags(self):
        return self._lazy_load('tags')

    @property
    def themes(self):
        return self._lazy_load('themes.name')

    @property
    def total_rating(self):
        return self._lazy_load('total_rating')

    @property
    def total_rating_count(self):
        return self._lazy_load('total_rating_count')

    @property
    def version_parent(self):
        return self._lazy_load('version_parent.name')

    @property
    def version_title(self):
        return self._lazy_load('version_title')

    @property
    def videos(self):
        videos = self._lazy_load('videos.video_id')
        return [f"https://www.youtube.com/watch?v={vid}" for vid in videos if vid]

    @property
    def websites(self):
        return self._lazy_load('websites.url')

    @classmethod
    def from_igdb(cls,wrapper: IGDBWrapper, name: str, platform: str = "") -> Optional["Game"]:
        FIELDS = [
            "name","url","platforms.name","cover.url"
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
            wrapper=wrapper,
            id=safe_get(data, "id"),
            name=safe_get(data, "name"),
            url=safe_get(data, "url"),
            platforms=[p["name"] for p in data.get("platforms",[])],
            cover=("https:" + safe_get(data, "cover", "url",default="")) if safe_get(data, "cover","url",default="") else None
        )

    def _lazy_load(self,field_name: str):
        if field_name not in self._cache:
            query = f'fields {field_name}; where id = {self.id};'
            result = self.wrapper.request('games', query)

            if result:
                if safe_get(result,*field_name.split('.')):
                    self._cache[field_name] = safe_get(result,*field_name.split('.'))
                else:
                    self._cache[field_name] = None
            else:
                self._cache[field_name] = None
        return self._cache[field_name][0]

    def __str__(self):
        return f"ID:{self.id} Game({self.name}) on {', '.join(self.platforms) if self.platforms else 'Unknown platform'}"

    def to_full_string(self,show_all: bool = False):
        if show_all:
            values = {
                name: getattr(self, name)
                for name in dir(self.__class__)
                if isinstance(getattr(self.__class__, name), property)
            }

            return "".join([f" {key}:{value}\n" for key,value in values.items()])
        else:
            return (
                f"Game({self.name}):\n"
                f"  ID: {self.id}\n"
                f"  Name: {self.name}\n"
                f"  URL: {self.url}\n"
                f"  Platforms: {', '.join(self.platforms)}\n"
                f"  Cover URL: {self.cover}\n"
            )
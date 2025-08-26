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

    cache: dict = field(default_factory=dict,repr=False)

    @property
    def aggregated_rating(self):
        """aggregated_rating"""
        return self._lazy_load('aggregated_rating')

    @property
    def aggregated_rating_count(self):
        """aggregated_rating_count"""
        return self._lazy_load('aggregated_rating_count')

    @property
    def alternative_names(self):
        """alternative_names.name"""
        return self._lazy_load('alternative_names.name')

    @property
    def artworks(self):
        """artworks.url"""
        return [('https:' + url).replace('t_thumb','t_1080p') for url in self._lazy_load('artworks.url')]

    @property
    def bundles(self):
        """bundles.name"""
        return self._lazy_load('bundles.name')

    @property
    def collections(self):
        """collections.name"""
        return self._lazy_load('collections.name')

    @property
    def dlcs(self):
        """dlcs.name"""
        return self._lazy_load('dlcs.name')

    @property
    def expanded_games(self):
        """expanded_games.name"""
        return self._lazy_load('expanded_games.name')

    @property
    def expansions(self):
        """expansions.name"""
        return self._lazy_load('expansions.name')

    @property
    def first_release_date(self):
        """first_release_date"""
        if self._lazy_load('first_release_date'):
            return datetime.datetime.fromtimestamp(self._lazy_load('first_release_date'), datetime.UTC)
        return None

    @property
    def forks(self):
        """forks.name"""
        return self._lazy_load('forks.name')

    @property
    def franchise(self):
        """franchise.name"""
        return self._lazy_load('franchise.name')

    @property
    def franchises(self):
        """franchises.name"""
        return self._lazy_load('franchises.name')

    @property
    def game_engines(self):
        """game_engines.name"""
        return self._lazy_load('game_engines.name')

    @property
    def game_localizations(self):
        """game_localizations.name"""
        return self._lazy_load('game_localizations.name')

    @property
    def game_modes(self):
        """game_modes.name"""
        return self._lazy_load('game_modes.name')

    @property
    def game_status(self):
        """game_status.status"""
        return self._lazy_load('game_status.status')

    @property
    def game_type(self):
        """game_type.type"""
        return self._lazy_load('game_type.type')

    @property
    def genres(self):
        """genres.name"""
        return self._lazy_load('genres.name')

    @property
    def hypes(self):
        """hypes"""
        return self._lazy_load('hypes')

    @property
    def involved_companies(self):
        """involved_companies.company.name"""
        return self._lazy_load('involved_companies.company.name')

    @property
    def keywords(self):
        """keywords.name"""
        return self._lazy_load('keywords.name')

    @property
    def language_supports(self):
        """language_supports.language.name"""
        return self._lazy_load('language_supports.language.name')

    @property
    def multiplayer_modes(self):
        """multiplayer_modes"""
        return self._lazy_load('multiplayer_modes')

    @property
    def parent_game(self):
        """parent_game.name"""
        return self._lazy_load('parent_game.name')

    @property
    def player_perspectives(self):
        """player_perspectives.name"""
        return self._lazy_load('player_perspectives.name')

    @property
    def ports(self):
        """ports.name"""
        return self._lazy_load('ports.name')

    @property
    def rating(self):
        """rating"""
        return self._lazy_load('rating')

    @property
    def rating_count(self):
        """rating_count"""
        return self._lazy_load('rating_count')

    @property
    def release_dates(self):
        """release_dates.date"""
        return self._lazy_load('release_dates.date')

    @property
    def remakes(self):
        """remakes.name"""
        return self._lazy_load('remakes.name')

    @property
    def remasters(self):
        """remasters.name"""
        return self._lazy_load('remasters.name')

    @property
    def screenshots(self):
        """screenshots.url"""
        return [('https:' + url).replace('t_thumb','t_1080p') for url in self._lazy_load('screenshots.url')]

    @property
    def similar_games(self):
        """similar_games.name"""
        return self._lazy_load('similar_games.name')

    @property
    def slug(self):
        """slug"""
        return self._lazy_load('slug')

    @property
    def standalone_expansions(self):
        """standalone_expansions.name"""
        return self._lazy_load('standalone_expansions.name')

    @property
    def storyline(self):
        """storyline"""
        return self._lazy_load('storyline')

    @property
    def summary(self):
        """summary"""
        return self._lazy_load('summary')

    @property
    def tags(self):
        """tags"""
        return self._lazy_load('tags')

    @property
    def themes(self):
        """themes.name"""
        return self._lazy_load('themes.name')

    @property
    def total_rating(self):
        """total_rating"""
        return self._lazy_load('total_rating')

    @property
    def total_rating_count(self):
        """total_rating_count"""
        return self._lazy_load('total_rating_count')

    @property
    def version_parent(self):
        """version_parent.name"""
        return self._lazy_load('version_parent.name')

    @property
    def version_title(self):
        """version_title"""
        return self._lazy_load('version_title')

    @property
    def videos(self):
        """videos.video_id"""
        videos = self._lazy_load('videos.video_id')
        return [f"https://www.youtube.com/watch?v={vid}" for vid in videos if vid]

    @property
    def websites(self):
        """websites.url"""
        return self._lazy_load('websites.url')

    @classmethod
    def from_igdb(cls,wrapper: IGDBWrapper, name: str, platform: str = "",load_all: bool = False) -> Optional["Game"]:
        FIELDS = [
            "name","url","platforms.name","cover.url"
        ]

        params = []
        if load_all:
            for _name in dir(Game):
                attr = getattr(Game,_name)
                if isinstance(attr, property):
                    source = attr.fget.__doc__ if attr.fget and attr.fget.__doc__ else _name
                    params.append(source)

        FIELDS = list(set(FIELDS + params))

        fields = ",".join(FIELDS)
        print(fields)

        platform_txt = f"&(platforms.name ~ *\"{platform}\"* | platforms.abbreviation ~ *\"{platform}\"*)" if platform else ""
        query = f'fields {fields}; where name ~ *\"{name}\"*{platform_txt}; sort rating desc; limit 100;'

        result = wrapper.request('games', query)
        if not result:
            print("No game found!")
            return None
        data = result[0]

        params_dict = {param:safe_get(data,*param.split('.')) for param in params}

        return cls(
            wrapper=wrapper,
            id=safe_get(data, "id"),
            name=safe_get(data, "name"),
            url=safe_get(data, "url"),
            platforms=[p["name"] for p in data.get("platforms",[])],
            cover=("https:" + safe_get(data, "cover", "url",default="")) if safe_get(data, "cover","url",default="") else None,
            cache=params_dict
        )

    def _lazy_load(self,field_name: str):
        if field_name not in self.cache:
            query = f'fields {field_name}; where id = {self.id};'
            result = self.wrapper.request('games', query)

            if result:
                if safe_get(result,*field_name.split('.')):
                    self.cache[field_name] = safe_get(result,*field_name.split('.'))
                else:
                    self.cache[field_name] = None
            else:
                self.cache[field_name] = None
        return self.cache[field_name]

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
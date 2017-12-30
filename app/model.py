import config
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Unicode, UnicodeText, Text, Float, DateTime, PickleType

engine = create_engine(config.MYSQL_DATABASE_URI, echo=False)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class App(Base):
    __tablename__ = 'APPS'

    achievements_enabled = Column(Boolean)
    app_id = Column(Unicode(20), primary_key=True)
    app_title = Column(UnicodeText)
    app_type = Column(UnicodeText)
    app_website = Column(UnicodeText)
    big_logo = Column(UnicodeText)
    big_picture_api_raw = Column(Text)
    captions = Column(Boolean)
    commentary = Column(Boolean)
    controller_support = Column(UnicodeText)
    hdr = Column(Boolean)
    hours_played = Column(Float)
    icon = Column(UnicodeText)
    last_updated = Column(DateTime)
    leaderboards_enabled = Column(Boolean)
    metascore = Column(UnicodeText)
    metascore_link = Column(UnicodeText)
    minutes_played = Column(Integer)
    multiplayer = Column(Boolean)
    os_linux = Column(Boolean)
    os_mac = Column(Boolean)
    os_windows = Column(Boolean)
    release_date = Column(UnicodeText)
    required_age = Column(Integer)
    singleplayer = Column(Boolean)
    size_mb = Column(Float)
    small_logo = Column(UnicodeText)
    source_sdk_included = Column(Boolean)
    stats_enabled = Column(Boolean)
    steamcloud_enabled = Column(Boolean)
    store_price_default_usd = Column(Float)
    tradingcards_enabled = Column(Boolean)
    VAC_enabled = Column(Boolean)
    workshop_enabled = Column(Boolean)

    def __repr__(self):
        return '<App %s - "%s" (%s%s) | Type: %s | Multi: %s | Price: $%s | Windows: %s | Mac: %s | Linux: %s | Joy: %s | Metacritic: %s | %s | %s | %s>' % (self.app_id, self.app_title, self.size_mb, ' MB', self.app_type, self.multiplayer, self.store_price_default_usd, self.os_windows, self.os_mac, self.os_linux, self.controller_support, self.metascore, self.icon, self.small_logo, self.big_logo)


class Time_To_Beat(Base):
    __tablename__ = 'TIME_TO_BEAT'

    app_id = Column(Unicode(20), index=True, primary_key=True)
    data_imputed_completionist = Column(Boolean)
    data_imputed_extras = Column(Boolean)
    data_imputed_main_game = Column(Boolean)
    hltb_id = Column(Unicode(20))
    minutes_to_beat_completionist = Column(Float)
    minutes_to_beat_extras = Column(Float)
    minutes_to_beat_main_game = Column(Float)
    timetobeat_api_raw = Column(Text)


class Genre(Base):
    __tablename__ = 'GENRES'

    name = Column(Unicode(200), primary_key=True)


class Genre_App_Map(Base):
    __tablename__ = 'GENRE_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    genres = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class Developer(Base):
    __tablename__ = 'DEVELOPERS'

    name = Column(Unicode(200), primary_key=True)


class Developer_App_Map(Base):
    __tablename__ = 'DEVELOPER_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    developers = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class Publisher(Base):
    __tablename__ = 'PUBLISHERS'

    name = Column(Unicode(200), primary_key=True)


class Publisher_App_Map(Base):
    __tablename__ = 'PUBLISHER_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    publishers = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class Language(Base):
    __tablename__ = 'LANGUAGES'

    name = Column(Unicode(200), primary_key=True)


class Language_App_Map(Base):
    __tablename__ = 'LANGUAGE_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    languages = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class Multiplayer_type(Base):
    __tablename__ = 'MULTIPLAYER_TYPES'

    name = Column(Unicode(200), primary_key=True)


class Multiplayer_type_App_Map(Base):
    __tablename__ = 'MULTIPLAYER_TYPE_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    multiplayer_types = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class DLC_id(Base):
    __tablename__ = 'DLC_IDS'

    name = Column(Unicode(200), primary_key=True)


class DLC_id_App_Map(Base):
    __tablename__ = 'DLC_ID_APP_MAP'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    dlc_ids = Column(Unicode(200), index=True)
    apps = Column(Unicode(20), index=True)


class Users(Base):
    __tablename__ = 'USERS'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Unicode(20), index=True)
    attributes = Column(PickleType)
    last_update = Column(DateTime)

def littleBobbyTables():
    Base.metadata.drop_all(engine)

def createAll():
    Base.metadata.create_all(engine)

import app

db = app.db

# TODO: app_id needs to be explicitly indexed?
class App(db.Model):
    __tablename__ = 'APPS'

    achievements_enabled = db.Column(db.Boolean)
    app_id = db.Column(db.Unicode(20), primary_key=True)
    app_type = db.Column(db.UnicodeText)
    app_website = db.Column(db.UnicodeText)
    big_logo = db.Column(db.UnicodeText)
    captions = db.Column(db.Boolean)
    commentary = db.Column(db.Boolean)
    controller_support = db.Column(db.UnicodeText)
    hdr = db.Column(db.Boolean)
    hours_played = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)
    leaderboards_enabled = db.Column(db.Boolean)
    metascore = db.Column(db.UnicodeText)
    metascore_link = db.Column(db.UnicodeText)
    minutes_played = db.Column(db.Integer)
    multiplayer = db.Column(db.Boolean)
    os_linux = db.Column(db.Boolean)
    os_mac = db.Column(db.Boolean)
    os_windows = db.Column(db.Boolean)
    release_date = db.Column(db.UnicodeText)
    required_age = db.Column(db.Integer)
    singleplayer = db.Column(db.Boolean)
    size_mb = db.Column(db.Float)
    source_sdk_included = db.Column(db.Boolean)
    stats_enabled = db.Column(db.Boolean)
    steamcloud_enabled = db.Column(db.Boolean)
    store_price_default_usd = db.Column(db.Float)
    tradingcards_enabled = db.Column(db.Boolean)
    VAC_enabled = db.Column(db.Boolean)
    workshop_enabled = db.Column(db.Boolean)

    def __repr__(self):
        return '<App %s - "Name No Longer Stored" (%s%s) | Type: %s | Multi: %s | Price: $%s | Windows: %s | Mac: %s | Linux: %s | Joy: %s | Metacritic: %s | %s>' % (self.app_id, self.size_mb, ' MB', self.app_type, self.multiplayer, self.store_price_default_usd, self.os_windows, self.os_mac, self.os_linux, self.controller_support, self.metascore, self.big_logo)


class Time_To_Beat(db.Model):
    __tablename__ = 'TIME_TO_BEAT'

    app_id = db.Column(db.Unicode(20), index=True, primary_key=True)
    data_imputed_completionist = db.Column(db.Boolean)
    data_imputed_extras = db.Column(db.Boolean)
    data_imputed_main_game = db.Column(db.Boolean)
    hltb_id = db.Column(db.Unicode(20))
    minutes_to_beat_completionist = db.Column(db.Integer)
    minutes_to_beat_extras = db.Column(db.Integer)
    minutes_to_beat_main_game = db.Column(db.Integer)
    timetobeat_api_raw = db.Column(db.Text)


class Genre_App_Map(db.Model):
    __tablename__ = 'GENRE_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    genres = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


class Developer_App_Map(db.Model):
    __tablename__ = 'DEVELOPER_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    developers = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


class Publisher_App_Map(db.Model):
    __tablename__ = 'PUBLISHER_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    publishers = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


class Language_App_Map(db.Model):
    __tablename__ = 'LANGUAGE_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    languages = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


class DLC_id_App_Map(db.Model):
    __tablename__ = 'DLC_ID_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    dlc_ids = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


def littleBobby():
    db.drop_all()


def createAll():
    db.create_all()

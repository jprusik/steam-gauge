import urllib.request as urllib2
import simplejson as json
from datetime import datetime
import math

# import other app scripts
import config
import model


def api_request(request_url):
    return json.load(urllib2.build_opener().open(urllib2.Request(request_url)))


def resolve_steam_vanity(username):
    vanity_resolve_api = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    key_query = ''.join(['?key=',config.API_KEY])
    format_query = '&format=json'
    vanity_query = '&vanityurl='

    json_get_steam_id = api_request('%(vanity_resolve_api)s%(key_query)s%(format_query)s%(vanity_query)s%(username)s' % locals())
    if json_get_steam_id['response']['success'] == 1:
        return json_get_steam_id['response']['steamid']
    else:
        return None


def get_user_metadata(user_id):
    user_metadata_api = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    key_query = ''.join(['?key=',config.API_KEY])
    format_query = '&format=json'
    steam_id_query = '&steamids='

    user_metadata = api_request('%(user_metadata_api)s%(key_query)s%(format_query)s%(steam_id_query)s%(user_id)s' % locals())
    return user_metadata


def get_user_app_list(user_id):
    user_apps_list_api = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    key_query = ''.join(['?include_played_free_games=1&include_appinfo=1&key=',config.API_KEY])
    steam_id_query = '&steamid='

    user_games = api_request('%(user_apps_list_api)s%(key_query)s%(steam_id_query)s%(user_id)s' % locals())
    return user_games


def get_steam_friends(user_id):
    user_friends_list_api = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
    key_query = ''.join(['?key=',config.API_KEY])
    steam_id_query = '&relationship=friend&format=json&steamid='

    user_friends = api_request('%(user_friends_list_api)s%(key_query)s%(steam_id_query)s%(user_id)s' % locals())
    return user_friends


def account_lookup(steam_user, api_format='py', request_type='account'):
    #API Model
    api_return = {'QueryStatus':{'error':False},'Account':{}}

    # if string is empty return 'no value passed' error
    if not steam_user:
        api_return['QueryStatus']['error'] = True
        api_return['QueryStatus']['error_message'] = 'No username was provided'
        return api_return

    steamID = ''

    # validate passed steam_user value
    if len(str(steam_user)) == 17 and str(steam_user).isdigit():
        steamID = str(steam_user)
    else:
        steamID = resolve_steam_vanity(steam_user)
        # if username can't be resolved via vanity resolution api at this point, then return error
        if steamID == None:
            api_return['QueryStatus']['error'] = True
            api_return['QueryStatus']['error_message'] = 'That account could not be found'
            return api_return

    # Check db for user first
    # if model_v2.Users.query.filter_by(user_id=str(steamID)).first():
    #     return model_v2.Users.query.filter_by(user_id=str(steamID)).first().attributes
        # user_query.last_update = datetime.now()

    user_summary = get_user_metadata(steamID)
    if len(user_summary['response']['players']) < 1:
        api_return['QueryStatus']['error'] = True
        api_return['QueryStatus']['error_message'] = 'That account could not be found'
        return api_return
    # Do a privacy setting check on the account
    if user_summary['response']['players'][0]['communityvisibilitystate'] == 1:
        api_return['Account']['account_public'] = False
        api_return['QueryStatus']['error'] = True
        api_return['QueryStatus']['error_message'] = 'That account is not publicly viewable'
        return api_return
    # If the account is public, set the user account info values
    else:
        api_return['Account'] = user_summary['response']['players'][0]
        api_return['Account']['UserApps'] = {'Apps':[]}

        # Convert timestamps to datetimes, since Jinja can't
        if str(api_return['Account']['timecreated']).isdigit():
            api_return['Account']['timecreated'] = datetime.fromtimestamp(api_return['Account']['timecreated'])
        if str(api_return['Account']['lastlogoff']).isdigit():
            api_return['Account']['lastlogoff'] = datetime.fromtimestamp(api_return['Account']['lastlogoff'])

    # Get account's gamelist
    user_games_page = get_user_app_list(steamID)

    if request_type == 'friends':
        api_return['least_common_game'] = []
        api_return['most_common_game'] = []
        api_return['most_played_game'] = []
        api_return['Account']['UserApps']['Apps'] = []

        user_friends = get_steam_friends(steamID)
        user_apps_list = []
        user_apps_multi = []
        user_friends_list = []

        # By filtering out non-multiplayer games here we can minimize lookups on each friend's account later
        for g in user_games_page['response']['games']:
            user_apps_list.append(str(g['appid']))
        user_multi_games = model.session.query(model.App).filter(model.App.app_id.in_(user_apps_list), model.App.multiplayer==True).all()
        for mg in user_multi_games:
            api_return['Account']['UserApps']['Apps'].append(mg.__dict__)
            user_apps_multi.append(mg.app_id)

        for f in user_friends['friendslist']['friends']:
            user_friends_list.append(f['steamid'])
        user_friends_query = ','.join(user_friends_list)
        user_friends_metadata = get_user_metadata(user_friends_query)
        api_return['Account']['Friends'] = user_friends_metadata['response']['players']

        for m in api_return['Account']['Friends']:
            # Convert timestamps to datetimes, since Jinja can't
            if m['communityvisibilitystate'] == 3:
                if str(m['timecreated']).isdigit():
                    m['timecreated'] = datetime.fromtimestamp(m['timecreated'])
                if str(m['lastlogoff']).isdigit():
                    m['lastlogoff'] = datetime.fromtimestamp(m['lastlogoff'])

            user_friend_apps = get_user_app_list(m['steamid'])
            user_friend_apps_list = []
            m['UserApps'] = {'Apps':[]}
            m['user_most_played_time'] = 0
            m['user_most_played_game'] = None

            # TODO: There's probably a more elegant way to do this check
            if 'games' in user_friend_apps['response']:
                for a in user_friend_apps['response']['games']:
                    user_friend_apps_list.append(str(a['appid']))
                    # m['UserApps']['Apps'].append(a)

                for n in set(user_friend_apps_list).intersection(user_apps_multi):
                    for o in user_friend_apps['response']['games']:
                        if n == str(o['appid']):
                            m['UserApps']['Apps'].append(o)

                            # check if this user played this app more than the current playtime leader app
                            if o['playtime_forever'] > m['user_most_played_time']:
                                m['user_most_played_time'] = o['playtime_forever']
                                m['user_most_played_game'] = o['name']
                            api_return['most_common_game'].append(o['name'])

            api_return['most_played_game'].append(m['user_most_played_game'])

        api_return['least_common_game'] = least_common(api_return['most_common_game'])
        api_return['most_common_game'] = most_common(api_return['most_common_game'])
        api_return['most_played_game'] = most_common(api_return['most_played_game'])

        return api_return

    else:
        # Pull data for each id, build the app object and append to proper key
        for x in user_games_page['response']['games']:

            app_data = get_app_data(x['appid'])

            if app_data['missing'] == True:
                app_data = {'missing':True,'app_id':str(x['appid']),'minutes_played':x['playtime_forever']}
                app_data['hours_played'] = math.ceil((float(app_data['minutes_played'])/60) * 100.0) / 100.0
            else:
                app_data['genres'] = get_app_genres(x['appid'])
                app_data['developers'] = get_app_developers(x['appid'])
                app_data['publishers'] = get_app_publishers(x['appid'])
                app_data['languages'] = get_app_languages(x['appid'])

                if app_data['size_mb'] and app_data['size_mb'] > 0:
                    app_data['size_gb'] = math.ceil((float(app_data['size_mb'])/1000) * 10.0) / 10.0
                else:
                    app_data['size_mb'] = 0
                    app_data['size_gb'] = 0

                app_data['minutes_played'] = x['playtime_forever']
                app_data['hours_played'] = math.ceil((float(app_data['minutes_played'])/60) * 100.0) / 100.0

                # Figure out price/hours ratio
                if app_data['hours_played'] >= 1 and app_data['store_price_default_usd'] is not None:
                    app_data['price_hours'] = math.ceil(float(app_data['store_price_default_usd']/app_data['hours_played']) * 100.0) / 100.0
                # elif app_data['hours_played'] == float(0) and app_data['store_price_default_usd'] is not None:
                #     app_data['price_hours'] = math.ceil(float(app_data['store_price_default_usd']) * 100.0) / 100.0
                else:
                    app_data['price_hours'] = ''
                # app_data['price_hours'] = 0

            api_return['Account']['UserApps']['Apps'].append(app_data)

    api_return['Account']['UserApps']['app_count'] = len(api_return['Account']['UserApps']['Apps'])

    # Dump python dict to json if the function was initiated by API call
    # if api_format == 'json':
    #     return json.dumps(api_return)
    # else:
        # Save user info as blob for short-term caching
        # try:
        #     if model_v2.Users.query.filter_by(user_id=api_return['Account']['user_64id']).first():
        #         user_query = model_v2.Users.query.filter_by(user_id=api_return['Account']['user_64id']).first()
        #         user_query.last_update = datetime.now()
        #         user_query.attributes = api_return
        #     else:
        #         model_v2.Users(user_id=api_return['Account']['user_64id'], attributes=api_return, last_update=datetime.now())
        #     model_v2.session.commit()
        # except:
        #     model_v2.session.rollback()

        # return api_return

    return api_return


def all_games_account():
    #API Model
    api_return = {'QueryStatus':{'error':False,'error_message':''},'Account':{'user_64id':'0','user_persona':'test_user','user_realname':'Test User','user_country':'XX','user_state':'XX','user_cityid':'XX','user_primary_group':'','user_avatar_small':'','user_avatar_medium':'','user_avatar_large':'','user_account_link':'','account_public':'','account_creation_datetime':'','current_status':'','current_app_id':'','current_app_title':'','last_logoff_datetime':'','UserApps':{'app_count':'','Apps':[]}}}

    # Get account's gamelist
    user_games_page = json.load(urllib2.build_opener().open(urllib2.Request('http://api.steampowered.com/ISteamApps/GetAppList/v2/')))

    for x in user_games_page['response']['games']:

        app_data = get_app_data(x['appid'])

        if app_data['missing'] == True:
            app_data = {'missing':True,'app_id':str(x['appid']),'minutes_played':x['playtime_forever']}
            app_data['hours_played'] = math.ceil((float(app_data['minutes_played'])/60) * 100.0) / 100.0
        else:
            app_data['genres'] = get_app_genres(x['appid'])
            app_data['developers'] = get_app_developers(x['appid'])
            app_data['publishers'] = get_app_publishers(x['appid'])
            app_data['languages'] = get_app_languages(x['appid'])

            if app_data['size_mb'] > 0:
                app_data['size_gb'] = math.ceil((float(app_data['size_mb'])/1000) * 10.0) / 10.0
            else:
                app_data['size_mb'] = 0
                app_data['size_gb'] = 0

            app_data['minutes_played'] = 42
            app_data['hours_played'] = math.ceil((float(app_data['minutes_played'])/60) * 100.0) / 100.0

            # Figure out price/hours ratio
            if app_data['hours_played'] >= 1 and app_data['store_price_default_usd'] is not None:
                app_data['price_hours'] = math.ceil(float(app_data['store_price_default_usd']/app_data['hours_played']) * 100.0) / 100.0
            else:
                app_data['price_hours'] = ''

        api_return['Account']['UserApps']['Apps'].append(app_data)

    api_return['Account']['UserApps']['app_count'] = len(api_return['Account']['UserApps']['Apps'])

    return api_return


def get_app_data(pid):
    pid = str(pid)
    query = model.session.query(model.App).filter_by(app_id=pid).first()
    if query:
        app_data = query.__dict__
        app_data['missing'] = False

        # There's probably a better way to do this, but we don't need these keys
        del app_data['_sa_instance_state']
        del app_data['big_picture_api_raw']

        return app_data
    else:
        return {'missing':True}


def get_app_genres(pid):
    pid = str(pid)
    genres = []
    for g in model.session.query(model.Genre_App_Map).filter_by(apps=pid).all():
        genres.append(g.genres)
    return genres


def get_app_developers(pid):
    pid = str(pid)
    developers = []
    for d in model.session.query(model.Developer_App_Map).filter_by(apps=pid).all():
        developers.append(d.developers)
    return developers


def get_app_publishers(pid):
    pid = str(pid)
    publishers = []
    for p in model.session.query(model.Publisher_App_Map).filter_by(apps=pid).all():
        publishers.append(p.publishers)
    return publishers


def get_app_languages(pid):
    pid = str(pid)
    languages = []
    for l in model.session.query(model.Language_App_Map).filter_by(apps=pid).all():
        languages.append(l.languages)
    return languages


def most_common(lst):
    if len(lst) < 1:
        return None
    else:
        return max(set(lst), key=lst.count)


def least_common(lst):
    if len(lst) < 1:
        return None
    else:
        return min(set(lst), key=lst.count)

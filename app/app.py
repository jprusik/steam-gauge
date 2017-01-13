from json import dumps, loads
from flask import Flask, url_for, redirect, request, Markup, render_template, make_response, session, flash, g
from urllib.request import quote
from urllib.parse import urlencode
from collections import OrderedDict
import model, config, datetime

app = Flask(__name__)
app.config.from_object('config')

# explicitly disable debug in production
app.debug = config.DEBUG_ACTIVE_P

app.secret_key = config.APP_SECRET

import account_api


def clear_session():
    session['account_id'] = None
    session['admin_p'] = False
    session['last_action'] = None
    session['session_start'] = None
    session['full_response'] = None
    # using session.clear() nulls everything, including the session object itself, so you have to check for session AND session['account_id'] or pop(None) individual session keys
    # session.clear()


@app.before_request
def before_request():
    if session and session['account_id']:
        # If more than x minutes have passed since the last time the user did anything, log them out
        minutes_expire = 720
        if (datetime.datetime.now()-session['last_action']).seconds > (minutes_expire*60):
            clear_session()
        else:
            # check anything that might have changed
            if session['account_id'] in config.ADMIN_USERS:
                session['admin_p']=True
            else:
                session['admin_p']=False
            session['last_action'] = datetime.datetime.now()
    else:
        clear_session()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/friends', methods=['GET'])
def friends():
    # error = None
    searchword = request.args.get('username', '')
    if searchword == '':
        # TODO: fix this redirection logic. Attempts to pass null value for username should go to the error page. Move this search to main homepage.
        return render_template('friends-home.html')
    else:
        api_accounts = account_api.account_lookup(searchword, request_type='friends')
        if api_accounts['QueryStatus']['error'] == True:
            return render_template('error.html', error_code='app', error_message=api_accounts['QueryStatus']['error_message'])
        return render_template('friends.html', api_return=api_accounts)


@app.route('/account', methods=['GET'])
def account():
    searchword = request.args.get('username', '')
    if searchword == '':
        return render_template('error.html', error_code='app', error_message='No username was provided')
    else:
        api_accounts = account_api.account_lookup(searchword)
        if api_accounts['QueryStatus']['error'] == True:
            return render_template('error.html', error_code='app', error_message=api_accounts['QueryStatus']['error_message'])
        return render_template('account.html', api_return=api_accounts)


# @app.route('/admin')
# def admin_index():
#     if session['admin_p'] == True:
#         api_accounts = account_api.all_games_account()
#         return render_template('account.html', api_return=api_accounts)
#     else:
#         return render_template('error.html')


# This is the old account summary path - redirect to new
@app.route('/search', methods=['GET'])
def search():
    searchword = request.args.get('username', '')
    return redirect('/account?username='+searchword, code=302)


@app.route('/login')
def login():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.mode': 'checkid_setup',
        'openid.return_to': config.DOMAIN_URL+'/authorize',
        'openid.realm': config.DOMAIN_URL
    }
    query_string = urlencode(params)
    auth_url = 'https://steamcommunity.com/openid/login?'+query_string
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    # print request.args
    response = dumps(request.args['openid.identity'])
    session['account_id'] = response.split('/')[-1].strip('"')
    session['session_start'] = datetime.datetime.now()
    session['last_action'] = datetime.datetime.now()
    if session['account_id'] in config.ADMIN_USERS:
        session['admin_p'] = True
    return redirect('/')


# @app.route('/api', methods=['GET'])
# def api():
#     searchword = request.args.get('username', '')
#     if searchword == '':
#         return render_template('account_api.html', api_return=api_accounts)
#     else:
#         api_accounts = account_api.account_lookup(searchword, True)
#         return api_accounts
#         # return render_template('account_api.html', api_return=api_accounts)


@app.route('/logout')
def logout():
    clear_session()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code='404', error_message='Page not found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    if session['account_id'] in config.ADMIN_USERS:
        return render_template('error.html', error_code='500', error_info='The server had a problem: '+error.args), 500
    else:
        return render_template('error.html', error_code='500', error_info='The server had a problem'), 500


@app.errorhandler(504)
def gateway_timeout(error):
    if session['account_id'] in config.ADMIN_USERS:
        return render_template('error.html', error_code='504', error_info='The request took too long: '+error.args), 504
    else:
        return render_template('error.html', error_code='504', error_info='The request took too long'), 504


# # What version of python is active?
# import sys
# @app.route('/pyversion')
# def pyversion():
#     return sys.version


if __name__ == '__main__':
    app.run()

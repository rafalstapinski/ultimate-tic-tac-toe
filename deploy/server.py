import web
import json
import os

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = "/etc/letsencrypt/live/rupreceptorials.com/fullchain.pem"
CherryPyWSGIServer.ssl_private_key = "/etc/letsencrypt/live/rupreceptorials.com/privkey.pem"


urls = (
    '/p/uttt/api/game/new', 'api_game_new',
    '/p/uttt/api/game/update', 'api_game_update',
    '/p/uttt/api/game/move', 'api_game_move',
    '/p/uttt', 'route_index',
    '/p/uttt/', 'route_index',
    '/p/uttt/game', 'route_game',
    '/p/uttt/res', 'route_res'
)

class route_res:
    def GET(self):

        i = web.input()

        try:
            f = open(os.path.join(__location__, 'static/res', i['f']))
            res = f.read()
            f.close()

            return res
        except:
            return notfound()


class api_game_move:
    def POST(self):

        new_api(self)

        i = web.input()

        try:
            game_name = i['game_name'].encode('utf-8')
            local = int(i['local'])
            cell = int(i['cell'])
            player = i['player'].encode('utf-8')
        except KeyError:
            return write({'message': 'data not provided'}, 400)
        except UnicodeError:
            return write({'message': 'input must be utf-8 encoded'}, 400)
        except ValueError:
            return write({'message': 'input must be integer'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        if player != 'x' and player != 'o':
            return write({'message': 'you\'re probably playing the wrong game'}, 400)

        if (cell < 0 and cell > 8) or (local < 0 and local > 8):
            return write ({'message': 'this must be some wackier version of ttt'}, 400)

        params = dict(game_name=game_name)

        try:
            game = db.select('games', params, where='game_name = $game_name').list()[0]
        except IndexError:
            return write({'message': 'game not found'}, 404)
        except:
            return write({'message': 'something went wrong'}, 500)

        if game.status == 'ended':
            return write({'message': 'you are too late to the party!'}, 403)

        params = dict(game_id=game.id)
        try:
            log = db.select('log', params, where='game_id = $game_id', order='id DESC', limit=1).list()[0]
        except:
            return write({'message': 'something went wrong'}, 500)

        if player == log.player:
            return write({'message': 'not your turn!'}, 403)

        state = json.loads(log.state)
        board = json.loads(log.board)

        if board[local] is not None:
            return write({'message': 'this local board is already taken!'}, 403)
        elif state[local][cell] is not None:
            return write({'message': 'this cell is already taken!'}, 403)

        if log.next_local_has_to_be is not None: # is this the best way of avoiding int(None)
            if local != int(log.next_local_has_to_be):
                return write({'message': 'this is not the local board you are looking for!'}, 403)

        new_state = state
        new_state[local][cell] = player

        new_board = board

        for i in range(9):
            if board[i] is None:
                print eval_ttt(new_state[i])
                new_board[i] = eval_ttt(new_state[i])

        winner = eval_ttt(new_board)

        if winner is not None:
            db.update('games', vars=params, where='id = $game_id', status='ended', winner=winner)

        if new_board[cell] is not None:
            next_local_has_to_be = None
        else:
            next_local_has_to_be = cell

        move = '%s,%s' % (local, cell)

        db.insert('log', game_id=game.id, player=player, move=move, state=json.dumps(new_state), next_local_has_to_be=next_local_has_to_be, board=json.dumps(new_board))

        return write({'message': 'you made your turn!'}, 200)

def eval_ttt(ttt):

    if (ttt[0] is not None and ttt[0] == ttt[1] and ttt[1] == ttt[2]):
        return ttt[0]
    if (ttt[3] is not None and ttt[3] == ttt[4] and ttt[4] == ttt[5]):
        return ttt[3]
    if (ttt[6] is not None and ttt[6] == ttt[7] and ttt[7] == ttt[8]):
        return ttt[6]
    if (ttt[0] is not None and ttt[0] == ttt[3] and ttt[3] == ttt[6]):
        return ttt[0]
    if (ttt[1] is not None and ttt[1] == ttt[4] and ttt[4] == ttt[7]):
        return ttt[1]
    if (ttt[2] is not None and ttt[2] == ttt[5] and ttt[5] == ttt[8]):
        return ttt[2]
    if (ttt[0] is not None and ttt[0] == ttt[4] and ttt[4] == ttt[8]):
        return ttt[0]
    if (ttt[2] is not None and ttt[2] == ttt[4] and ttt[2] == ttt[6]):
        return ttt[2]

    if None not in ttt:
        return 'n'

    return None


class route_game:
    def GET(self):

        i = web.input()

        try:
            game_name = i['game_name'].encode('utf-8')
            player = i['player'].encode('utf-8')
        except:
            raise web.seeother('/p/uttt')

        if player != 'x' and player != 'o':
            raise web.seeother('/p/uttt')

        params = dict(game_name=game_name)

        results = db.select('games', params, where='game_name = $game_name').list()

        if len(results) == 0:
            raise web.seeother('/p/uttt')
        elif len(results) == 1:
            game = results[0]
            if game.status == 'ended':
                raise web.seeother('/p/uttt')
        else:
            raise web.seeother('/p/uttt')

        f = open(os.path.join(__location__, 'static/game.html'))
        html = f.read()
        f.close()

        return html

class api_game_update:
    def POST(self):

        new_api(self)
        i = web.input()

        try:
            game_name = i['game_name'].encode('utf-8')
            user_log_id = int(i['log_id'])
        except KeyError:
            return write({'message': 'game_name or id not provided'}, 400)
        except UnicodeError:
            return write({'message': 'input must be utf-8 encoded'}, 400)
        except ValueError:
            return write({'message': 'input must be integer'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        params = dict(game_name=game_name)

        try:
            game = db.select('games', params, where='game_name = $game_name').list()[0]
        except IndexError:
            return write({'message': 'game not found'}, 404)
        except:
            return write({'message': 'something went wrong'}, 500)

        params = dict(game_id=game.id)
        try:
            log = db.select('log', params, where='game_id = $game_id', order='id DESC', limit=1).list()[0]
        except:
            return write({'message': 'something went wrong'}, 500)


        if log.id > user_log_id:
            player = 'x' if log.player == 'o' else 'o'
            state = json.loads(log.state)

            if game.status == 'ended':
                return write({'winner': game.winner, 'log_id': log.id, 'board': json.loads(log.board), 'state': state, 'player': player, 'next_local_has_to_be': log.next_local_has_to_be}, 200)

            return write({'log_id': log.id, 'board': json.loads(log.board), 'state': state, 'player': player, 'next_local_has_to_be': log.next_local_has_to_be}, 200)

        return write({'message': 'log up to date'}, 204)


class route_index:
    def GET(self):
        f = open(os.path.join(__location__, 'static/index.html'))
        html = f.read()
        f.close()
        return html

class api_game_new:
    def POST(self):

        new_api(self)
        i = web.input()

        try:
            game_name = i['game_name'].encode('utf-8')
        except KeyError:
            return write({'message': 'game_name not provided'}, 400)
        except UnicodeError:
            return write({'message': 'inputs must be utf-8 encoded'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        params = dict(game_name=game_name)

        results = db.select('games', params, where='game_name = $game_name')

        for result in results:
            return write({'message': 'game of that name already exists'}, 403)

        game_id = db.insert('games', game_name=game_name, status='running')

        new_state = json.dumps([[None for x in range(9)] for y in range(9)])
        board = json.dumps([None for x in range(9)])

        db.insert('log', state=new_state, board=board, game_id=game_id, player='o', move=None, next_local_has_to_be=None)

        return write({'game_name': game_name}, 200)

def write(payload, status):
    return json.dumps({'payload': payload, 'status': status})

def notfound():
    return web.notfound('404')

def new_api(request):
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')

def new_page(request):
    web.header('Content-Type', 'text/html')
    web.header('Access-Control-Allow-Origin', '*')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
dbname = os.path.realpath(os.path.join(__location__, 'utt.db'))
db = web.database(dbn='sqlite', db=dbname)

app = web.application(urls, globals())
app.notfound = notfound
application = app.wsgifunc()

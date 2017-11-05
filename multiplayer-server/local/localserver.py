import web
import json
import os

urls = (
    '/api/game/new', 'api_game_new',
    '/api/game/update', 'api_game_update',
    '/api/game/move', 'api_game_move',
    '/', 'route_index',
    '/game', 'route_game',
)

# api endpoint to register new move

class api_game_move:
    def POST(self):

        new_api(self)

        i = web.input()

        # validate input

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

        # if invalid player

        if player != 'x' and player != 'o':
            return write({'message': 'you\'re probably playing the wrong game'}, 400)

        # if invalid cell

        if (cell < 0 and cell > 8) or (local < 0 and local > 8):
            return write ({'message': 'this must be some wackier version of ttt'}, 400)

        # get game

        params = dict(game_name=game_name)

        try:
            game = db.select('games', params, where='game_name = $game_name').list()[0]
        except IndexError:
            return write({'message': 'game not found'}, 404)
        except:
            return write({'message': 'something went wrong'}, 500)

        # check if ended

        if game.status == 'ended':
            return write({'message': 'the game is over!'}, 403)

        # get most recent log of the game

        params = dict(game_id=game.id)
        try:
            log = db.select('log', params, where='game_id = $game_id', order='id DESC', limit=1).list()[0]
        except:
            return write({'message': 'something went wrong'}, 500)

        # if not your turn

        if player == log.player:
            return write({'message': 'not your turn!'}, 403)

        state = json.loads(log.state)
        board = json.loads(log.board)

        # validate move

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

        # check if any of the local boards are done

        for i in range(9):
            if board[i] is None:
                print eval_ttt(new_state[i])
                new_board[i] = eval_ttt(new_state[i])

        # check if the global board is done

        winner = eval_ttt(new_board)

        if winner is not None:
            db.update('games', vars=params, where='id = $game_id', status='ended', winner=winner)

        if new_board[cell] is not None:
            next_local_has_to_be = None
        else:
            next_local_has_to_be = cell

        move = '%s,%s' % (local, cell)

        # update log

        db.insert('log', game_id=game.id, player=player, move=move, state=json.dumps(new_state), next_local_has_to_be=next_local_has_to_be, board=json.dumps(new_board))

        return write({'message': 'you made your turn!'}, 200)

    # function to evaluate if the array representing a board (local/global)
    # has three in a row/diagonal for either o/x or if is full

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

# api endpoint to return any updated log of the board

class api_game_update:
    def POST(self):

        new_api(self)
        i = web.input()

        # validate input

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

        # if user has old log, return necessary info

        if log.id > user_log_id:
            player = 'x' if log.player == 'o' else 'o'
            state = json.loads(log.state)

            if game.status == 'ended':
                return write({'winner': game.winner, 'log_id': log.id, 'board': json.loads(log.board), 'state': state, 'player': player, 'next_local_has_to_be': log.next_local_has_to_be}, 200)

            return write({'log_id': log.id, 'board': json.loads(log.board), 'state': state, 'player': player, 'next_local_has_to_be': log.next_local_has_to_be}, 200)

        return write({'message': 'log up to date'}, 204)

# create a new game in the database

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

# serve game.html

class route_game:
    def GET(self):

        i = web.input()

        try:
            game_name = i['game_name'].encode('utf-8')
            player = i['player'].encode('utf-8')
        except:
            raise web.seeother('/')

        if player != 'x' and player != 'o':
            raise web.seeother('/')

        params = dict(game_name=game_name)

        results = db.select('games', params, where='game_name = $game_name').list()

        if len(results) == 0:
            raise web.seeother('/')
        elif len(results) == 1:
            game = results[0]
            if game.status == 'ended':
                raise web.seeother('/')
        else:
            raise web.seeother('/')

        f = open(os.path.join(__location__, 'static/game.html'))
        html = f.read()
        f.close()

        return html

# serve index

class route_index:
    def GET(self):
        f = open(os.path.join(__location__, 'static/index.html'))
        html = f.read()
        f.close()
        return html

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

if __name__ == '__main__':
    app = web.application(urls, globals())
    web.config.debug = False
    app.notfound = notfound
    app.run()

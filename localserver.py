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

class api_game_move:
    def POST(self):

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

        params = dict(game_id=game.id)
        try:
            log = db.select('log', params, where='game_id = $game_id', order='id DESC', limit=1).list()[0]
        except:
            return write({'message': 'something went wrong'}, 500)

        if player == log.player:
            return write({'message': 'not your turn!'}, 403)

        state = json.loads(log.state)

        if board[local] is not None:
            return write({'message': 'this local board is already taken!'}, 403)
        elif state[local][cell] is not None:
            return write({'message': 'this cell is already taken!'}, 403)

        if log.next_local_has_to_be is not None:
            if local != int(log.next_local_has_to_be):
                return write({'message': 'this is not the local board you are looking for!'}, 403)

        new_state = state
        new_state[local][cell] = player

        if state[]

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

            return write({'log_id': log.id, ' board', log.board, 'state': state, 'player': player, 'next_local_has_to_be': log.next_local_has_to_be}, 200)

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
db = web.database(dbn='sqlite', db='utt.db')

if __name__ == '__main__':
    app = web.application(urls, globals())
    web.config.debug = False
    app.notfound = notfound
    app.run()

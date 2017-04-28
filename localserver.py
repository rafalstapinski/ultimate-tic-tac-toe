import web
import json
import os

urls = (
    '/api/game/new', 'api_game_new',
    '/', 'route_index',
    '/game', 'route_game',
)

class route_game:
    def GET(self):
        i = web.input()

        try:
            game_name = i['name'].encode('utf-8')
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

        params = dict(game_id=game.id)

        results = db.select('log', params, where='game_id = $game_id').list()

        turn = 'x' if len(results) % 2 == 0 else 'o'
        state = json.loads(results['state'])

        if len(results) == 0:
            return write({'payload': {'state': state}}, 200)



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

        db.insert('log', state=new_state, game_id=game_id, player='o', move=None, next_local_has_to_be=None)

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
    app.notfound = notfound
    app.run()

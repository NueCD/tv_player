import cgi
from wsgiref.simple_server import make_server

html = '''
<html>
    <head>
        <title>Add to tv queue</title>
    </head>
    <body>
        <p>Add link to queue. Youtube and Twitch links work. Make sure the "http/https" part is present. You can also type Twitch channel names.</p>
        <form method="post">
            <label>Link</label>
            <input type="text" name="item">
            <input type="submit" value="Add">
        </form>
        <!--ADDED_TEXT-->
    </body>
</html>
'''

queue = 'queue'

def app(environ, start_response):
    response = html
    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )

        link = post['item'].value
        # If link is no real website assume it is a Twitch channel.
        if 'http' not in link:
            link = 'https://twitch.tv/' + link
            response = html.replace('<!--ADDED_TEXT-->', 'Twitch channel was added to queue.')
        
        else:
            response = html.replace('<!--ADDED_TEXT-->', 'Link was added to queue.')

        # Add link to queue.
        with open(queue, 'a') as f:
            f.write(link + '\n')

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [bytes(response, 'utf-8')]

print('Starting web server.')
httpd = make_server('', 80, app)
httpd.serve_forever()

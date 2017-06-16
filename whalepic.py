import flask, os
app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

    # gather all images
    images = []
    all_tags = set([])
    for dirpath, dirnames, filenames in os.walk("./static/image-repo"):

        for filename in [f for f in filenames if (f.endswith(".jpg") or f.endswith(".png"))  ]:
            tags = parse_tags(os.path.join(dirpath, 'tags'))
            style = ''
            for tag in tags:
                if tag[:5] != '!CSS!':
                	all_tags.add(tag)
                else:
                    style = tag[5:]
            image = {
                'name': filename,
                'dir': dirpath[20:],
                'relpath': os.path.join(dirpath, filename)[9:],
                'class': ' '.join(tags),
                'style': style
            }
            images.append(image)
        
    all_tags = list(all_tags)
    all_tags = sorted(all_tags)

    return flask.render_template('index.html', images=images, tags=list(all_tags))

@app.route('/<dir>/<name>')
def pic(dir, name):

    hostpath = os.environ['HOST_PIC_PATH']
    #f = open('/app/static/image-repo/' + dir+'/tags', 'r')
    tags = parse_tags('/app/static/image-repo/' + dir+'/tags')
    style = ''
    if tags[0].startswith('!CSS!'):
        style = tags[0][5:]

    return flask.render_template('pic.html', hostpath=hostpath, dir=dir, name=name, style=style )




def parse_tags(path):
	# given the path to a tags file, chew it up into a list

	with open(path) as f:
	    content = f.readlines()
	content = [x.strip() for x in content] 

	return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
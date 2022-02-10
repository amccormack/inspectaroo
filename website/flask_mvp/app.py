from flask import Flask, request, redirect, url_for
import boto3
import hashlib
import json

app = Flask(__name__)

BUCKET='inspectaroo-app'
PREFIX='inbox'
EXIF_PREFIX='exifdata'

@app.route('/')
def hello():
    return '''<html><head><title>Welcome</title></head>
    <body>
        <div>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit"/>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/results/<name>')
def results(name):
    key = f'{EXIF_PREFIX}/{name}.exif.json'
    s3 = boto3.client('s3')
    try:
        f = s3.get_object(Bucket=BUCKET, Key=key)
        resp = json.loads(f['Body'].read())
        content = f'''<pre>{json.dumps(resp, indent=2)}</pre>'''
    except Exception as e:
        content = f'''<p>No content yet.<a href="/results/{name}">Refresh</a>.</p>'''
    body = f'''<html><head><title>Results</title></head>
    <body>
        <div>
        {content}
        </div>
        <div>
        <a href="/">Home</a>
        </div>
    </body>
    </html>
    '''
    return body

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return 'bad'
    t = file.read()
    digest = hashlib.md5(t).hexdigest()
    filename = f'{digest}_{file.filename}'
    key = f'{PREFIX}/{filename}'
    s3 = boto3.client('s3')
    s3.put_object(Body=t, Bucket=BUCKET, Key=key)
    return redirect(url_for('results', name=filename))


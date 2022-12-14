from scrapper import final
from flask import Flask,render_template,request,send_file,redirect, url_for
import os,random
from flask_minify import Minify

#print(platform.system(),os.system('cat /proc/version'))
app = Flask(__name__)
Minify(app=app, html=True, js=True, cssless=True)
app.config['SECRET_KEY'] = 'nothing'

#Folders
app.config['SS_IMAGES'] = 'static/ss_imgs'
app.config['SS_AUDIOES'] = 'static/ss_audioes'
app.config['OUTPUT'] = 'static/output'

def check():
    if os.path.exists('static/output') and os.path.exists('static/ss_imgs') and os.path.exists('static/ss_audioes'):
        if  len(os.listdir('static/output'))>0 and len(os.listdir('static/ss_imgs'))>0:
            empty_dir('static/ss_imgs')
            empty_dir('static/ss_audioes')
            empty_dir('static/output')

def create_dirs():
    if os.path.exists('static/output')==False:
        os.mkdir('static/output')
    if os.path.exists('static/ss_audioes')==False:
        os.mkdir('static/ss_audioes')
    if os.path.exists('static/ss_imgs')==False:
        os.mkdir('static/ss_imgs')

@app.route("/")
def index():
    check()
    return render_template("home.html",title='Home')

@app.route("/home")
def home():
    check()
    return render_template("home.html",title='Home')

@app.route("/how")
def how():
    check()
    return render_template("how.html",title="How it works")

@app.route("/ran")
def auto():
    return render_template("auto.html",title="Auto Mode")

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error.html',title="Error")

@app.errorhandler(500)
def pageNotFound(error):
    return render_template('error.html',title="Error")

@app.route("/ranproc")
def atproc():
    create_dirs()
    flag =False
    qlist = ["what","when","whom","which","why","how","is","was","will","has","have","had"]
    global q
    q = random.sample(qlist,1)[0]
    print(q)
    if len(os.listdir('static/output'))==0:
        flag = True
    return render_template("proc.html",title='Processing',fpath='../static/loading.gif',flag=flag)

@app.route("/proc",methods=['POST','GET'])
def proc():
    create_dirs()
    try:
        flag =False
        if request.method=="POST":
            form_data=request.form
            if form_data['query']:
                global q
                q = form_data['query']
                if ' ' in q:
                    q = q.replace(' ','%20')
                if len(os.listdir('static/output'))==0:
                    flag = True
                return render_template("proc.html",title='Processing',fpath='../static/loading.gif',flag=flag)
        else:
            return redirect(url_for('home'))
    except:
        return redirect(url_for('error'))         

@app.route("/download")
def download():
    if q:
        final(query=q)
        if q in ["what","when","whom","which","why","how","is","was","will","has","have","had"]:
            return render_template("download.html",title='Download',fpath = f'../static/output/auto.mp4')
        else:
            qs=q.replace('%20','_')
            return render_template("download.html",title='Download',fpath = f'../static/output/{qs}.mp4')
    else:
        return 'Error'   

@app.route('/link')
def link():
    if len(os.listdir('static/output'))==1:
        return send_file(os.path.join('static/output',os.listdir('static/output')[0]),as_attachment=True)
    #else:
        #return redirect(url_for('home'))

@app.route("/about")
def samps():
    return render_template("about.html",title="About")

@app.route("/err")
def error():
    return render_template("error.html",title="Error")

def empty_dir(dirpath):
    for i in os.listdir(dirpath):
        os.remove(f'{dirpath}/{i}')
    os.rmdir(dirpath)

if __name__ == "__main__":
    app.run()
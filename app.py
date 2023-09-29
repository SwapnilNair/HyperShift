#Imports
#Copyright - Swapnil Nair
'''TKINTER'''
import tkinter as tk
import qrcode
import pyqrcode

'''FLASK'''
from flask_dropzone import Dropzone
from flask import Flask, render_template, redirect, url_for, request, session,Response,send_file,abort
import os,threading,time,socket

'''GUNCIORN'''
import gunicorn.app.base
class StandaloneApplication(gunicorn.app.base.BaseApplication):

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.debug=False
app.use_reloader = False
app.config.update(
    UPLOADED_PATH= '/home/swapnilsnair/HyperShift',
    DROPZONE_MAX_FILE_SIZE = 402400,
    DROPZONE_TIMEOUT = 5*60*10000,
    CREATE_IMAGE_THUMBNAILS = False,
    ALLOWED_EXTENSIONS = set(['hdf5','.hdf5','.py','h5py','.h5','h5','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','apk','.apk']))
dropzone = Dropzone(app)

#Config for the flask routing
@app.route('/', defaults={'req_path': ''},  methods=['GET','POST'])
@app.route('/<path:req_path>')
def home(req_path):
    if request.method == 'GET':
        BASE_DIR = '/home/swapnilsnair/'
        abs_path = os.path.join(BASE_DIR, req_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = sorted(os.listdir(abs_path))
        return render_template('home.html', files=files)
        
    if request.method == 'POST':
        filee = request.files.get('file')
        filee.save(os.path.join(app.config['UPLOADED_PATH'],str(int(time.time()) )+'_'+filee.filename ) )
        return redirect('/')


#Config for the tkinter object
class Config():
    def __init__(self,root):
        root.title("HyperShift")
        
        #Main window dimensions
        window_height = 600
        window_width = 600
        
        #Resize option
        root.resizable(False,False)

        #Dimensions of the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        #Setting co-ordinates to be the center of the axes
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        
        #Setting the window geometry and offset
        win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        



if __name__=='__main__':
    win = tk.Tk() 
    Config(win)

    #Getting current IP
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    portno = 4700
    #The label for the QR code //What a pain
    
    l1=tk.Label(win,text='Potato')
    l1.place(relx = 0.5,rely = 0.5,anchor='center')
    my_qr = pyqrcode.create(f"http://{ip_address}:{portno}/") 
    my_qr = my_qr.xbm(scale=10)
    my_img=tk.BitmapImage(data=my_qr)
    l1.config(image=my_img) 
    number_of_workers = 9
    #WSGI config
    options = {
            'bind': '%s:%s' % (hostname, portno),
            'workers': number_of_workers,
            # 'threads': number_of_workers(),
            'timeout': 120,
        }
    #initialize()

    #Run flask
    #flaskthread = threading.Thread(target=StandaloneApplication(app, options).run).start() 
    
    #Looping for tkinter
    try:
        win.mainloop()
        StandaloneApplication(app, options).run()
    except:
        pass
    
    #Looping for tkinter
    #win.mainloop()

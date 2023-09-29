#Imports
#Copyright - Swapnil Nair

import os,threading,time,socket
'''TKINTER'''
import tkinter as tk
import pyqrcode

'''FLASK'''
from flask_dropzone import Dropzone
from flask import Flask, render_template, redirect,  request,send_file,abort

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.debug=False
app.use_reloader = False
app.config.update(
    UPLOADED_PATH= '/home/swapnilsnair/HyperShift',
    DROPZONE_MAX_FILE_SIZE = 102400,
    DROPZONE_TIMEOUT = 5*60*10000,
    DROPZONE_PARALLEL_UPLOADS = True,
    #DROPZONE_UPLOAD_MULTIPLE = True,
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','apk','.apk']))
dropzone = Dropzone(app)

#Config for the flask routing
@app.route('/', defaults={'req_path': ''},  methods=['GET','POST'])
@app.route('/<path:req_path>')
def home(req_path):
    if request.method == 'GET':
        BASE_DIR = '/home/swapnilsnair/'
        abs_path = os.path.join(BASE_DIR, req_path)
        print(abs_path)      
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

    #Run flask
    flaskthread = threading.Thread(target=lambda: app.run(port = portno,host=ip_address)).start() 
    
    #Looping for tkinter
    win.mainloop()


    
    #Looping for tkinter
    #win.mainloop()

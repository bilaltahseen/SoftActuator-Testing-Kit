
import csv
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import argparse
import cv2
from PIL import Image, ImageTk
import numpy as np
import serial
import datetime
style.use('ggplot')

global ser
ser = None


class NewprojectApp:
    xdata, ydata = [], []
    bendingSWFlag = True
    deflateSWFlag = True
    scaleFactor = 1.4
    count = 0
    num = 0
    start = False

    def __init__(self, master=None):
        # build ui
        self.style = ttk.Style()
        self.style.configure('START.TButton', font=('Arial', 14, 'bold'),
                             foreground='green')
        self.style.configure('STOP.TButton', font=('Arial', 14, 'bold'),
                             foreground='red')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 0.7*320*self.scaleFactor)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 0.7*280*self.scaleFactor)
        self.frame_3 = ttk.Frame(master)
        self.label_4_5 = ttk.Label(self.frame_3)
        self.label_4_5.config(
            font='{Arial} 20 {bold}', justify='left', padding='2 10', text='Soft Actuator')
        self.label_4_5.pack(side='top')
        self.label_6 = ttk.Label(self.frame_3)
        self.label_6.config(
            background='#008000', font='{Arial} 12 {bold}', foreground='#ffffff', padding='2')
        self.label_6.config(text='Connected')
        self.label_6.pack(side='top')
        self.frame_4 = ttk.Frame(self.frame_3)
        self.frame_4.config(height='10', width='200')
        self.frame_4.pack(side='top')

        self.labelframe_1_2 = ttk.Labelframe(self.frame_3)
        self.label_1 = ttk.Label(self.labelframe_1_2)
        self.label_1.config(text='Test Name')
        self.label_1.pack(padx='10', side='left')
        self.button_2 = ttk.Button(
            self.labelframe_1_2, command=self.stopRecord)
        self.button_2.config(style='STOP.TButton',
                             text='Stop', state='disabled')
        self.button_2.pack(side='right')
        self.button_1 = ttk.Button(
            self.labelframe_1_2, command=self.startRecord)
        self.button_1.config(style='START.TButton', text='Start')
        self.button_1.pack(padx='10', side='right')
        self.entry_1 = ttk.Entry(self.labelframe_1_2)
        _text_ = '''entry_1'''
        self.entry_1.delete('0', 'end')
        self.entry_1.insert('0', _text_)
        self.entry_1.pack(side='top')
        self.labelframe_1_2.config(
            height='200', text='Record Test', width='200')
        self.labelframe_1_2.pack(side='top')

        self.label_10 = ttk.Label(self.frame_3)
        self.time = tk.StringVar()
        self.label_10.config(
            cursor='arrow', textvariable=self.time, font='{Arial} 16 {bold}', justify='center', padding='2 10')
        self.label_10.pack(side='top')
        self.labelframe_1 = ttk.Labelframe(self.frame_3)
        self.button_5 = ttk.Button(self.labelframe_1)
        self.button_5.config(text='LOW')
        self.button_5.grid()
        self.button_6 = ttk.Button(self.labelframe_1)
        self.button_6.config(takefocus=False, text='MEDIUM')
        self.button_6.grid(column='1', row='0')
        self.button_7 = ttk.Button(self.labelframe_1)
        self.button_7.config(text='HIGH')
        self.button_7.grid(column='2', row='0')
        self.labelframe_1.config(
            height='200', padding='10', relief='flat', text='Pump Controls')
        self.labelframe_1.config(width='200')
        self.labelframe_1.pack(side='top')
        self.labelframe_3 = ttk.Labelframe(self.frame_3)
        self.button_11 = ttk.Button(
            self.labelframe_3, command=self.BendingValveSW)
        self.button_11.config(text='Bending')
        self.button_11.grid()
        self.button_12 = ttk.Button(self.labelframe_3)
        self.button_12.config(text='Straight')
        self.button_12.grid(column='1', row='0')
        self.button_13 = ttk.Button(
            self.labelframe_3, command=self.DeflateValveSW)
        self.button_13.config(text='Deflate')
        self.button_13.grid(column='2', row='0')
        self.labelframe_3.config(
            height='200', text='Valve Controls', width='200')
        self.labelframe_3.pack(side='top')
        self.frame_6 = ttk.Frame(self.frame_3)
        self.labelframe_4 = ttk.Labelframe(self.frame_6)
        self.labelframe_4.config(
            height=320*self.scaleFactor, width=280*self.scaleFactor, labelanchor='nw', takefocus=False, text='Pressue Graph')
        self.labelframe_4.grid()

        self.cv2Label = ttk.Label(self.frame_6)
        self.cv2Label.grid(column='1', row='0')

        self.frame_6.config(height='1000', padding='10', width='1000')
        self.frame_6.pack(side='top')

        self.frame_3.pack(side='top')

        # Main widget
        self.mainwindow = self.frame_3

        # Matplot Lib
        self.fig = Figure((320*self.scaleFactor/96, 280 *
                           self.scaleFactor/96), dpi=96)
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [], lw=1)
        # A tk.DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.labelframe_4)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.show_frame()
        self.ani = FuncAnimation(self.fig, self.update, self.generate_data, init_func=self.init, blit=False, interval=50,
                                 repeat=False)

    def run(self):
        self.mainwindow.mainloop()

    def startRecord(self):
        self.button_2['state'] = 'normal'
        self.button_1['state'] = 'disabled'
        self.start = True
        self.ani.event_source.start()

    def stopRecord(self):
        self.button_2['state'] = 'disabled'
        self.button_1['state'] = 'enable'
        self.start = True
        self.ani.event_source.stop()
        self.datalogger()

    def show_frame(self):
        ok, frame = self.cap.read()
        black_frame = np.zeros(
            (int(0.7*280*self.scaleFactor), int(0.7*320*self.scaleFactor)), dtype="uint8")
        if ok:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            if(self.start == True):
                self.current_image = Image.fromarray(
                    cv2image)  # convert image for PIL
            else:
                self.current_image = Image.fromarray(
                    black_frame)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            # anchor imgtk so it does not be deleted by garbage-collector
            self.cv2Label.imgtk = imgtk
            self.cv2Label.config(image=imgtk)  # show the image
        self.cv2Label.after(30, self.show_frame)

    def datalogger(self):
        print("Dumped")
        with open(f'PressureLog{datetime.datetime.now().strftime("%b-%d-%Y-%H-%M-%S")}.csv', mode='a+', newline='') as pressure_file:
            pressure_writer = csv.writer(
                pressure_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
            for x, y in zip(self.xdata, self.ydata):
                pressure_writer.writerow([x, y])

    def BendingValveSW(self):
        if ser.isOpen():
            try:
                if(self.bendingSWFlag == True):
                    ser.write('A'.encode())
                else:
                    ser.write('B'.encode())
                self.bendingSWFlag = not self.bendingSWFlag
            except Exception as e:
                print(e)

    def DeflateValveSW(self):
        if ser.isOpen():
            try:
                if(self.deflateSWFlag == True):
                    ser.write('C'.encode())
                else:
                    ser.write('D'.encode())
                self.deflateSWFlag = not self.deflateSWFlag
            except Exception as e:
                print(e)

    def generate_data(self, t=0):
        while True:
            yield float(ser.readline().decode('utf-8').split(',')[0]), float(ser.readline().decode('utf-8').split(',')[1])

    def init(self):
        self.ax.set_ylim([20, 100])
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def update(self, data):
        t, y = data
        self.time.set(
            str(f'Elapsed Time {datetime.timedelta(seconds=int(t))}'))
        self.xdata.append(t)
        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()
        if self.start == False:
            self.ani.event_source.stop()
        if t >= xmax:
            self.ax.set_xlim(xmin, 2*xmax)
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)
        return self.line,


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("port", help='COM port Where Arduino is connected')
args = parser.parse_args()
if __name__ == '__main__' and args.port:
    import tkinter as tk
    try:
        ser = serial.Serial(str(args.port), 9600)
        ser.close()
        ser.open()
        if ser.isOpen():
            ser.flushInput()
            ser.flushOutput()
        root = tk.Tk()

        app = NewprojectApp(root)
        app.run()
    except serial.serialutil.SerialException as e:
        print(e)

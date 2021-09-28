from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import preview
from tkinter.messagebox import *
import cv2, os

class Main(Tk):
	def __init__(self):
		super().__init__()
		self.title('Simple Animation App')
		self.geometry('900x600')
		self.resizable(False, False)
		self.n = 0
		self.images = []
		self.widgets()

	def widgets(self):
		self.frame = LabelFrame(self, text="buttons", width = 600, height = 55)
		self.frame.place(x = 10, y = 15)
		btn1 = Button(self.frame, text = "open", command = self.open)
		btn1.place(x = 2)
		btn2 = Button(self.frame, text = "save", command = self.save)
		btn2.place(x = 80)
		btn3 = Button(self.frame, text = "new", command = self.new)
		btn3.place(x = 158)
		btn4 = Button(self.frame, text = "prev", command = self.prev_frame)
		btn4.place(x = 236)
		btn5 = Button(self.frame, text = "next", command = self.next_frame)
		btn5.place(x = 314)
		fpsframe = LabelFrame(self.frame, text = "FPS", width = 150, height = 35)
		fpsframe.place(x = 392)
		self.FPS = IntVar()
		fps = Spinbox(fpsframe, from_ = 0,to = 2000, width = 5, textvariable = self.FPS)
		fps.pack()

		btn6 = Button(self.frame, text = "preview", 
			command = lambda:[preview.Animate.animate(self.images, self.FPS.get())])
		btn6.place(x = 442)
		btn7 = Button(self.frame, text = "export", command = self.export)
		btn7.place(x = 520)

	def open(self):
		global img
		file = askopenfilename(title = "Open image - animator app")
		self.images.append(file)
		img = ImageTk.PhotoImage(Image.open(file))
		self.view = Label(self, image = img, width = 852, height = 450)
		self.view.place(x = 20, y = 100)

	def save(self):
		file = asksaveasfilename(title = "Save Project - Simple animation app", initialfile = 'Untitled.txt', defaultextension = ".txt", filetypes = [("Text Files", "*.txt")])
		if file == '':
			file == "Untitled"
		else:
			self.title(os.path.basename(file).replace('.txt', '') + "- Simple Animation app")
			with open(file, 'w+') as f:
				data = str(self.images)
				f.write(data)
				f.close()

	def new(self):
		self.images = []
		self.title('Simple Animation app')

	def prev_frame(self):
		global img
		self.n-=1
		img = ImageTk.PhotoImage(Image.open(self.images[self.n]))
		self.view = Label(self, image = img, width = 852, height = 450)
		self.view.place(x = 20, y = 100)
	
	def next_frame(self):
		global img
		self.n += 1
		img = ImageTk.PhotoImage(Image.open(self.images[self.n]))
		self.view = Label(self, image = img, width = 852, height = 450)
		self.view.place(x = 20, y = 100)

	def createVid(self, images, fps, title):
		imgs = []
		for i in images:
			img = cv2.imread(i)
			height, width, layer = img.shape
			size = (width, height)
			imgs.append(img)
		Title = title.replace('.txt', '')
		output = cv2.VideoWriter(Title, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
		for i in range(len(imgs)):
			output.write(imgs[i])
		output.release()
	
	def export(self):
		images = self.images
		fps = self.FPS.get()
		title = 'animation' + '.avi'
		self.createVid(images, fps, title)
		showinfo("Success", "Your animation was exported succesfully exported to "+title)


if __name__=='__main__':
	Main().mainloop()
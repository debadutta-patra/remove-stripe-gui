from tkinter import *
from tkinter import filedialog
import customtkinter
from threading import Thread
import destripe
destripe.check_matplotlib_version()
##################################################
from skimage import io
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title('Removing stripe artifacts')
img = PhotoImage(file="icon.png")
root.wm_iconbitmap()
root.iconphoto(False, img)
# root.tk.call('wm', 'iconphoto', root._w, img)
root.iconphoto(False, img)

# root.iconbitmap("icon.ico")
root.geometry('1300x900')

switch_var = customtkinter.IntVar(value=1)

def switch_theme():
    if switch_var.get() == 0:
        customtkinter.set_appearance_mode('light')
    else:
        customtkinter.set_appearance_mode('dark')

def quit_gui():
    root.quit()

canvas,toolbar,canvas_fft,toolbar_fft = None, None, None, None
def plot_input(): 
    global canvas, toolbar, canvas_fft, toolbar_fft

    input_img = io.imread(ifile.get())
    input_img = np.array(input_img, dtype=np.float32)
    destripe_obj = destripe.destripe(input_img, int(eval(iter_entry.get())), float(a_entry.get()), 
                                     float(wedge_entry.get()), float(theta_entry.get()), float(kmin_entry.get()))
    # the figure that will contain the plot 
    fft_raw, mask_edge = destripe_obj.view_missing_wedge()
    plt.close()
    fig, ax_list = plt.subplots(1,1, figsize=(7,5),dpi=150)
    ax_list.imshow(destripe_obj.dataset, cmap='gray')
    ax_list.set_title('Input Image')
    ax_list.axis('off')

    # plotting the graph 
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    if canvas: 
        canvas.get_tk_widget().pack_forget()
        toolbar.forget()
    canvas = FigureCanvasTkAgg(fig, 
                               master = tab_raw)   
    canvas.draw() 
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   tab_raw) 
    toolbar.update() 
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 

    fig_fft, ax_list_fft = plt.subplots(1,1, figsize=(7,5),dpi=150)
    ax_list_fft.imshow(fft_raw, cmap = 'gray')
    ax_list_fft.set_title('FFT of Input Image')
    ax_list_fft.imshow(mask_edge, cmap='viridis_r')
    ax_list_fft.axis('off')

    if canvas_fft: 
        canvas_fft.get_tk_widget().pack_forget()
        toolbar_fft.forget()
    canvas_fft = FigureCanvasTkAgg(fig_fft, 
                               master = tab_fft)   
    canvas_fft.draw() 
    # placing the canvas on the Tkinter window 
    canvas_fft.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar_fft = NavigationToolbar2Tk(canvas_fft, 
                                   tab_fft) 
    toolbar_fft.update() 
    # placing the toolbar on the Tkinter window 
    canvas_fft.get_tk_widget().pack() 

canvas_processed, toolbar_processed, canvas_processed_fft, toolbar_processed_fft = None, None, None, None
def remove_artifact():
    global canvas_processed, toolbar_processed, canvas_processed_fft, toolbar_processed_fft
    savefile = filedialog.asksaveasfilename(filetypes=[("TIFF file", ".tiff"),("JPEG file", ".jpg"),("PNG file",".png")],
                                            defaultextension='.tiff', confirmoverwrite=False)
    input_img = io.imread(ifile.get())
    input_img = np.array(input_img, dtype=np.float32)
    destripe_obj = destripe.destripe(input_img, int(eval(iter_entry.get())), float(a_entry.get()), 
                                     float(wedge_entry.get()), float(theta_entry.get()), float(kmin_entry.get()))
    destripe_obj.TV_reconstruction()
    recon_constaraint, recon_fft = destripe_obj.recon_constraint, destripe_obj.recon_fft
    io.imsave(savefile, np.uint8(recon_constaraint))
    # the figure that will contain the plot 
    fig, ax_list = plt.subplots(1,1, figsize=(7,5),dpi=150)
    ax_list.imshow(recon_constaraint, cmap='gray')
    ax_list.set_title('Reconstructed Image')
    ax_list.axis('off')

    # plotting the graph 
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    if canvas_processed: 
        canvas_processed.get_tk_widget().pack_forget()
        toolbar_processed.forget()
    canvas_processed = FigureCanvasTkAgg(fig, 
                               master = tab_processed)   
    canvas_processed.draw() 
    # placing the canvas on the Tkinter window 
    canvas_processed.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar_processed = NavigationToolbar2Tk(canvas_processed, 
                                   tab_processed) 
    toolbar_processed.update() 
    # placing the toolbar on the Tkinter window 
    canvas_processed.get_tk_widget().pack() 

    fig_fft, ax_list_fft = plt.subplots(1,1, figsize=(7,5),dpi=150)
    ax_list_fft.imshow(recon_fft, cmap = 'gray')
    ax_list_fft.set_title('FFT of Reconstructed Image')

    if canvas_processed_fft: 
        canvas_processed_fft.get_tk_widget().pack_forget()
        toolbar_processed_fft.forget()
    canvas_processed_fft = FigureCanvasTkAgg(fig_fft, 
                               master = tab_processed_fft)   
    canvas_processed_fft.draw() 
    # placing the canvas on the Tkinter window 
    canvas_processed_fft.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar_processed_fft = NavigationToolbar2Tk(canvas_processed_fft, 
                                   tab_processed_fft) 
    toolbar_processed_fft.update() 
    # placing the toolbar on the Tkinter window 
    canvas_processed_fft.get_tk_widget().pack() 

    tabview_input.set("Processed Image")



frame_io = customtkinter.CTkFrame(master=root)
frame_io.grid(row=0,column=0,pady=10,padx=10)  # add tab at the end

ifile = StringVar()
ifile.set("")
def get_input():
    ifile.set(filedialog.askopenfilename())

read_button = customtkinter.CTkButton(master = frame_io, command = get_input, corner_radius=50, font=("Helvetica", 14), text = "Open file") 
read_button.grid(row=0,column=0,pady=10,columnspan=2)

def set_wedge(value):
    wedge_entry.delete(0,END)
    wedge_entry.insert(0,value)
wedge_slider = customtkinter.CTkSlider(frame_io, command=set_wedge, from_=0, to=180, number_of_steps=360, width = 300)
wedge_slider.set(5)
wedge_slider.grid(row=2,column=0,pady=5,padx=10,columnspan=2,stick="ew")
wedge_entry = customtkinter.CTkEntry(frame_io,placeholder_text='Wedge Size', font=("Helvetica", 14))
wedge_entry.grid(row=1,column=0,pady=10,padx=10)

def set_theta(value):
    theta_entry.delete(0,END)
    theta_entry.insert(0,value)
theta_slider = customtkinter.CTkSlider(frame_io, command=set_theta, from_=-90, to=90, number_of_steps=360, width = 300)
theta_slider.set(0)
theta_slider.grid(row=4,column=0,pady=5,padx=10,columnspan=2,stick="ew")
theta_entry = customtkinter.CTkEntry(frame_io,placeholder_text='Theta', font=("Helvetica", 14))
theta_entry.grid(row=3,column=0,pady=10,padx=10)

def set_kmin(value):
    kmin_entry.delete(0,END)
    kmin_entry.insert(0,value)
kmin_slider = customtkinter.CTkSlider(frame_io, command=set_kmin, from_=0, to=50, number_of_steps=50,width = 300)
kmin_slider.set(15)
kmin_slider.grid(row=6,column=0,pady=5,padx=10,columnspan=2,stick="ew")
kmin_entry = customtkinter.CTkEntry(frame_io,placeholder_text='K_min Value', font=("Helvetica", 14))
kmin_entry.grid(row=5,column=0,pady=10,padx=10)

def set_a(value):
    a_entry.delete(0,END)
    a_entry.insert(0,value)
a_slider = customtkinter.CTkSlider(frame_io, command=set_a, from_=0, to=0.3, number_of_steps=100, width = 300)
a_slider.set(0.2)
a_slider.grid(row=8,column=0,pady=5,padx=10,columnspan=2,stick="ew")
a_entry = customtkinter.CTkEntry(frame_io,placeholder_text='a value', font=("Helvetica", 14))
a_entry.grid(row=7,column=0,pady=10,padx=10)

def set_iter(value):
    iter_entry.delete(0,END)
    iter_entry.insert(0,value)
iter_slider = customtkinter.CTkSlider(frame_io, command=set_iter, from_=1, to=500, number_of_steps=499, width = 300)
iter_slider.set(10)
iter_slider.grid(row=10,column=0,pady=5,padx=10,columnspan=2,stick="ew")
iter_entry = customtkinter.CTkEntry(frame_io,placeholder_text='Iterations',font=("Helvetica", 14))
iter_entry.grid(row=9,column=0,pady=10,padx=10)

plot_button = customtkinter.CTkButton(master = frame_io, command = plot_input, corner_radius=50, font=("Helvetica", 14), text = "Show_input") 
plot_button.grid(row=11,column=0,pady=(10, 10),padx=20, sticky="w")

process_button = customtkinter.CTkButton(master = frame_io, command = remove_artifact, corner_radius=50, font=("Helvetica", 14), text = "Remove Artifacts") 
process_button.grid(row=11,column=1,pady=(10, 10), padx=20,sticky="ew")

tabview_input = customtkinter.CTkTabview(master=root,height=700,width=700, corner_radius=20)
tabview_input._segmented_button.configure(font=("Helvetica", 14))
tabview_input.grid(row=0,column=1,pady=10,padx=5,rowspan=2)  # add tab at the end

tab_raw = tabview_input.add("Input Image")
tab_fft = tabview_input.add("Input FFT")
tab_processed = tabview_input.add("Processed Image")
tab_processed_fft = tabview_input.add("Processed Image FFT")

frame_settings = customtkinter.CTkFrame(master=root)
frame_settings.grid(row=1,column=0,pady=10, padx=10, sticky="ew")  # add tab at the end

themes_switch = customtkinter.CTkSwitch(frame_settings, text='Dark mode', onvalue=1,offvalue=0, variable=switch_var, command=switch_theme, switch_height=20,
                                        switch_width=40, font=("Helvetica", 14))
themes_switch.grid(row=0,column=0,pady=10)

quit_button  = customtkinter.CTkButton(frame_settings, text='Quit', command=quit_gui, corner_radius=50, fg_color=('#E34234','#DC143C'), font=("Helvetica", 14))
quit_button.grid(row=1,column=0,pady=10)

citation_label = customtkinter.CTkTextbox(root,width=1280,height=125,font=("Helvetica", 20))
citation_label.insert("0.2", 'Please cite:\n"Removing Stripes, Scratches, and Curtaining with Nonrecoverable Compressed Sensing", Microscopy and Microanalysis (2019),\n\
DOI: 10.1017/S1431927619000254')
citation_label.insert("0.1", f'App made by Debadutta Patra\n')

citation_label.configure(state='disabled')
citation_label.grid(row=3,column=0, padx=10, pady = 10,columnspan=2,sticky="ew")

root.mainloop()
from tkinter import *
import os
import subprocess
import shutil #to copy files
from tkinter.filedialog import *
from PIL import ImageTk, Image
shutil.rmtree('temp', ignore_errors = True) #remove temp folder


def metadata_window():
    top=Toplevel()
    top.grab_set()
    top.title('Metadata Creator')
    top.iconbitmap('resources/icon.ico')
    top.geometry('600x450')
    top.resizable(False, False)
    
    #set colour here
    #top.configure(bg='blue')
    #   '#F0F0F0' is the default bg colour of tkinter
    top['bg'] = '#F0F0F0'
    label_font_colour='black'
    label_bg_colour='#F0F0F0'
    radio_font_colour='black'
    radio_bg_colour= '#F0F0F0'
    
    
    
    
    def cal_scale():
        height=game_height.get()
        if (height=='128') or (height=='65'):
            scale_value='400'
        elif (height=='160'):
            scale_value='300'

        elif (height=='208') or (height=='220'):
            scale_value='200'
        else:
            scale_value='100'
        zoom_level.delete(0, END)
        zoom_level.insert(0,scale_value)
    def save_to_file():
    
        fileout=open('temp/game/meta.txt','w')
        fileout.write('Title: '+EntryBox[0].get()+'\n'
        +'Series: '+EntryBox[1].get()+'\n'
        +'Developer: '+EntryBox[2].get()+'\n'
        +'Publisher: '+EntryBox[3].get()+'\n'
        +'Play Mode: '+play_mode.get()+'\n'
        +'Status: '+status.get()+'\n'
        +'Extreme: '+extreme.get()+'\n'
        +'Genre: '+EntryBox[7].get()+'\n'
        +'Source: '+EntryBox[8].get()+'\n'
        +'Platform: J2ME\n'
        +'Application Path: '+emulator.get()+'\n'
        +'Launch command: '+game_name_entry.get()+'.jar '
                      +game_width.get()+' '
                      +game_height.get()+' '
                      +zoom_level.get()+' '
                      +fps.get()+' '
                      +'\n'
        +'Notes: '+EntryBox[11].get()+'\n'
        +'Author Notes: '+EntryBox[12].get()+'\n'
        )
        
        fileout.close()
       
        des='temp/game/content/'+game_name_entry.get()+'.jar'
        #exection handling
        try:
            
            if not os.path.exists('temp/game/content'):
                os.makedirs('temp/game/content')
            shutil.copy(game_file_src, des)
        except FileNotFoundError:
            print('Error file or directory was not found')
        else:
            print('No Error')
    
        if not os.path.exists('temp/game'+game_name_entry.get()):
            os.replace('temp/game','temp/'+game_name_entry.get() )
        shutil.make_archive('output/'+game_name_entry.get(),'zip','temp')
        root.destroy() #exit the window
        os.system('cmd /k "start output"') #opens output folder
        
    #--------------------------test game routine----------------------------------------
    dir_file=open('resources/kahvi_config.txt','r')
    soft_dir=dir_file.readlines()
    
    try:
        global freej2me_dir, freej2me_new_dir,kemulator_1_0_3_dir, kemulator_9_8_dir,kemulator_9_8_dir,Jre_1_4_dir,jre_1_8_dir
        freej2me_dir=soft_dir[0].strip()
        freej2me_new_dir=soft_dir[1].strip()
        kemulator_1_0_3_dir=soft_dir[2].strip()
        kemulator_9_8_dir=soft_dir[3].strip()
        jre_1_4_dir=soft_dir[4].strip()
        jre_1_8_dir=soft_dir[5].strip()
       
    except IndexError:
        print("Pls select kahvibreak directory")
   
    dir_file.close()

    def select_kahvi_dir():
        try:
            kahvi_dir =  askdirectory()
        except AttributeError:
                 print("No directory selected")
        else:
            kahvi_config=open('resources/kahvi_config.txt','w')
            kahvi_config.write(kahvi_dir+"/Software/FreeJ2ME/freej2me-kahvi-0.4.1.jar"+"\n"
                           +kahvi_dir+"/Software/FreeJ2ME/freej2me-kahvi-0.4.2.jar"+"\n"
                            +kahvi_dir+"/Software/KEmulator/KEmulator-1.0.3.jar"+"\n"
                            +kahvi_dir+"/Software/KEmulator/KEmulator-0.9.8.jar"+"\n"
                            +kahvi_dir+"/Software/jre-1.4/bin/javaz.exe"+"\n"
                            +kahvi_dir+"/Software/jre-8/bin/javaz.exe")
            kahvi_config.close()
    def test_game_btn():
        emulator_var=emulator.get()
        batch_script=''
        if emulator_var=='Software\FreeLaunch.bat':
            batch_script='start "" "' + jre_1_8_dir+'" -jar "'+freej2me_dir+'" "file:///'+game_file_src+'" '+game_width.get()+" "+game_height.get()+" "+zoom_level.get()+" "+fps.get()

        elif emulator_var=='Software\FreeLaunch0.4.2.bat':
            batch_script='start "" "' + jre_1_8_dir+'" -jar "'+freej2me_new_dir+'" "file:///'+game_file_src+'" '+game_width.get()+" "+game_height.get()+" "+zoom_level.get()+" "+fps.get()

        elif emulator_var=='Software\KLaunch.bat':
            batch_script='start "" "' + jre_1_8_dir+'" -jar "'+kemulator_1_0_3_dir+'" -jar "'+game_file_src

        #emulator='Software\KLaunch98.bat'
        else:
            batch_script='start "" "' + jre_1_4_dir+'" -jar "'+kemulator_9_8_dir+'" -jar "'+game_file_src

        bat_file=open('resources/run_game.bat','w')
        bat_file.write(batch_script)
        bat_file.close()
        #run_game_script='"'+os.path.abspath('resources/run_game.bat')+'"'
        run_game_script=os.path.abspath('resources/run_game.bat')
        subprocess.call(run_game_script)

    #-----------------------------------------------------------------

    LabelList=[0]*13
    LabelListText=['Title','Series','Developer','Publisher','Play Mode','Status','Extreme','Genre','Source','Emulator to use','Launch settings','Notes','Author notes']
    EntryBox=[0]*13

    for i in range(0,13):
        LabelList[i]=Label(top,text=LabelListText[i],fg=label_font_colour,bg=label_bg_colour,font=('Verdana',12))
        LabelList[i].grid(row=i,column=0)
        EntryBox[i]=Entry(top,font=('Verdana', 12), width=40)
        EntryBox[i].grid(row=i, column=1)

   
    #radio buttons
    #Play Mode
    EntryBox[4].grid_forget()
    frame1=Frame(top)
    frame1.grid(row=4,column=1)

    play_mode=StringVar()
    play_mode.set('Single Player') #default value
    single_player=Radiobutton(frame1,text='Single Player',fg=radio_font_colour,bg=radio_bg_colour,var=play_mode,value='Single Player')
    single_player.pack(side=LEFT)
    multi_player=Radiobutton(frame1,text='Multi Player',fg=radio_font_colour,bg=radio_bg_colour,var=play_mode,value='Multi Player')
    multi_player.pack()

    #status mode
    EntryBox[5].grid_forget()
    frame2=Frame(top)
    frame2.grid(row=5,column=1)

    status=StringVar()
    status.set('Playable') #default value
    status_playable=Radiobutton(frame2,text='Playable',fg=radio_font_colour,bg=radio_bg_colour,var=status,value='Playable')
    status_playable.pack(side=LEFT)
    status_unplayable=Radiobutton(frame2,text='Unplayable',fg=radio_font_colour,bg=radio_bg_colour,var=status,value='Unplayable')
    status_unplayable.pack()

    #Extreme Mode
    EntryBox[6].grid_forget()
    frame3=Frame(top)
    frame3.grid(row=6,column=1)

    extreme=StringVar()
    extreme.set('No') #default value
    no=Radiobutton(frame3,text='No', fg=radio_font_colour,bg=radio_bg_colour, var=extreme,value='No')
    no.pack(side=LEFT)
    yes=Radiobutton(frame3,text='Yes', fg=radio_font_colour,bg=radio_bg_colour,var=extreme,value='Yes')
    yes.pack()
    '''
    #genre
    EntryBox[7].grid_forget()
    frame4=Frame(top)
    frame4.grid(row=7,column=1)
    '''

    #Application Path/emulator to use
    EntryBox[9].grid_forget()
    frame5=Frame(top)
    frame5.grid(row=9,column=1)

    emulator=StringVar()
    emulator.set('Software\FreeLaunch.bat') #default value
    freej2me=Radiobutton(frame5,text='FreeJ2me', fg=radio_font_colour,bg=radio_bg_colour,var=emulator,value='Software\FreeLaunch.bat')
    freej2me.pack(side=LEFT)
    freej2me_new=Radiobutton(frame5,text='FreeJ2me(new)', fg=radio_font_colour,bg=radio_bg_colour,var=emulator,value='Software\FreeLaunch0.4.2.bat')
    freej2me_new.pack(side=LEFT)
    kemulator_new=Radiobutton(frame5,text='Kemulator v1.0.3', fg=radio_font_colour,bg=radio_bg_colour,var=emulator,value='Software\KLaunch.bat')
    kemulator_new.pack(side=LEFT)
    kemulator_old=Radiobutton(frame5,text='Kemulator v9.8', fg=radio_font_colour,bg=radio_bg_colour,var=emulator,value='Software\KLaunch98.bat')
    kemulator_old.pack(side=LEFT)
    

    #Launch command
    EntryBox[10].grid_forget()
    frame6=Frame(top)
    frame6.grid(row=10,column=1)
    
    

    sel_kahvi_dir_btn=Button(frame6,text='Select Kahvi Directory',command=select_kahvi_dir)
    sel_kahvi_dir_btn.grid(row=0,column=2,padx=10)
    test_game_btn=Button(frame6,text=    'Test Game',command=test_game_btn)
    test_game_btn.grid(row=1,column=2,padx=10)
    cal_scale_btn=Button(frame6,text=    'Calculate Scale',command=cal_scale)
    cal_scale_btn.grid(row=2,column=2,padx=10)
    
    game_width_label=Label(frame6, text='Width')
    game_width_label.grid(row=0,column=0)
    
    game_height_label=Label(frame6, text='Height')
    game_height_label.grid(row=1,column=0)
    
    scale_level_label=Label(frame6, text='Scale/Zoom')
    scale_level_label.grid(row=2,column=0)
    
    fps_label=Label(frame6, text='FPS')
    fps_label.grid(row=3,column=0)
    
    
    game_width=Entry(frame6, width=5)
    game_width.grid(row=0,column=1)
    
    game_height=Entry(frame6, width=5)
    game_height.grid(row=1,column=1)
    
    zoom_level=Entry(frame6, width=5)
    zoom_level.grid(row=2,column=1)
    
    fps=Entry(frame6, width=5)
    fps.grid(row=3,column=1)
    
    save_btn=Button(top,font=('Verdana', 15),text="SAVE",command=save_to_file)
    #save_btn=Button(top,font=('Verdana', 15),bg='green',fg='white',text="SAVE",command=save_to_file)
    save_btn.grid(row=14,column=1)
    
    top.mainloop()

#=================================================================Main Window======================================================================#     
ss_flag=FALSE
logo_flag=FALSE
game_flag=FALSE

def check_button():
    if not (ss_flag and logo_flag and game_flag) == FALSE:
    
        next.config(state=NORMAL)
        print("Next button enabled Enjoy ;)")
    else:
        print("Next button is disabled :( ")



def open_image(a):
    global ss_image_src, logo_image_src, ss_image, logo_image, ss_flag, logo_flag #set to global otherwise images wont show up due to pythons garbage collector
    
    if a==1:
        logo_image_src=askopenfilename(initialdir='', filetypes=[('Image files','.png')])
        des='temp/game/logo.png'
        try:
            logo_image=ImageTk.PhotoImage(Image.open(logo_image_src))
            logo_view=Label(image_frame1,image=logo_image)
            logo_view.grid(row=0,column=0)
            copy_image_files(logo_image_src,des)
        except AttributeError:
            print('No logo image selected')
        else:
            print('No error selecting logo image')
            logo_flag=TRUE
        check_button()
        
    elif a==2:
        ss_image_src=askopenfilename(initialdir='', filetypes=[('Image files','.png')])
        des='temp/game/ss.png'
        try:
            ss_image=ImageTk.PhotoImage(Image.open(ss_image_src))
            screenshot_view=Label(image_frame2,image=ss_image)
            screenshot_view.grid(row=0,column=0)
            copy_image_files(ss_image_src,des)
        except AttributeError:
            print('No screenshot image selected')
        else:
            print('No error selecting screenshot image')
            ss_flag=TRUE
        check_button()


def open_game():
    
    global game_file_src, game_flag
 
    game_file_src=askopenfilename(initialdir='', filetypes=[('J2ME files','.jar')])
    name=os.path.basename(game_file_src)
    new_name=name[:len(name)-4]
    underscored_name=new_name.replace(" ", "_")
    game_name_entry.delete(0,END)
    game_name_entry.insert(0,underscored_name)
        
    if game_file_src=='':
        print('No game selected')
    else:
        print('No error selecting game')
        game_flag=TRUE
    check_button()
        
def copy_image_files(source,destination):
    #exection handling
    try:

        if not os.path.exists('temp/game'):
            os.makedirs('temp/game')
        shutil.copy(source, destination)
    except FileNotFoundError:
        print('Error file was not found')
    else:
        print('No Error during image copy')
   

    
root=Tk()
root.title('Kahvibreak Curation Tool v1.1')
root.iconbitmap('resources/icon.ico')
root.geometry('500x500')
root.resizable(False, False)

#color
#window_one_bg='black'
#window_one_fg='white'

image_frame_master=Frame()
image_frame_master.pack(side=TOP)
image_frame_master.configure(bg='green')

default_logo='resources/logo.png'
image_frame1=LabelFrame(image_frame_master, text='Logo',width=100,height=100)
image_frame1.pack(side=LEFT)
default_ss='resources/ss.png'
image_frame2=LabelFrame(image_frame_master, text='Screen Shot',width=100,height=100)
image_frame2.pack(side=LEFT)


logo_image=ImageTk.PhotoImage(Image.open(default_logo))
logo_view_default=Label(image_frame1,image=logo_image)
logo_view_default.grid(row=0,column=0)

ss_image=ImageTk.PhotoImage(Image.open(default_ss))
screenshot_view_default=Label(image_frame2,image=ss_image)
screenshot_view_default.grid(row=0,column=0)


buttons_frame=LabelFrame(root,text='Must Select All',padx=10,pady=10)
buttons_frame.pack(side=BOTTOM)


#open_logo=Button(buttons_frame,bg=window_one_bg,fg=window_one_fg,font=('Verdana', 10),text="Select Logo", command = lambda: open_image(1))
open_logo=Button(buttons_frame,font=('Verdana', 10),text="Select Logo", command = lambda: open_image(1))
open_logo.pack(fill=X)

open_ss=Button(buttons_frame,font=('Verdana', 10),text="Select Screenshot", command = lambda: open_image(2))
open_ss.pack(fill=X)



open_game=Button(buttons_frame,font=('Verdana', 10),text="Select Game", command = open_game)
open_game.pack(fill=X)


game_name_entry=Entry(buttons_frame,font=('Verdana', 10), width=30)
game_name_entry.pack()

next=Button(buttons_frame,font=('Verdana', 10),text="NEXT",state=DISABLED,command = metadata_window)
#next=Button(buttons_frame,font=('Verdana', 10),text="NEXT",bg='black',fg='white',state=DISABLED,command = metadata_window)
#next=Button(buttons_frame,font=('Verdana', 10),text="NEXT",bg='black',fg='white',command = metadata_window)

next.pack()    


root.mainloop()

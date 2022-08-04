import cv2
from numpy.lib.function_base import append
import pygame
import numpy as np
import sys
from pygame.locals import *
# import pygame_menu
import serial
import serial.tools.list_ports
from struct import pack
import pygame_gui
import pygame.camera
import time
import ctypes

cv = 0

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
pygame.font.init()

myfont = pygame.font.SysFont('Tahoma', 50)

start = time.time()

ser = serial.Serial()

def getSerial():
    serials=[]
    for info in serial.tools.list_ports.comports():
        # print(info)
        # print(info.pid)
        if info.pid != None:
            try:
                seri = serial.Serial(info.device, 9600)
                serials.append(info.device)
                seri.close()
            except:
                next
    serials.append("refresh")
    return serials

# videoIn = 0
# resolution = (1280,960)

py_map={
    pygame.K_LCTRL:"KEY_LEFT_CTRL",
    pygame.K_LSHIFT:"KEY_LEFT_SHIFT",
    pygame.K_LALT:"KEY_LEFT_ALT",
    pygame.K_LSUPER:"KEY_LEFT_GUI",
    pygame.K_RCTRL:"KEY_RIGHT_CTRL",
    pygame.K_RSHIFT:"KEY_RIGHT_SHIFT",
    pygame.K_RALT:"KEY_RIGHT_ALT",
    pygame.K_RSUPER:"KEY_RIGHT_GUI",
    pygame.K_UP:"KEY_UP_ARROW",
    pygame.K_DOWN:"KEY_DOWN_ARROW",
    pygame.K_LEFT:"KEY_LEFT_ARROW",
    pygame.K_RIGHT:"KEY_RIGHT_ARROW",
    pygame.K_BACKSPACE:"KEY_BACKSPACE",
    pygame.K_TAB:"KEY_TAB",
    pygame.K_RETURN:"KEY_RETURN",
    pygame.K_ESCAPE:"KEY_ESC",
    pygame.K_INSERT:"KEY_INSERT",
    pygame.K_DELETE:"KEY_DELETE",
    pygame.K_PAGEUP:"KEY_PAGE_UP",
    pygame.K_PAGEDOWN:"KEY_PAGE_DOWN",
    pygame.K_HOME:"KEY_HOME",
    pygame.K_END:"KEY_END",
    pygame.K_CAPSLOCK:"KEY_CAPS_LOCK",
    pygame.K_F1:"KEY_F1",
    pygame.K_F2:"KEY_F2",
    pygame.K_F3:"KEY_F3",
    pygame.K_F4:"KEY_F4",
    pygame.K_F5:"KEY_F5",
    pygame.K_F6:"KEY_F6",
    pygame.K_F7:"KEY_F7",
    pygame.K_F8:"KEY_F8",
    pygame.K_F9:"KEY_F9",
    pygame.K_F10:"KEY_F10",
    pygame.K_F11:"KEY_F11",
    pygame.K_F12:"KEY_F12" }
orig_map = {"KEY_LEFT_CTRL":128,
            "KEY_LEFT_SHIFT":129,
            "KEY_LEFT_ALT":130,
            "KEY_LEFT_GUI":131,
            "KEY_RIGHT_CTRL":132,
            "KEY_RIGHT_SHIFT":133,
            "KEY_RIGHT_ALT":134,
            "KEY_RIGHT_GUI":135,
            "KEY_UP_ARROW":218,
            "KEY_DOWN_ARROW":217,
            "KEY_LEFT_ARROW":216,
            "KEY_RIGHT_ARROW":215,
            "KEY_BACKSPACE":178,
            "KEY_TAB":179,
            "KEY_RETURN":176,
            "KEY_ESC":177,
            "KEY_INSERT":209,
            "KEY_DELETE":212,
            "KEY_PAGE_UP":211,
            "KEY_PAGE_DOWN":214,
            "KEY_HOME":210,
            "KEY_END":213,
            "KEY_CAPS_LOCK":193,
            "KEY_F1":194,
            "KEY_F2":195,
            "KEY_F3":196,
            "KEY_F4":197,
            "KEY_F5":198,
            "KEY_F6":199,
            "KEY_F7":200,
            "KEY_F8":201,
            "KEY_F9":202,
            "KEY_F10":203,
            "KEY_F11":204,
            "KEY_F12":205}

def draw_background(cap, surface,scr_size):
    #### CV2 - deprecated
    if cv:
        success, frame = cap.read()
        if not success:
            exit

        #for some reasons the frames appeared inverted
        try:
            frame = np.fliplr(frame)
            frame = np.rot90(frame)

            # The video uses BGR colors and PyGame needs RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            surf = pygame.surfarray.make_surface(frame)
            surf=pygame.transform.scale(surf,scr_size)
            surface.blit(surf, (0,0))
        except Exception as e:
            print(e)
            surface.fill([0,0,0])
    else:
        try:
            img = cap.get_image()
            img = pygame.transform.scale(img, scr_size)
            surface.blit(img, (0,0))
        except Exception as e: 
            # print(e)
            surface.fill([0,0,0])
    


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 9
    # index = 0
    arr = []
    i = 10
    while i > 0:
        lap = cv2.VideoCapture(index,cv2.CAP_DSHOW)
        if lap.read()[0]:
            yield(index)
            # arr.append(index)
            lap.release()
        index -= 1
        # index += 1
        i -= 1
    # return arr

def genrateUI(manager,scr_size,serials,activeSerial,resolution,activeVideoIn, showSettings,camlist,keyLayouts, activeKeyLayout):
    resolutions = ['640x480','800x600','1024x768','1280x960','1920x1080']
    # activeSerial = serials[0]
    res = scale_screen(scr_size)
    activeResolution=str(res[0])+'x'+str(res[1])
    elment_x=150
    elment_y=35
    i=0
    settings_button = pygame_gui.elements.UIButton(pygame.Rect(scr_size[0]-elment_x-30, i*elment_y, elment_x, elment_y),
                                            text='Settings',
                                            manager=manager)
    i+=1
    resolution_text = pygame_gui.elements.ui_text_box.UITextBox("Resolution:",
                                            relative_rect=pygame.Rect(scr_size[0]-elment_x-15, i*elment_y, elment_x, elment_y),
                                            manager=manager)
    i+=1
    resolution_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=resolutions,
                                                        starting_option=activeResolution,
                                                        relative_rect=pygame.Rect(scr_size[0]-elment_x, i*elment_y, elment_x, elment_y),
                                                        manager=manager)            
    i+=1
    videoIn_text = pygame_gui.elements.ui_text_box.UITextBox("VideoIn:",
                                            relative_rect=pygame.Rect(scr_size[0]-elment_x-15, i*elment_y, elment_x, elment_y),
                                            manager=manager)
    i+=1
    videoIn_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=camlist,
                                                    starting_option=activeVideoIn,
                                                    relative_rect=pygame.Rect(scr_size[0]-elment_x, i*elment_y, elment_x, elment_y),
                                                    manager=manager)   
    i+=1
    serial_text = pygame_gui.elements.ui_text_box.UITextBox("SerialPort:",
                                            relative_rect=pygame.Rect(scr_size[0]-elment_x-15, i*elment_y, elment_x, elment_y),
                                            manager=manager)
    i+=1
    serial_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=serials,
                                                    starting_option=activeSerial,
                                                    relative_rect=pygame.Rect(scr_size[0]-elment_x, i*elment_y, elment_x, elment_y),
                                                    manager=manager)   
    i+=1
    keylayout_text = pygame_gui.elements.ui_text_box.UITextBox("KeyLayout:",
                                            relative_rect=pygame.Rect(scr_size[0]-elment_x-15, i*elment_y, elment_x, elment_y),
                                            manager=manager)
    i+=1
    keylayout_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=keyLayouts,
                                                    starting_option=activeKeyLayout,
                                                    relative_rect=pygame.Rect(scr_size[0]-elment_x, i*elment_y, elment_x, elment_y),
                                                    manager=manager)   
    i+=1
    if not showSettings:
        resolution_dropdown.hide()
        resolution_text.hide()
        videoIn_dropdown.hide()
        videoIn_text.hide()
        serial_dropdown.hide()
        serial_text.hide()
        keylayout_dropdown.hide()
        keylayout_text.hide()
    else:
        resolution_dropdown.show()
        resolution_text.show()
        videoIn_dropdown.show()
        videoIn_text.show()
        serial_dropdown.show()
        serial_text.show()
        keylayout_dropdown.show()
        keylayout_text.show()
    return settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text

def scale_screen(size):
    return tuple(int(scaleFactor*x) for x in size)


def main( camlist):
    # resolutions = ['1280x960','1920x1080','640x480','800x600','1024x768']
    try:
        videoIn=camlist[-2]
    except:
        videoIn="not availible"
    ser_connected = False
    serials=getSerial()
    if len(serials) > 1:
        ser = serial.Serial(serials[0], 9600)
    else:
        ser = serial.Serial()
    activeSerial = serials[0]
    keyLayouts=["us","de","es","fr","it"]
    activeKeyLayout = "us"
    # serials.append('refresh')
    pygame.init()
    scr_size = (round(pygame.display.Info().current_w*0.8),round(pygame.display.Info().current_h*0.8))
    # scr_size = (1280,960)
    resolution=str(scr_size[0])+'x'+str(scr_size[1])
    pygame.display.set_caption("mobileKVM")
    # pygame.display.set_icon(0)
    surface = pygame.display.set_mode(scr_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    manager = pygame_gui.UIManager(scr_size)

    surface.fill([0,0,0])
    ##### CV2 - deprecated
    if cv:
        vin = 0
        cap = cv2.VideoCapture()
        print(camlist)
        try:
            cap.open(vin, cv2.CAP_DSHOW)
        except Exception as e: print(e)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, scr_size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, scr_size[1])
    else:
        try:
            if scale_screen(scr_size) > (1920,1080):
                camsize=(1920,1080)
            else:
                camsize = scale_screen(scr_size)
            # cap = pygame.camera.Camera(videoIn,scale_screen(scr_size))
            print(camsize)
            cap = pygame.camera.Camera(videoIn,camsize)
            cap.start()
        except Exception as e: print(e)


    showSettings = False
    settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)
    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(60)/1000.0
        surface.fill([0,0,0])
        try:
            draw_background(cap, surface,scr_size)
        except Exception as e: 
            print(e)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type==VIDEORESIZE:
                scr_size=tuple(event.dict['size'])
                surface=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                manager.set_window_resolution(event.dict['size'])
                manager.clear_and_reset()
                settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text,keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)
                
                ##### CV2 - deprecated
                if cv:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, event.dict['size'][0])
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, event.dict['size'][1])
                else:
                    if scale_screen(scr_size) > (1920,1080):
                        camsize=(1920,1080)
                    else:
                        camsize = scale_screen(scr_size)
                    cap = pygame.camera.Camera(videoIn,camsize) 
                    cap.start()
                pygame.display.flip()
                # print(cap.get_size())
            elif event.type in (pygame.KEYUP ,pygame.KEYDOWN):
                    if event.type == pygame.KEYUP:
                        press=False
                    else:
                        press=True

                    if event.key in py_map:
                        key=orig_map[py_map[event.key]]
                        print("{} mapped to {} ({})".format(event.key,
                            py_map[event.key],key))
                    else:
                        key=event.key
                    layoutNum=keyLayouts.index(activeKeyLayout)+2
                    if ser.is_open and key < 256:
                        ser.write(pack("!BB",1 if press else 0,key))
                    #print(ser.readlines())
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == settings_button:
                        showSettings = not showSettings
                        if not showSettings:
                            resolution_dropdown.hide()
                            resolution_text.hide()
                            videoIn_dropdown.hide()
                            videoIn_text.hide()
                            serial_dropdown.hide()
                            serial_text.hide()
                            keylayout_dropdown.hide()
                            keylayout_text.hide()
                        else:
                            resolution_dropdown.show()
                            resolution_text.show()
                            videoIn_dropdown.show()
                            videoIn_text.show()
                            serial_dropdown.show()
                            serial_text.show()
                            keylayout_dropdown.show()
                            keylayout_text.show()
                        # print(event.ui_element)
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    # print(event.ui_element)
                    if event.ui_element == resolution_dropdown:
                        res=event.text.split('x')
                        res = list(map(int, res))
                        if res[0] != scr_size[0] and res[1] != scr_size[1]:
                            scr_size=tuple(res)
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size=res))
                    if event.ui_element == videoIn_dropdown:
                        if event.text =='refresh':
                            pygame.camera.init()
                            camlist = pygame.camera.list_cameras()
                            # print(camlist)
                            # videoIns=list(range(0,len(camlist)))
                            camlist.append('refresh')
                            manager.clear_and_reset()
                            settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)
                        else:
                            videoIn=event.text
                            cID = [i for i,x in enumerate(camlist) if x == event.text][0]
                            vin = cID
                            #### CV2 - deprecated
                            if cv:
                                print(cID)
                                sap = cv2.VideoCapture(cID,cv2.CAP_DSHOW)
                                if sap.read()[0]:
                                    sap.release()
                                cap.open(cID, cv2.CAP_DSHOW)
                                cap.set(cv2.CAP_PROP_FRAME_WIDTH, scr_size[0])
                                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, scr_size[1])
                            else:
                                if scale_screen(scr_size) > (1920,1080):
                                    camsize=(1920,1080)
                                else:
                                    camsize = scale_screen(scr_size)
                                cap = pygame.camera.Camera(event.text,scale_screen(scr_size)) 
                                cap.start()
                    if event.ui_element == serial_dropdown:
                        try:
                            ser.close()
                        except:
                            continue
                        if event.text =='refresh':
                            serials=getSerial()
                            try:
                                ser = serial.Serial(serials[0], 9600)
                            except:
                                continue
                            # serials.append('refresh')
                            manager.clear_and_reset()
                            settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)
                        else:
                            try:
                                ser = serial.Serial(event.text, 9600)
                            except:
                                serials=getSerial()
                                # serials.append('refresh')
                                manager.clear_and_reset()
                                settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)
                    if event.ui_element == keylayout_dropdown:
                        layoutNum=keyLayouts.index(activeKeyLayout)+2
                        if ser.is_open:
                            ser.write(pack("!BB",0,layoutNum))
                            activeKeyLayout = event.text
                        manager.clear_and_reset()
                        settings_button, resolution_dropdown, resolution_text, videoIn_dropdown, videoIn_text, serial_dropdown, serial_text, keylayout_dropdown, keylayout_text = genrateUI(manager,scr_size,serials,activeSerial,resolution,videoIn,showSettings,camlist,keyLayouts,activeKeyLayout)


                    

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(surface)
        pygame.display.flip()


pygame.camera.init()
camlist = pygame.camera.list_cameras()

camlist.append('refresh')
if __name__ == "__main__":
    main(camlist)


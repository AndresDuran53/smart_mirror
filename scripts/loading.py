import tkinter as tk
import time

def getArcs():
    extenal_coord = circle_x0+(circle_width), circle_y0+(circle_width), circle_x1-(circle_width), circle_y1-(circle_width)
    internal_coord = circle_x0+(circle_width*2), circle_y0+(circle_width*2), circle_x1-(circle_width*2), circle_y1-(circle_width*2)

    external_arc1 = canvas.create_arc(extenal_coord, start=0, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc1 = canvas.create_arc(internal_coord, start=0, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc2 = canvas.create_arc(extenal_coord, start=-45, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc2 = canvas.create_arc(internal_coord, start=-45, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc3 = canvas.create_arc(extenal_coord, start=-90, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc3 = canvas.create_arc(internal_coord, start=-90, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc4 = canvas.create_arc(extenal_coord, start=-135, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc4 = canvas.create_arc(internal_coord, start=-135, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc5 = canvas.create_arc(extenal_coord, start=-180, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc5 = canvas.create_arc(internal_coord, start=-180, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc6 = canvas.create_arc(extenal_coord, start=-225, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc6 = canvas.create_arc(internal_coord, start=-225, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc7 = canvas.create_arc(extenal_coord, start=-270, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc7 = canvas.create_arc(internal_coord, start=-270, extent=45, fill="#005090",width=circle_width,outline="#005070")

    external_arc8 = canvas.create_arc(extenal_coord, start=-315, extent=45, fill="#004030",width=circle_width,outline="#005090")
    internal_arc8 = canvas.create_arc(internal_coord, start=-315, extent=45, fill="#005090",width=circle_width,outline="#005070")

    return [
    [external_arc1,internal_arc1],
    [external_arc2,internal_arc2],
    [external_arc3,internal_arc3],
    [external_arc4,internal_arc4],
    [external_arc5,internal_arc5],
    [external_arc6,internal_arc6],
    [external_arc7,internal_arc7],
    [external_arc8,internal_arc8]
    ]


def overlayArcs():
    circleInner=canvas.create_oval(circle_x0+(circle_width*3),circle_y0+(circle_width*3),
                                    circle_x1-(circle_width*3),circle_y1-(circle_width*3),
                                    fill=bg_color,width=0,outline="")

    vertical_line=canvas.create_line(vertical_x0, vertical_y0, vertical_x1, vertical_y1,fill=bg_color, width=lines_width)
    horizontal_line=canvas.create_line(horizontal_x0, horizontal_y0, horizontal_x1, horizontal_y1, fill=bg_color, width=lines_width)
    diagonal_izq_der_line=canvas.create_line(diagona_izq_der_x0, diagona_izq_der_y0, diagona_izq_der_x1, diagona_izq_der_y1, fill=bg_color, width=lines_width)
    diagonal_der_izq_line=canvas.create_line(diagona_der_izq_x0, diagona_der_izq_y0, diagona_der_izq_x1, diagona_der_izq_y1, fill=bg_color, width=lines_width)

def redraw():
    global indice,arcs
    canvas.after(250,redraw)
    #Anterior Segmento, Reset Color
    canvas.itemconfig(arcs[indice-1][0], fill="#004030",outline="#004560") # change color
    canvas.itemconfig(arcs[indice-1][1], fill="#004560",outline="#005070") # change color
    #Segmento Actual, actualizar Color
    canvas.itemconfig(arcs[indice][0], fill="#0c9981",outline="#40C6EC") # change color
    canvas.itemconfig(arcs[indice][1], fill="#40F6EC",outline="#00A6CC") # change color
    indice = (indice+1)%len(arcs)
    canvas.update()


root=tk.Tk()
root.attributes('-fullscreen', True) # make main window full-screen
root.update()
screen_width = root.winfo_width()
screen_height = root.winfo_height()
center = (screen_width/2,screen_height/2)
bg_color = 'BLACK'

#circle
diametroCirculo = 100
circle_width = 3
ovalOverflow = diametroCirculo/10
circle_x0 = center[0]-(diametroCirculo/2) - (ovalOverflow/2)
circle_y0 = center[1]-(diametroCirculo/2)
circle_x1 = circle_x0 + diametroCirculo + ovalOverflow
circle_y1 = circle_y0 + diametroCirculo

#cross
lines_width = diametroCirculo/10
vertical_x0 = center[0]
vertical_y0 = center[1] - (diametroCirculo/2)
vertical_x1 = vertical_x0
vertical_y1 = vertical_y0 + diametroCirculo

horizontal_x0 = center[0] - ((diametroCirculo+ovalOverflow)/2)
horizontal_y0 = center[1]
horizontal_x1 = horizontal_x0 + diametroCirculo + ovalOverflow
horizontal_y1 = horizontal_y0

diagona_izq_der_x0 = circle_x0
diagona_izq_der_y0 = circle_y0
diagona_izq_der_x1 = circle_x1
diagona_izq_der_y1 = circle_y1

diagona_der_izq_x0 = circle_x1
diagona_der_izq_y0 = circle_y0
diagona_der_izq_x1 = circle_x0
diagona_der_izq_y1 = circle_y1

indice = 0

canvas=tk.Canvas(root,width=screen_width,height=screen_height,bg=bg_color)
canvas.pack(expand=True, fill='both')
canvas.pack()
arcs = getArcs()
overlayArcs()
canvas.create_text(center[0],center[1]+(diametroCirculo/2)+20,fill="#40C6EC",font="System 18 bold",text="Cargando")

redraw()
root.mainloop()

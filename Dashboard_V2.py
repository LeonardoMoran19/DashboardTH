#Imports de Matplotlib
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as md

#Imports tkinter
import tkinter as tk
from tkinter import ttk

#Import tkcalendar
from tkcalendar import DateEntry

#Import data.py
from data import tempdata,humdata,obtdata,actdata

style.use("ggplot")
is_Live = True

#Inicializar gráficas de temperatura
temp_Figure, temp_axis = plt.subplots()

#Inicializar gráficas de humedad
hum_Figure, hum_axis = plt.subplots()


class Page(tk.Frame): #Pagina principal
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        is_Live = False
    def show(self):
        self.lift()

class live(Page): #Pestaña de datos en vivo
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs) 
        is_Live = True
        show_info(self)

class consu(Page): #Pestaña de consulta de datos (filtros por fecha)
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        is_Live = False

class csv(Page): #Pestaña de exportar CSV 
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       is_Live = False

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        #Instancias de las páginas
        livepage = live(self)
        consupage = consu(self)
        csvpage = csv(self)   

        #Creación de sección de botones (color morado)
        buttonframe = tk.Frame(self, bg="#4C2A85")
        buttonframe.pack(side="left", fill="y")

        #Creación de sección de gráficos (color blanco)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        ##
        livepage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        consupage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        csvpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        #Inicialización de página principal
        label = tk.Label(buttonframe, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
        label.pack(pady=50, padx=20)

        bttlive = tk.Button(buttonframe, text="Gráficos en vivo", bg="#4C2A85", fg="#FFF", font=25, command=livepage.show)
        bttlive.pack(pady=0, padx=20)

        bttgraph = tk.Button(buttonframe, text="Consultar gráficos", bg="#4C2A85", fg="#FFF", font=25,command= consupage.show)
        bttgraph.pack(pady=10, padx=20)

        bttcsv = tk.Button(buttonframe, text="Exportar CSV", bg="#4C2A85", fg="#FFF", font=25,command=csvpage.show)
        bttcsv.pack(pady=0, padx=20)

        #Contenedor para visulización de datos en vivo
        liveFrame = tk.Frame(livepage)
        liveFrame.pack(fill="both", expand=True)

        #Contenedor para ingreso de fechas
        consuFrame1 = tk.Frame(consupage)
        consuFrame1.pack(fill="both", expand=True)

        label=tk.Label(consuFrame1,text='Fecha')
        label.pack(side = "left")

        calendar = DateEntry(consuFrame1,selectmode='day')
        calendar.pack(side = "left", padx = 20,pady =10)
        
        #Contenedor para botón de actualización de datos
        consuFrame2 = tk.Frame(consupage)
        consuFrame2.pack(fill="both", expand=True)        

        refresh_Button = tk.Button(consuFrame1,text='Actualizar', command=lambda:update_Info(label,calendar,consuFrame2))
        refresh_Button.pack(side ="left", padx=10)

        #Estilo de gráficas
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

def configure_plots():
    #temp_Figure.set_size_inches(6,10)
    temp_axis.set_title("Temperatura")
    temp_axis.set_yticks(range(0, 30,2))
    temp_axis.xaxis.set_major_locator(md.SecondLocator(bysecond=range(60),interval = 30))
    temp_axis.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
    temp_Figure.autofmt_xdate()
    plt.xticks(rotation = 45)

    #temp_Figure.set_size_inches(6,10)
    hum_axis.set_title("Humedad")
    hum_axis.set_yticks(range(0, 100,5))
    hum_axis.xaxis.set_major_locator(md.SecondLocator(bysecond=range(60),interval = 30))
    hum_axis.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
    hum_Figure.autofmt_xdate()
    plt.xticks(rotation = 45)

def update_Info(label, calendar, This_Frame): 
    #Se limpian parámetros
    temp_axis.clear()
    hum_axis.clear()

    #Configuración de gráficas
    configure_plots()

    #Se obtiene la fecha seleccionada
    fecha=calendar.get_date()
    label.config(text=fecha)

    #Se consultan los datos de esa fecha
    obtdata(fecha)

    #Se setean parámetros
    temp_axis.plot(list(tempdata.keys()), list(tempdata.values()))
    hum_axis.plot(list(humdata.keys()), list(humdata.values()))   

    show_info(This_Frame)

def update_Temp_liveInfo(FrameData):
    temp_axis.clear()

    actdata() 

    #Se setean parámetros
    temp_axis.plot(list(tempdata.keys()), list(tempdata.values()))
    
    #Configuración de gráficas
    configure_plots()

def update_Hum_liveInfo(FrameData):
    hum_axis.clear()

    actdata()   
    
    #Se setean parámetros
    hum_axis.plot(list(humdata.keys()), list(humdata.values()))   
    
    #Configuración de gráficas
    configure_plots()

def show_info(This_Frame):
    #Se muestran los parámetros en las gráficas
    canvas1 = FigureCanvasTkAgg(temp_Figure, This_Frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
    
    canvas2 = FigureCanvasTkAgg(hum_Figure, This_Frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.state('zoomed')
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1000x600")
    configure_plots()

    if is_Live:
        temp_animation = animation.FuncAnimation(temp_Figure, update_Temp_liveInfo, interval=5000)
        hum_animation = animation.FuncAnimation(hum_Figure, update_Hum_liveInfo, interval=5000)
        
    root.mainloop()
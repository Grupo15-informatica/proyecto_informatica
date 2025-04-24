from steps import *

def ploi():
    G=CreateGraph_1()
    plot(G)
def plot(g):
    fig,ax=plt.subplots()
    ax.clear()
    ax.grid(color='red', linestyle='dashed', linewidth=0.5)
    for node in g.nodes:
        ax.plot(node.x, node.y, 'o', color='red', markersize=5)
        ax.text(node.x + 0.2, node.y + 0.2, node.nombre, color='green',
                weight='bold', fontsize=8)
    for segment in g.segments:
        dx = segment.destino.x - segment.origen.x
        dy = segment.destino.y - segment.origen.y
        ax.arrow(segment.origen.x, segment.origen.y, dx, dy,
                 head_width=0.5, head_length=0.5, ec='blue', linewidth=1, length_includes_head=True)
        cx = (segment.origen.x + segment.destino.x) / 2
        cy = (segment.origen.y + segment.destino.y) / 2
        ax.text(cx, cy, round(segment.cost, 2), fontsize=9, color='black')
    ax.set_title('Gráfico con nodos y segmentos')
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    if 'canvas_picture' in globals():
        canvas_picture.grid_forget()
    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=400)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5,
                        sticky=tk.N + tk.E + tk.W + tk.S)
    return fig,ax
def mostrar_archivo():
    filepath = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.py *.txt")])
    if not filepath:
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        contenido = f.read()
    text_widget = scrolledtext.ScrolledText(picture_frame, wrap=tk.WORD, width=80, height=25)
    text_widget.insert(tk.END, contenido)
    text_widget.config(state='disabled')
    for widget in picture_frame.winfo_children():
        widget.destroy()
    text_widget.grid(row=0, column=0, padx=5, pady=5)
def plotnode(g,a):
    fig, ax = plt.subplots()
    ax.clear()
    ax.grid(color='red', linestyle='dashed', linewidth=0.5)
    i = 0
    while i < len(g.nodes):
        ax.plot(g.nodes[i].x, g.nodes[i].y, 'o', color='gray', markersize=5)
        ax.text(g.nodes[i].x + 0.2, g.nodes[i].y + 0.2, g.nodes[i].nombre, color='green',
                weight='bold', fontsize=8)
        i = i + 1
    i = 0
    encontrado = False
    while i < len(g.nodes) and not encontrado:
        if g.nodes[i].nombre == a:
            ax.plot(g.nodes[i].x, g.nodes[i].y, 'o', color='red', markersize=5)
            encontrado = True
        i = i + 1
    i = 0
    while i < len(g.segments):
        if g.segments[i].origen.nombre == a:
            ax.arrow(g.segments[i].origen.x, g.segments[i].origen.y,
                     g.segments[i].destino.x - g.segments[i].origen.x,
                     g.segments[i].destino.y - g.segments[i].origen.y, head_width=0.5, head_length=0.5,
                     ec='blue',
                     linewidth=1)
            ax.text((g.segments[i].destino.x + g.segments[i].origen.x) / 2,
                    (g.segments[i].destino.y + g.segments[i].origen.y) / 2,
                    round(g.segments[i].cost, 2), fontsize=9, color='black')
        i = i + 1
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    if 'canvas_picture' in globals():
        canvas_picture.grid_forget()
    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=400)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5,
                        sticky=tk.N + tk.E + tk.W + tk.S)
def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = float(event.xdata), float(event.ydata)
        a=GetClosest(G,x,y).nombre
        plotnode(G,a)
def mostrarvecinos(g):
    fig,ax=plot(g)
    messagebox.showinfo("Información", "Clica en el nodo cuyos vecinos quieras conocer")
    fig.canvas.mpl_connect('button_press_event', on_click)
def on_click2(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = float(event.xdata), float(event.ydata)
        a=simpledialog.askstring("Nuevo nodo", "¿Cómo quieres llamar al nuevo nodo?")
        if a:
            n=Node(a,x,y)
            AddNode(G,n)
            plot(G)
def addnode(g):
    fig, ax = plot(g)
    messagebox.showinfo("Información", "Clica allá donde quieras añadir un nodo")
    fig.canvas.mpl_connect('button_press_event', on_click2)
def addsegment(g):
    fig, ax = plot(g)

    nombre = simpledialog.askstring("Nombre segmento", "¿Cómo se llama el segmento?")
    if not nombre:
        return
    estado = {'paso': 'origen', 'origen': None}
    messagebox.showinfo("Información", "Clica en el nodo de origen")
    def on_click(event):
        if event.xdata is None or event.ydata is None:
            return
        x, y = float(event.xdata), float(event.ydata)
        nodo = GetClosest(G, x, y).nombre
        if estado['paso'] == 'origen':
            estado['origen'] = nodo
            estado['paso'] = 'destino'
            messagebox.showinfo("Información", "Ahora clica en el nodo de destino")
        else:
            AddSegment(G, nombre, estado['origen'], nodo)
            fig.canvas.mpl_disconnect(cid)  # Quitamos el evento para evitar más clics
            plot(G)  # Redibujar con el nuevo segmento
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
def eliminar(g):
    def on_click4(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = float(event.xdata), float(event.ydata)
            a = GetClosest(G, x, y).nombre
            c=GetClosest(G,x,y).x
            i=0
            found=False
            while i<len(g.nodes) and not found:
                if g.nodes[i].nombre==a:
                    del g.nodes[i]
                    found=True
                i=i+1
            i=0
            while i<len(g.segments):
                if g.segments[i].origen.nombre==a:
                    del g.segments[i]
                    i=i-1
                    print('correctoOrigen')
                i=i+1
            i = 0
            while i < len(g.segments):
                if g.segments[i].destino.nombre == a:
                    del g.segments[i]
                    i=i-1
                    print('correctoDestino')
                i=i+1
        fig,ax=plot(g)
        canvas = FigureCanvasTkAgg(fig, master=picture_frame)
        canvas.draw()
        if 'canvas_picture' in globals():
            canvas_picture.grid_forget()
        canvas_picture = canvas.get_tk_widget()
        canvas_picture.config(width=600, height=400)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5,
                            sticky=tk.N + tk.E + tk.W + tk.S)
    fig, ax = plot(g)
    messagebox.showinfo("Información", "Clica en el nodo que quieras eliminar")
    fig.canvas.mpl_connect('button_press_event', on_click4)

#BASES DE LA ESTRUCTURA DEL TKINTER:
root=tk.Tk()
root.geometry('800x400')
root.title('Project: Versión 1')
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=10)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)

#FRAME IMÁGENES:
picture_frame=tk.LabelFrame(root,text='Imágenes')
picture_frame.grid(row=0,column=1,rowspan=2,padx=5,pady=5,sticky='nsew')
picture_frame.columnconfigure(index=0,weight=1)
picture_frame.rowconfigure(index=0,weight=1)
#root.rowconfigure(2,weight=1)

#FRAME STEP 5:
Step5_frame=tk.LabelFrame(root, text='Step 5')
Step5_frame.grid(row=0,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
Step5_frame.rowconfigure(index=0,weight=1)
Step5_frame.rowconfigure(index=1,weight=1)
Step5_frame.rowconfigure(index=2,weight=1)
Step5_frame.columnconfigure(index=0,weight=1)
button1=tk.Button(Step5_frame,text='Mostrar gráfico de ejemplo',command=lambda:ploi())
button1.grid(row=0,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button2=tk.Button(Step5_frame,text='Mostrar archivo de ejemplo',command=lambda:mostrar_archivo())
button2.grid(row=1,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button3=tk.Button(Step5_frame,text='Mostrar nodos vecinos',command=lambda:mostrarvecinos(G))
button3.grid(row=2,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)

#FRAME STEP 6:
button_graphs_frame=tk.LabelFrame(root,text='Step 6')
button_graphs_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button_graphs_frame.rowconfigure(index=0,weight=1)
button_graphs_frame.rowconfigure(index=1,weight=1)
button_graphs_frame.rowconfigure(index=2,weight=1)
button_graphs_frame.rowconfigure(index=3,weight=1)
button_graphs_frame.columnconfigure(index=0,weight=1)
button3=tk.Button(button_graphs_frame,text='Añadir nodo',command=lambda:addnode(G))
button3.grid(row=0,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button4=tk.Button(button_graphs_frame,text='Añadir segmento',command=lambda:addsegment(G))
button4.grid(row=1,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button5=tk.Button(button_graphs_frame,text='Eliminar nodo y sus segmentos',command=lambda:eliminar(G))
button5.grid(row=2,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)
button6=tk.Button(button_graphs_frame,text='Guardar gráfico en un archivo')
button6.grid(row=3,column=0,padx=5,pady=5,sticky=tk.N+tk.E+tk.W+tk.S)

root.mainloop()

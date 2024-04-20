import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_graph():
    x = [1, 2, 3, 4, 5]
    y = [int(entry1.get()), int(entry2.get()), int(entry3.get()), int(entry4.get()), int(entry5.get())]
    fig, ax = plt.subplots()
    ax.plot(x, y)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


window = tk.Tk()
window.title("График на основе введенных значений")

label = ttk.Label(window, text="Введите значения для Y:")
label.pack()

entry1 = ttk.Entry(window)
entry1.pack()
entry2 = ttk.Entry(window)
entry2.pack()
entry3 = ttk.Entry(window)
entry3.pack()
entry4 = ttk.Entry(window)
entry4.pack()
entry5 = ttk.Entry(window)
entry5.pack()

button = ttk.Button(window, text="Построить график", command=plot_graph)
button.pack()

window.mainloop()

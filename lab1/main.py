import tkinter as tk
from tkinter import ttk
import colorsys

Flag = False

def rgb_to_cmyk(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k < 1:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    else:
        c = m = y = 0
    return (c, m, y, k)

def cmyk_to_rgb(c, m, y, k):
    r = int(255 * (1 - c) * (1 - k))
    g = int(255 * (1 - m) * (1 - k))
    b = int(255 * (1 - y) * (1 - k))
    return (r, g, b)


def rgb_to_hls(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return h * 360, l * 100, s * 100


def hls_to_rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)


def update_entry(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

def update_color():
    r = int(r_slider.get())
    g = int(g_slider.get())
    b = int(b_slider.get())

    c, m, y, k = c_slider.get(), m_slider.get(), y_slider.get(), k_slider.get()
    h, l, s = h_slider.get(), l_slider.get(), s_slider.get()
    
    color = f'#{r:02x}{g:02x}{b:02x}'
    color_box.config(bg=color)

    update_entry(r_entry, r)
    update_entry(g_entry, g)
    update_entry(b_entry, b)

    update_entry(c_entry, c)
    update_entry(m_entry, m)
    update_entry(y_entry, y)
    update_entry(k_entry, k)

    update_entry(h_entry, h)
    update_entry(s_entry, s)
    update_entry(l_entry, l)


def set_cmyk_slider(c, m, y, k):
    global Flag 
    Flag = True
    c_slider.set(c)
    m_slider.set(m)
    y_slider.set(y)
    k_slider.set(k)
    Flag = False

def set_hls_slider(h, l, s):
    global Flag 
    Flag = True
    h_slider.set(h)
    l_slider.set(l)
    s_slider.set(s)
    Flag = False

def set_rgb_slider(r, g, b):
    global Flag
    Flag = True
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)
    Flag = False

def update_from_rgb(*args):
    global Flag
    if Flag:
        return
    Flag = True
    print("update from rgb")
    r, g, b = r_slider.get(), g_slider.get(), b_slider.get()
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = rgb_to_hls(r, g, b)
    
    set_cmyk_slider(c, m, y, k)
    set_hls_slider(h, l, s)
    update_color()
    Flag = False

def update_from_cmyk(*args):
    global Flag
    if Flag == True:
        return
    print("update from cmyk")
    Flag = True
    c = c_slider.get()
    m = m_slider.get()
    y = y_slider.get()
    k = k_slider.get()
    
    r, g, b = cmyk_to_rgb(c, m, y, k)
    set_rgb_slider(r, g, b)
    h, l, s = rgb_to_hls(r, g, b)
    set_hls_slider(h, l, s)
    
    update_color()  
    Flag = False

def update_from_hls(*args):
    global Flag
    if Flag:
        return
    print("update from hls")
    Flag = True
    h = h_slider.get() 
    s = s_slider.get()
    l = l_slider.get()
    r, g, b = hls_to_rgb(h, l, s)
    
    set_rgb_slider(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)
    
    set_cmyk_slider(c, m, y, k)
    update_color()  
    Flag = False

def update_rgb_from_entry(slider, entry):
    print("update from entry rgb")
    value = entry.get()
    if value.isdigit():
        value = int(value)
        if slider == r_slider:
            r_slider.set(max(0, min(value, 255)))
        elif slider == g_slider:
            g_slider.set(max(0, min(value, 255)))
        elif slider == b_slider:
            b_slider.set(max(0, min(value, 255)))
    update_color()

def update_cmyk_from_entry(slider, entry):
    value = entry.get()
    if value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
        value = float(value)
        if slider == c_slider:
            c_slider.set(max(0, min(value, 1)))
        elif slider == m_slider:
            m_slider.set(max(0, min(value, 1)))
        elif slider == y_slider:
            y_slider.set(max(0, min(value, 1)))
        elif slider == k_slider:
            k_slider.set(max(0, min(value, 1)))
    update_from_cmyk()

def update_hls_from_entry(slider, entry):
    value = entry.get()
    if value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
        value = float(value)
        if slider == h_slider:
            h_slider.set(max(0, min(value, 360)))
        elif slider == s_slider:
            s_slider.set(max(0, min(value, 100)))
        elif slider == l_slider:
            l_slider.set(max(0, min(value, 100)))
    update_from_hls()

root = tk.Tk()
root.title('Цветовые модели')

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# RGB
ttk.Label(frame, text='R:').grid(column=0, row=0)
r_var = tk.DoubleVar()
r_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', variable=r_var)
r_slider.set(0)
r_slider.grid(column=1, row=0)
r_entry = ttk.Entry(frame, width=5)
r_entry.grid(column=2, row=0)
r_entry.insert(0, '0')
r_entry.bind("<Return>", lambda _: update_rgb_from_entry(r_slider, r_entry))


ttk.Label(frame, text='G:').grid(column=0, row=1)
g_var = tk.DoubleVar()
g_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', variable=g_var)
g_slider.set(0)
g_slider.grid(column=1, row=1)
g_entry = ttk.Entry(frame, width=5)
g_entry.grid(column=2, row=1)
g_entry.insert(0, '0')
g_entry.bind("<Return>", lambda _: update_rgb_from_entry(g_slider, g_entry))


ttk.Label(frame, text='B:').grid(column=0, row=2)
b_var = tk.DoubleVar()
b_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', variable=b_var)
b_slider.set(0)
b_slider.grid(column=1, row=2)
b_entry = ttk.Entry(frame, width=5)
b_entry.grid(column=2, row=2)
b_entry.insert(0, '0')
b_entry.bind("<Return>", lambda _: update_rgb_from_entry(b_slider, b_entry))


r_var.trace("w", update_from_rgb)
g_var.trace("w", update_from_rgb)
b_var.trace("w", update_from_rgb)
color_box = tk.Label(frame, text=' ', width=20, height=5, relief='solid')
color_box.grid(column=0, row=3, columnspan=3)

#CMYK

ttk.Label(frame, text='C:').grid(column=0, row=4)
c_var = tk.DoubleVar()
c_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', variable=c_var)
c_slider.set(0)
c_slider.grid(column=1, row=4)
c_entry = ttk.Entry(frame, width=5)
c_entry.grid(column=2, row=4)
c_entry.insert(0, '0.00')
c_entry.bind("<Return>", lambda _: update_cmyk_from_entry(c_slider, c_entry))

ttk.Label(frame, text='M:').grid(column=0, row=5)
m_var = tk.DoubleVar()
m_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', variable=m_var)
m_slider.set(0)
m_slider.grid(column=1, row=5)
m_entry = ttk.Entry(frame, width=5)
m_entry.grid(column=2, row=5)
m_entry.insert(0, '0.00')
m_entry.bind("<Return>", lambda _: update_cmyk_from_entry(m_slider, m_entry))

ttk.Label(frame, text='Y:').grid(column=0, row=6)
y_var = tk.DoubleVar()
y_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', variable=y_var)
y_slider.set(0)
y_slider.grid(column=1, row=6)
y_entry = ttk.Entry(frame, width=5)
y_entry.grid(column=2, row=6)
y_entry.insert(0, '0.00')
y_entry.bind("<Return>", lambda _: update_cmyk_from_entry(y_slider, y_entry))

ttk.Label(frame, text='K:').grid(column=0, row=7)
k_var = tk.DoubleVar()
k_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', variable=k_var)
k_slider.set(0)
k_slider.grid(column=1, row=7)
k_entry = ttk.Entry(frame, width=5)
k_entry.grid(column=2, row=7)
k_entry.insert(0, '0.00')
k_entry.bind("<Return>", lambda _: update_cmyk_from_entry(k_slider, k_entry))

c_var.trace("w", update_from_cmyk)
m_var.trace("w", update_from_cmyk)
y_var.trace("w", update_from_cmyk)
k_var.trace("w", update_from_cmyk)

# HLS
ttk.Label(frame, text='H:').grid(column=0, row=9)
h_var = tk.DoubleVar()
h_slider = tk.Scale(frame, from_=0, to=360, resolution=0.01, orient='horizontal', variable=h_var)
h_slider.set(0)
h_slider.grid(column=1, row=9)
h_entry = ttk.Entry(frame, width=5)
h_entry.grid(column=2, row=9)
h_entry.insert(0, '0.00')
h_entry.bind("<Return>", lambda _: update_hls_from_entry(h_slider, h_entry))

ttk.Label(frame, text='S:').grid(column=0, row=10)
s_var = tk.DoubleVar()
s_slider = tk.Scale(frame, from_=0, to=100, resolution=0.01, orient='horizontal', variable=s_var)
s_slider.set(0)
s_slider.grid(column=1, row=10)
s_entry = ttk.Entry(frame, width=5)
s_entry.grid(column=2, row=10)
s_entry.insert(0, '0.00')
s_entry.bind("<Return>", lambda _: update_hls_from_entry(s_slider, s_entry))

ttk.Label(frame, text='L:').grid(column=0, row=11)
l_var = tk.DoubleVar()
l_slider = tk.Scale(frame, from_=0, to=100, resolution=0.01, orient='horizontal', variable=l_var)
l_slider.set(0)
l_slider.grid(column=1, row=11)
l_entry = ttk.Entry(frame, width=5)
l_entry.grid(column=2, row=11)
l_entry.insert(0, '0.00')
l_entry.bind("<Return>", lambda _: update_hls_from_entry(l_slider, l_entry))


h_var.trace("w", update_from_hls)
s_var.trace("w", update_from_hls)
l_var.trace("w", update_from_hls)

root.mainloop()
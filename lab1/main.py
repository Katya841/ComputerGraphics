import tkinter as tk
from tkinter import ttk
import colorsys

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

def update_color():
    r = int(r_slider.get())
    g = int(g_slider.get())
    b = int(b_slider.get())
    
    color = f'#{r:02x}{g:02x}{b:02x}'
    color_box.config(bg=color)

    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h = h * 360  

    c_slider.set(c)
    m_slider.set(m)
    y_slider.set(y)
    k_slider.set(k)
    h_slider.set(h)
    s_slider.set(s)
    l_slider.set(l)

    cmyk_label.config(text=f'CMYK: {c:.2f}, {m:.2f}, {y:.2f}, {k:.2f}')
    hls_label.config(text=f'HLS: {h:.2f}, {s:.2f}, {l:.2f}')

    r_entry.delete(0, tk.END)
    r_entry.insert(0, str(r))
    g_entry.delete(0, tk.END)
    g_entry.insert(0, str(g))
    b_entry.delete(0, tk.END)
    b_entry.insert(0, str(b))
    
    c_entry.delete(0, tk.END)
    c_entry.insert(0, f"{c:.2f}")
    m_entry.delete(0, tk.END)
    m_entry.insert(0, f"{m:.2f}")
    y_entry.delete(0, tk.END)
    y_entry.insert(0, f"{y:.2f}")
    k_entry.delete(0, tk.END)
    k_entry.insert(0, f"{k:.2f}")
    
    h_entry.delete(0, tk.END)
    h_entry.insert(0, f"{h:.2f}")
    s_entry.delete(0, tk.END)
    s_entry.insert(0, f"{s:.2f}")
    l_entry.delete(0, tk.END)
    l_entry.insert(0, f"{l:.2f}")

def update_rgb_from_cmyk(*args):
    c = c_slider.get()
    m = m_slider.get()
    y = y_slider.get()
    k = k_slider.get()
    r, g, b = cmyk_to_rgb(c, m, y, k)
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)
    update_color()

def update_rgb_from_hls(*args):
    h = h_slider.get() / 360  
    s = s_slider.get()
    l = l_slider.get()
    r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)
    update_color()

def update_rgb_from_entry(slider, entry):
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
    update_rgb_from_cmyk()

def update_hls_from_entry(slider, entry):
    value = entry.get()
    if value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
        value = float(value)
        if slider == h_slider:
            h_slider.set(max(0, min(value, 360)))
        elif slider == s_slider:
            s_slider.set(max(0, min(value, 1)))
        elif slider == l_slider:
            l_slider.set(max(0, min(value, 1)))
    update_rgb_from_hls()


root = tk.Tk()
root.title('Цветовые модели')

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# RGB
ttk.Label(frame, text='R:').grid(column=0, row=0)
r_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', command=lambda _: update_color())
r_slider.set(0)
r_slider.grid(column=1, row=0)
r_entry = ttk.Entry(frame, width=5)
r_entry.grid(column=2, row=0)
r_entry.insert(0, '0')
r_entry.bind("<Return>", lambda _: update_rgb_from_entry(r_slider, r_entry))

ttk.Label(frame, text='G:').grid(column=0, row=1)
g_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', command=lambda _: update_color())
g_slider.set(0)
g_slider.grid(column=1, row=1)
g_entry = ttk.Entry(frame, width=5)
g_entry.grid(column=2, row=1)
g_entry.insert(0, '0')
g_entry.bind("<Return>", lambda _: update_rgb_from_entry(g_slider, g_entry))

ttk.Label(frame, text='B:').grid(column=0, row=2)
b_slider = tk.Scale(frame, from_=0, to=255, orient='horizontal', command=lambda _: update_color())
b_slider.set(0)
b_slider.grid(column=1, row=2)
b_entry = ttk.Entry(frame, width=5)
b_entry.grid(column=2, row=2)
b_entry.insert(0, '0')
b_entry.bind("<Return>", lambda _: update_rgb_from_entry(b_slider, b_entry))


color_box = tk.Label(frame, text=' ', width=20, height=5, relief='solid')
color_box.grid(column=0, row=3, columnspan=3)

# CMYK
ttk.Label(frame, text='C:').grid(column=0, row=4)
c_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_cmyk)
c_slider.set(0)
c_slider.grid(column=1, row=4)
c_entry = ttk.Entry(frame, width=5)
c_entry.grid(column=2, row=4)
c_entry.insert(0, '0.00')
c_entry.bind("<Return>", lambda _: update_cmyk_from_entry(c_slider, c_entry))

ttk.Label(frame, text='M:').grid(column=0, row=5)
m_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_cmyk)
m_slider.set(0)
m_slider.grid(column=1, row=5)
m_entry = ttk.Entry(frame, width=5)
m_entry.grid(column=2, row=5)
m_entry.insert(0, '0.00')
m_entry.bind("<Return>", lambda _: update_cmyk_from_entry(m_slider, m_entry))

ttk.Label(frame, text='Y:').grid(column=0, row=6)
y_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_cmyk)
y_slider.set(0)
y_slider.grid(column=1, row=6)
y_entry = ttk.Entry(frame, width=5)
y_entry.grid(column=2, row=6)
y_entry.insert(0, '0.00')
y_entry.bind("<Return>", lambda _: update_cmyk_from_entry(y_slider, y_entry))

ttk.Label(frame, text='K:').grid(column=0, row=7)
k_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_cmyk)
k_slider.set(0)
k_slider.grid(column=1, row=7)
k_entry = ttk.Entry(frame, width=5)
k_entry.grid(column=2, row=7)
k_entry.insert(0, '0.00')
k_entry.bind("<Return>", lambda _: update_cmyk_from_entry(k_slider, k_entry))

cmyk_label = ttk.Label(frame, text='CMYK: ')
cmyk_label.grid(column=0, row=8, columnspan=3)

# HLS
ttk.Label(frame, text='H:').grid(column=0, row=9)
h_slider = tk.Scale(frame, from_=0, to=360, orient='horizontal', command=update_rgb_from_hls)
h_slider.set(0)
h_slider.grid(column=1, row=9)
h_entry = ttk.Entry(frame, width=5)
h_entry.grid(column=2, row=9)
h_entry.insert(0, '0')
h_entry.bind("<Return>", lambda _: update_hls_from_entry(h_slider, h_entry))

ttk.Label(frame, text='S:').grid(column=0, row=10)
s_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_hls)
s_slider.set(0)
s_slider.grid(column=1, row=10)
s_entry = ttk.Entry(frame, width=5)
s_entry.grid(column=2, row=10)
s_entry.insert(0, '0.00')
s_entry.bind("<Return>", lambda _: update_hls_from_entry(s_slider, s_entry))

ttk.Label(frame, text='L:').grid(column=0, row=11)
l_slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient='horizontal', command=update_rgb_from_hls)
l_slider.set(0)
l_slider.grid(column=1, row=11)
l_entry = ttk.Entry(frame, width=5)
l_entry.grid(column=2, row=11)
l_entry.insert(0, '0.00')
l_entry.bind("<Return>", lambda _: update_hls_from_entry(l_slider, l_entry))

hls_label = ttk.Label(frame, text='HLS: ')
hls_label.grid(column=0, row=12, columnspan=3)


update_color()


root.mainloop()
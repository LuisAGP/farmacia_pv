from tkinter import *


root = Tk()
root.title=("Scrollbar practice")
root.geometry("500x400")

# Create a main frame
# Create a canvas
# Add a Scrollbar
# Configura de Canvas
# Create a new Frame

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scroll = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scroll.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scroll.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

second_frame = Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw", width=480)


for i in range(100):
    Button(second_frame, text=f"Button {i} ready!", height=15).pack(pady=3, padx=20, fill=X, expand=1)


Button(second_frame, text=f"Button {100} ready!").pack(pady=3, fill=X, expand=1)

root.mainloop()

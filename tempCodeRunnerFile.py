        lblM = tk.Label(c, text='Failed!!!Press Enter key to start again')
        lblID = c.create_window(100, 190, anchor='nw', window=lblM)
        c.itemconfigure(lblID, state='hidden')
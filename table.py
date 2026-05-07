from tkinter import Label, Frame

# a class that manages the table of data
class Table(Frame): # this is an example of inheritance
    def __init__(self,master,db_manager,bg_colour="white",font=("Arial",12)):
        super().__init__(master)
        self.master = master # window
        self.db_manager = db_manager
        self.font = font
        self.bg_colour = bg_colour
        self.order_by = ""
        self.order = ""
        self.headings, self.data = self.get_data()
        self.title_text="Data currently held in tblHistoricItems"

    # method that binds the change_sort method to certain headers and updates the text colours
    def bind_headers(self):
        for i in self.headers:
            self.set_colour(i) # makes all text black explicitly 
            # system default looks black, but is stored as SystemButtonText
            if self.headers.index(i) > 1: i.bind("<Button>",self.change_sort) # cannot order by rank or username
        self.set_colour(self.headers[2],"#84B987")

    # method that allows the leaderboard to be sorted differently depending on what headers are clicked
    # if you keep clicking the same header, it will switch between ASC (red) / DESC (green) 
    def change_sort(self,event):
        column_names = self.db_manager.get_leaderboard_column_names()
        if event.widget["foreground"] == "#000000": # means new column was selected
            self.set_colour(event.widget,"#84B987")
            self.order = "DESC"
            for i in self.headers: # sets all other widgets to black
                if i != event.widget: self.set_colour(i) 
        elif event.widget["foreground"] == "#84B987":
            self.set_colour(event.widget,"#9D716B")
            self.order = "ASC"
        else: 
            self.set_colour(event.widget,"#84B987")
            self.order = "DESC"
        # gets actual column name (key) from the display name the user sees (value) 
        self.order_by = [key for key, value in column_names.items() if value == event.widget["text"]][0]
        self.recalculate_data()
        
    # method to change text colour of widget. default text is black 
    def set_colour(self,widget,colour="#000000"):
        widget["foreground"] = colour

    # getter that returns result of SQL query as a list of tuples
    def get_data(self):
        return self.db_manager.get_leaderboard(self.singleplayer,order_by=self.order_by,order=self.order,
                                               table1_difficulty=self.table1_difficulty)

    # setter to change value of table1_difficulty attribute
    def set_table_difficulty(self, difficulty):
        self.table1_difficulty = difficulty

    # updates heading and data tuples before showing leaderboard
    def recalculate_data(self):
        self.headings, self.data = self.get_data()
        self.show_leaderboard()

    # destroys all children
    def clear_leaderboard(self):
        for widget in self.winfo_children():
            if widget not in self.headers:
                widget.destroy()

    # method that displays top/lowest 5 scores, with column headings
    def show_leaderboard(self):
        self.clear_leaderboard()
        # increases font size by 40% for title
        title = Label(self,font=(self.font[0],int(self.font[1]*1.4)), text = self.title_text)
        # calculates dimensions of "table"
        row_number = len(self.data)
        column_number = len(self.headings)
        column_width = [len(i) for i in self.headings]
        # adds title to the leaderboard
        title.grid(row=0,column=0,columnspan=column_number)
        # creates labels for each field and places them in a grid,
        # creating the appearance of a table
        for i in range(0,row_number):
            for j in range(column_number):
                field = Label(self,font=self.font,width=column_width[j],
                              bg=self.bg_colour, text = self.data[i][j])
                field.grid(row=i+2,column=j)
        self.show_message()

    # separate method to place headers as headers only need to be placed when the leaderboard is first shown
    def show_headers(self):
        # creates the heading labels and places them in a row
        self.headers = []
        for i in range(len(self.headings)):
            header = Label(self,font=self.font, text = self.headings[i])
            self.headers.append(header)
            header.grid(row=1,column=i)
        self.bind_headers()

    # method to show explanatory message
    def show_message(self):
        message = Label(self,text="Press the headers to re-sort the leaderboard!",font=("Helvetica",12))
        message.grid(row=7,pady=20,columnspan=6)

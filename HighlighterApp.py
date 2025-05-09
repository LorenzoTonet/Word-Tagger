import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import string

class HighlightApp:
    def __init__(self, root, color_dict):
        self.tr = root
        self.tr.title("Tagger di testo")
        self.tr.iconbitmap(r"Tools\Tag_tool_icon.ico")

        # Impostazione del font 
        custom_font = ("Arial", 12, "normal")

        self.menubar = tk.Menu(self.tr)

        # file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Apri", command=self.open_file)
        self.tr.bind_all("<Control-a>", lambda event: self.open_file())
        self.file_menu.add_command(label="Salva", command=self.save_file, accelerator="Ctrl+s")
        self.tr.bind_all("<Control-s>", lambda event: self.save_file())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Esci", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        # format menu
        self.editor = tk.Text(self.tr, wrap='word')
        self.editor.config(font=custom_font)
        self.format_menu = tk.Menu(self.menubar, tearoff=0)
        self.remove_menu = tk.Menu(self.menubar, tearoff=0)
        # tag dict
        self.tag_dict = color_dict
        self.TAG = ""
        # inizializziamo tutti i vari tag
        self.process()
        self.tr.bind_all("<Control-y>",lambda event : self.tag_text())

        self.editor.pack(expand=True, fill='both')
        self.tr.config(menu=self.menubar)
    
    def process(self):
        # se non viene passato lo carichiamo di default da un file in cui salviamo un dizionario
        if self.tag_dict == None:
            my_input_dict = open("Tools\default_dict.txt","r") # ci prendiamo il dizionario da un file su cui viene scritto
            self.tag_dict = {linea.split(":")[0]:linea.split(":")[1].strip() for linea in my_input_dict}

        for tags in self.tag_dict:
            self.editor.tag_configure(tags, background=self.tag_dict[tags])
            self.format_menu.add_command(label=f"Tag {tags}", command=self.tag_text_parametrico(tags), accelerator="Select then Ctrl+y")
        
        self.menubar.add_cascade(label="Tag", menu=self.format_menu)
        self.menubar.add_separator()
        for tags in self.tag_dict:
            self.remove_menu.add_command(label=f"Rimuovi {tags}", command=self.rimuovi_tag_parametrico(tags))
        self.remove_menu.add_separator()
        self.remove_menu.add_command(label="Rimuovi tutto", command=self.remove_all_tags)
        self.menubar.add_cascade(label="Rimozione", menu = self.remove_menu)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.editor.delete('1.0', 'end')
                self.editor.insert(tk.END, file.read())
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        file = open(file_path, "w")
        contenuto = self.editor.get('1.0', 'end')
        righe = contenuto.split("\n")
        res_per_riga = {i:" " for i in range(len(righe))}
        for tags in self.tag_dict:
            t = self.editor.tag_ranges(tags)
            for i in range (0, len(t), 2) :
                k = self.riga_di_appartenenza(t[i])
                res_per_riga[k] = f"{res_per_riga[k]} {self.formattamento_buono(tags, t[i], t[i+1])}"
        for i in range(len(righe)):
            res_per_riga[i] = res_per_riga[i][:-1]
            file.write(self.formatta_riga(righe[i], res_per_riga[i]))
            file.write("\n")
        file.close()

    def riga_di_appartenenza(self, t):
        return int(str(t).split(".")[0]) - 1
    
    def formattamento_buono(self, tag, t1, t2):
        starting_index = str(t1).split(".")[1]
        ending_index = str(t2).split(".")[1]
        tag = tag
        return f"({starting_index}; {ending_index}; {tag}) ,"
    
    def formatta_riga(self, riga, tags):
        return f"{riga.strip()}#{tags}"
    
    def tag_text_parametrico(self, tag):
        def tag_text():
            self.TAG = tag
            self.editor.tag_add(tag, "sel.first", "sel.last")
        return tag_text
    
    def tag_text(self):
        self.editor.tag_add(self.TAG, "sel.first", "sel.last")

    def rimuovi_tag_parametrico(self, tag):
        def remove_tag():
            self.editor.tag_remove(tag, "sel.first", "sel.last")
        return remove_tag
    
    def remove_all_tags(self):
        for tags in self.tag_dict:
            self.editor.tag_remove(tags, '1.0', 'end')

#----------------------------------------------------------

class WordListApp:
    def __init__(self, root):
        self.tr = root
        self.tr.title("Selezione di Tag")
        self.tr.geometry("500x400")
        self.tr.iconbitmap(r"Tools\Tag_tool_icon.ico")
        # Creazione di un oggetto di stile
        style = ttk.Style()
        # Impostazione del font globale
        custom_font = ("Arial", 12, "normal")
        style.configure('.', font=custom_font)  # Applica il font a tutti i widget

        self.my_label = ttk.Label(self.tr, text="Add your tags and choose colors")
        self.my_label.pack()

        self.word_color_dict = {}

        self.word_entry = ttk.Entry(self.tr)
        self.word_entry.pack()

        self.add_button = ttk.Button(self.tr, text="Add a Tag", command=self.add_word)
        self.add_button.pack()

        self.color_button = ttk.Button(self.tr, text="Choose Color", command=self.choose_color)
        self.color_button.pack()

        self.color_label = ttk.Label(self.tr, text="No color selected")
        self.color_label.pack()

        self.word_display = tk.Listbox(self.tr)
        self.word_display.config(font=custom_font)
        self.word_display.pack()

        self.color_button = ttk.Button(self.tr, text="Next", command=self.next)
        self.color_button.pack()

        # File button
        self.button_frame = ttk.Frame(self.tr)
        self.upload_button = ttk.Button(self.button_frame, text="Load dict", command=self.load_word_color_dict)
        self.upload_button.pack(side=tk.LEFT,padx=10, pady=10)
        self.upload_button = ttk.Button(self.button_frame, text="Upload dict", command=self.upload_word_color_dict)
        self.upload_button.pack(side=tk.LEFT, padx=10, pady=10 )
        self.button_frame.pack()

    def add_word(self):
        word = self.word_entry.get().strip()
        if word:
            if word not in self.word_color_dict:
                self.word_color_dict[word] = self.get_color()
            else:
                self.color_label.config(text="Word already exists")
                messagebox.showinfo("Error", "Word already exists!")
            self.update_word_display()
        else:
            self.color_label.config(text="No color selected")

    def update_word_display(self):
        self.word_display.delete(0, tk.END)
        for word, color in self.word_color_dict.items():
            self.word_display.insert(tk.END, f"{word}: {color}")
            self.word_display.itemconfig(tk.END, {'bg': color})

    def get_color(self):
        color = colorchooser.askcolor()[1]  # Get selected color
        if color:
            if color in self.word_color_dict.values():
                self.color_label.config(text="Color already selected")
                messagebox.showinfo("Error", "Color already selected!")
                return self.get_color()
            else:
                return color
            
    def choose_color(self):
        word = self.word_entry.get().strip()
        if word:
            color = colorchooser.askcolor()[1]  # Get selected color
            if color:
                if color in self.word_color_dict.values():
                    self.color_label.config(text="Color already selected")
                    messagebox.showinfo("Error", "Color already selected!")
                else:
                    self.word_color_dict[word] = color
                    self.color_label.config(text=f"Selected color: {color}")
                    self.update_word_display()

    def get_word_color_dict(self):
        return self.word_color_dict
    
    def upload_word_color_dict(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'w') as file:
                for tag in self.word_color_dict:
                    file.write(f"{tag}:{self.word_color_dict[tag]}\n")
    
    def load_word_color_dict(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.word_color_dict = {}
                try:
                    self.word_color_dict  ={linea.split(":")[0]:linea.split(":")[1].strip() for linea in file}
                except:
                    messagebox.showinfo("Error", "The file selected hasn't the right format")
                if self.check_correctness() == False:
                    messagebox.showinfo("Error", "The dictionary selected contains duplicates colors")
                    self.word_color_dict = {}
                self.update_word_display()

    def check_correctness(self):
        return len(self.word_color_dict.values()) == len(set(self.word_color_dict.values()))
    
    def next(self):
        if len(self.word_color_dict) == 0:
            self.show_alert()
        self.tr.destroy()
        self.tr = tk.Tk()
        
        if len(self.get_word_color_dict().keys()) == 0:
            app = HighlightApp(self.tr, None)
        else:
            app = HighlightApp(self.tr, self.get_word_color_dict())
        self.tr.mainloop() 
    
    def show_alert(self):
        messagebox.showwarning("Alert", "You have inserted no tags \n (A default palette will be used)")
        
#-----------------------------------------------

root = tk.Tk()
app = WordListApp(root)
root.mainloop()

    
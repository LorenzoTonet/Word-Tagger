import requests
import re
from bs4 import BeautifulSoup
import tkinter as tk
import string

def cleaningString(testo):
    # Regex to substitute multiple spaces with a single one
    testo_pulito = re.sub(r'\s+', ' ', testo)
    return testo_pulito.replace("\n", " ")

# Interface to get the user input as list of links
def get_user_input():
    def save_input():
        user_input.extend(text_entry.get("1.0", tk.END).strip().split("\n"))
        root.destroy()

    root = tk.Tk()
    root.title("User Input")
    
    text_frame = tk.Frame(root)
    text_frame.pack(pady=10)

    text_label = tk.Label(text_frame, text="Enter links:")
    text_label.pack(side=tk.LEFT)

    text_entry = tk.Text(text_frame, height=8, width=50)
    text_entry.pack(side=tk.LEFT)

    format_label = tk.Label(root, text="Enter links in separate lines. Press 'Save' when done.")
    format_label.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save", command=save_input)
    save_button.pack()

    root.mainloop()

user_input = []
get_user_input()

# Get the required pages at the same time
soup = []
for link in user_input:
    try:
        page = requests.get(link)
        soup.append(BeautifulSoup(page.content,'html.parser'))
    except:
        # Manage excess newlines in the input and invalid links
        if link == "": link = "empty"
        print('Error while getting the page with following link: ',link)

# Get all the text with the "p" tag in the paragraphs (not yet as text)
paragraphs_all = []
for s in soup:
    paragraphs_all.append(s.select('p'))

# Write the contents of all pages on separate txt files
for paragraphs in paragraphs_all:
    # Name the file after the title of the site
    name = soup[paragraphs_all.index(paragraphs)].title.string
    # Clean the name if it contains unusual characters
    name = ''.join(filter(lambda x: x in string.ascii_letters + string.digits + ' ', name)) + 'txt'
    with open(name,'w',encoding='utf-8', errors='ignore') as file:
        for p in paragraphs:
            cleaned = cleaningString(p.text.strip())
            file.write(cleaned)
            file.write('\n\n#---------------===============---------------#\n\n')
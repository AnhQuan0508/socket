import tkinter as tk
from tkinter import *
import socket
import base64
from PIL import Image, ImageTk
from io import BytesIO
import fitz

class EmailViewerApp:
  def __init__(self, master, email):
    self.master = master
    master.title("Email Viewer")

    self.email = email

    # Email List
    self.email_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    self.email_listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.email_listbox.bind('<<ListboxSelect>>', self.show_messages)

    # Message List
    self.message_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
    self.message_listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.message_listbox.bind('<<ListboxSelect>>', self.show_email_content)

    # Email Content
    self.email_content_text = tk.Text(master, wrap=tk.WORD, height=10, width=40)
    self.email_content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Initialize data (replace this with actual data retrieval logic)
    self.tk_image = None
    self.email_addresses = []
    self.messages = {}
    self.email_content = {}
    self.email_status = {}
    self.sock()

    self.auto_check_interval = 5000

    self.master.after(0, self.auto_check_and_update)

  def auto_check_and_update(self):
    # Perform the email check here
    self.sock()
    print(self.email_addresses)

    # Clear and repopulate the email_listbox with updated data
    self.email_listbox.delete(0, tk.END)
    for email in self.email_addresses:
        self.email_listbox.insert(tk.END, email)

    # Schedule the next auto-check and update
    self.master.after(self.auto_check_interval, self.auto_check_and_update)



  def check(self, base64_string):
    try:
      image_data = base64.b64decode(base64_string)
      image_buffer = BytesIO(image_data)
      return 1
    except:
      return 0
    
  def get_file(self, b):
    if b[:4] == "/9j/":
      image = self.get_img(b)
      # if image:
        # image.show()
      return image

    if b[:3] == "JVB":
      with open('output.pdf', 'wb') as file:
        file.write(base64.b64decode(b))
    
    with open('output.txt', 'wb') as file:
      file.write(base64.b64decode(b))
  
  def get_img(self, b):
    if b.startswith('data:image'):
      b = b.split(',')[1]

    print("1")
    # print(b)

    try:
      image_data = base64.b64decode(b)
      image_buffer = BytesIO(image_data)
      image = Image.open(image_buffer)
      return image
    except Exception as e:
      print("none")
      return None

  def show_messages(self, event):
    selected_email_index = self.email_listbox.curselection()
    if selected_email_index:
      selected_email = self.email_listbox.get(selected_email_index)
      messages = self.messages.get(selected_email, [])
      self.message_listbox.delete(0, tk.END)  # Clear previous messages
      for message in messages:
        status = "●" if self.email_status[message] == "Unread" else ""
        self.message_listbox.insert(tk.END, f"{message}{status}")

  def update_email_list(self, message_index, message):
    self.message_listbox.delete(message_index, message_index)
    self.message_listbox.insert(message_index, message.split('●')[0])


  def show_email_content(self, event):
    selected_message_index = self.message_listbox.curselection()
    if selected_message_index:
      selected_message = self.message_listbox.get(selected_message_index)
      email_content = self.email_content.get(selected_message.split('●')[0], "")

      parts = email_content.partition("Content-Type:")

      self.email_content_text.delete(1.0, tk.END)  # Clear previous content
      self.email_content_text.insert(tk.END, parts[0])

      b = ""
      img_text = parts[2].split()
      for part in img_text:
        if part[:4] == "name" or part[:8] == "filename": 
          continue
        if self.check(part) == 1: 
          b += part
        if part[:12] == "Content-Type" or part == ".":
          if b != "":
            image = self.get_file(b)
            if image:
              # resized_image = image.resize((100, 100), Image.ANTIALIAS)
              self.tk_image = ImageTk.PhotoImage(image)
              label = tk.Label(self.email_content_text, image=self.tk_image)
              label.image = self.tk_image
              self.email_content_text.window_create(tk.END, window=label)

            # if b.startswith('JVBERi'):
            #   # Display PDF
            #   pdf_data = base64.b64decode(b)
            #   pdf_buffer = BytesIO(pdf_data)
            #   pdf_document = fitz.open(pdf_buffer)
            #   pdf_page = pdf_document.load_page(0)
            #   image = pdf_page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
            #   resized_image = image.resize((100, 100), Image.ANTIALIAS)
            #   self.tk_image = ImageTk.PhotoImage(resized_image)
            #   label = tk.Label(self.email_content_text, image=self.tk_image)
            #   label.image = self.tk_image
            #   self.email_content_text.window_create(tk.END, window=label)
            # print(b)
            b = ""

      self.email_status[selected_message.split('●')[0]] = "Read"
      self.update_email_list(selected_message_index, selected_message)

    

  def receive_data(self, sock):
    email_data = b''
    while True:
      part = sock.recv(4096)
      email_data += part
      if len(part) < 4096:
        break

    return email_data

  def sock(self):
    email_address = self.email
    password = "your_password"

    pop_conn = socket.socket()
    pop_conn.connect(("localhost", 3335))

    recv = pop_conn.recv(1024).decode()
    print(recv)

    pop_conn.send(f'USER {email_address}\r\n'.encode())
    print(pop_conn.recv(1024).decode())

    pop_conn.send(f'PASS {password}\r\n'.encode())
    print(pop_conn.recv(1024).decode())

    pop_conn.sendall(b'STAT\r\n')
    response = pop_conn.recv(1024).decode()
    print(response)

    pop_conn.send(b'LIST\r\n')
    message_list = pop_conn.recv(1024).decode()
    print(message_list)

    pop_conn.send(b'UIDL\r\n')
    response = pop_conn.recv(1024).decode()

    for k in range(1, len(message_list.split()), 2):
      if message_list.split()[k] == '.':
        continue

      pop_conn.send(f'RETR {message_list.split()[k]}\r\n'.encode())
      email_data = self.receive_data(pop_conn)
      email_text = email_data.decode()
      email_parts = email_text.split()
      
      self.email_content[response.split()[k + 1]] = email_text
      # print(email_text)

      b = ""
      content = ""
      flag = 0
      for i, part in enumerate(email_parts):
        if part[:4] == "From":
          content += part
          content += email_parts[i+1]
          i + 1
          content+= '\n'
          if part.split(":")[1].strip() not in self.email_addresses:
            self.email_addresses.append(part.split(":")[1].strip()) 
            self.messages[part.split(":")[1].strip()] = []
          
          if response.split()[k + 1] not in self.messages[part.split(":")[1].strip()]:
            self.messages[part.split(":")[1].strip()].append(response.split()[k + 1])
            self.email_status[response.split()[k + 1]] = "Unread"

          continue
          
        if part[:3] == "To:":
          content += part
          content += email_parts[i+1]
          i + 1
          content += '\n'
          continue

        if part == "":
          continue

        if part[:4] == "name" or part[:8] == "filename":
          continue

        if part[:3] == "+OK":
          email_parts[i+1] =""
          continue

        if part[:4] == "Date":
          email_parts[i + 1] = ""
          content += part
          content += email_parts[i + 2]
          content += '\n'
          email_parts[i+2] = ""
          continue

        if part[:7] == "Subject":
          content += part
          content += email_parts[i+1]
          i = i + 1
          content += '\n\n'
          continue


    # for email in self.email_addresses:
    #   self.email_listbox.insert(tk.END, email)    




def main():
  root = tk.Tk()
  app = EmailViewerApp(root)
  root.mainloop()

if __name__ == "__main__":
  main()

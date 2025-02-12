import tkinter as tk

class EmailViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Email Viewer")

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

        # Initialize data with a new attribute for read/unread status
        self.email_addresses = ["john@example.com", "jane@example.com"]
        self.messages = {
            "john@example.com": ["Meeting Tomorrow", "Project Update"],
            "jane@example.com": ["Review Proposal", "Follow-up"]
        }
        self.email_content = {
            "Meeting Tomorrow": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Project Update": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Review Proposal": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Follow-up": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }

        self.email_status = {
            "Meeting Tomorrow": "Unread",
            "Project Update": "Unread",
            "Review Proposal": "Unread",
            "Follow-up": "Unread"
        }

        # Populate email list
        for email in self.email_addresses:
            self.email_listbox.insert(tk.END, email)

    def show_messages(self, event):
        selected_email_index = self.email_listbox.curselection()
        if selected_email_index:
            selected_email = self.email_listbox.get(selected_email_index)
            messages = self.messages.get(selected_email.split()[0], [])
            self.message_listbox.delete(0, tk.END)  # Clear previous messages
            for message in messages:
                print(self.email_status[message])
                status = "●" if self.email_status[message] == "Unread" else ""
                self.message_listbox.insert(tk.END, f"{message}{status}")

            # Mark the selected email as read and update its appearance
            # for message in messages:
            #     self.email_status[message] = "Read"
            # self.update_email_list()

    def update_email_list(self, message_index, message):
        self.message_listbox.delete(message_index, message_index)
        self.message_listbox.insert(message_index, message.split('●')[0])

    def show_email_content(self, event):
        selected_message_index = self.message_listbox.curselection()
        if selected_message_index:
            selected_message = self.message_listbox.get(selected_message_index)
            email_content = self.email_content.get(selected_message.split('●')[0], "")
            self.email_status[selected_message.split('●')[0]] = "Read"
            self.email_content_text.delete(1.0, tk.END)  # Clear previous content
            self.email_content_text.insert(tk.END, email_content)

            self.update_email_list(selected_message_index, selected_message)



def main():
    root = tk.Tk()
    app = EmailViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import json
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class JobApplication:
    def __init__(self, company, position, application_date, status, notes):
        self.company = company
        self.position = position
        self.application_date = application_date
        self.status = status
        self.notes = notes

    def __str__(self):
        return f"{self.company} - {self.position} (Applied: {self.application_date}, Status: {self.status}) Notes: {self.notes}"

class JobApplicationTracker:
    def __init__(self):
        self.applications = []

    def add_application(self, company, position, application_date, status, notes):
        new_application = JobApplication(company, position, application_date, status, notes)
        self.applications.append(new_application)
        return f'Added application for "{position}" at {company}.'

    def list_applications(self):
        return [str(app) for app in self.applications]

    def delete_application(self, index):
        try:
            index = int(index)
            if 0 <= index < len(self.applications):
                removed = self.applications.pop(index)
                return f'Removed application for "{removed.position}" at {removed.company}.'
            return "No such application exists."
        except ValueError:
            return "Error: Please specify the index as an integer."

    def search_application(self, keyword):
        matches = [
            str(app)
            for app in self.applications
            if keyword.lower() in app.company.lower() or keyword.lower() in app.position.lower()
        ]
        return matches if matches else [f'No applications found for "{keyword}".']

    def save_to_file(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump([vars(app) for app in self.applications], f, indent=4)
            return f'Saved applications to "{filename}".'
        except Exception as e:
            return f"Error saving file: {e}"

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.applications = [JobApplication(**entry) for entry in data]
            return f'Loaded applications from "{filename}".'
        except FileNotFoundError:
            return f'File "{filename}" not found.'
        except Exception as e:
            return f"Error loading file: {e}"

class JobApplicationGUI:
    def __init__(self, root):
        self.tracker = JobApplicationTracker()
        self.root = root
        self.root.title("Job Application Tracker")
        
        # Entry Fields
        tk.Label(root, text="Company:").grid(row=0, column=0)
        self.company_entry = tk.Entry(root)
        self.company_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Position:").grid(row=1, column=0)
        self.position_entry = tk.Entry(root)
        self.position_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Date Applied:").grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Status:").grid(row=3, column=0)
        self.status_entry = tk.Entry(root)
        self.status_entry.grid(row=3, column=1)
        
        tk.Label(root, text="Notes:").grid(row=4, column=0)
        self.notes_entry = tk.Entry(root)
        self.notes_entry.grid(row=4, column=1)
        
        # Buttons
        tk.Button(root, text="Add Application", command=self.add_application).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Delete Selected", command=self.delete_application).grid(row=6, column=0, columnspan=2)
        tk.Button(root, text="Search", command=self.search_application).grid(row=7, column=0, columnspan=2)
        tk.Button(root, text="Save", command=self.save_to_file).grid(row=8, column=0, columnspan=2)
        tk.Button(root, text="Load", command=self.load_from_file).grid(row=9, column=0, columnspan=2)
        
        # Listbox
        self.listbox = tk.Listbox(root, width=80, height=10)
        self.listbox.grid(row=10, column=0, columnspan=2)
        
    def add_application(self):
        company = self.company_entry.get()
        position = self.position_entry.get()
        date = self.date_entry.get()
        status = self.status_entry.get()
        notes = self.notes_entry.get()
        
        if company and position and date and status:
            self.tracker.add_application(company, position, date, status, notes)
            self.update_listbox()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")
        
    def delete_application(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.tracker.delete_application(selected_index[0])
            self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select an application to delete.")
    
    def search_application(self):
        keyword = simpledialog.askstring("Search", "Enter company or position:")
        if keyword:
            results = self.tracker.search_application(keyword)
            self.listbox.delete(0, tk.END)
            for result in results:
                self.listbox.insert(tk.END, result)
    
    def save_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            messagebox.showinfo("Save File", self.tracker.save_to_file(filename))
    
    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filename:
            messagebox.showinfo("Load File", self.tracker.load_from_file(filename))
            self.update_listbox()
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for app in self.tracker.list_applications():
            self.listbox.insert(tk.END, app)

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationGUI(root)
    root.mainloop()
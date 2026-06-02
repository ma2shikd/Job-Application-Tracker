import json
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class JobApplication:
    def __init__(self, company, position, application_date, status, notes=""):
        self.company = company.strip()
        self.position = position.strip()
        self.application_date = application_date.strip()
        self.status = status.strip()
        self.notes = notes.strip()

    def __str__(self):
        details = f"{self.company} - {self.position} (Applied: {self.application_date}, Status: {self.status})"
        return f"{details} Notes: {self.notes}" if self.notes else details

class JobApplicationTracker:
    def __init__(self):
        self.applications = []

    def add_application(self, company, position, application_date, status, notes):
        new_application = JobApplication(company, position, application_date, status, notes)
        self.applications.append(new_application)
        return f'Added application for "{position}" at {company}.'

    def list_applications(self):
        return [str(app) for app in self.applications]

    def get_application_rows(self, keyword=None):
        rows = []
        normalized_keyword = keyword.lower().strip() if keyword else ""
        for index, app in enumerate(self.applications):
            if (
                not normalized_keyword
                or normalized_keyword in app.company.lower()
                or normalized_keyword in app.position.lower()
                or normalized_keyword in app.status.lower()
                or normalized_keyword in app.notes.lower()
            ):
                rows.append((index, str(app)))
        return rows

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
        matches = [row for _, row in self.get_application_rows(keyword)]
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
            if not isinstance(data, list):
                return "Error loading file: Expected a list of applications."

            loaded_applications = []
            for entry in data:
                if not isinstance(entry, dict):
                    return "Error loading file: Each application must be an object."
                required_fields = {"company", "position", "application_date", "status"}
                if not required_fields.issubset(entry):
                    return "Error loading file: One or more applications are missing required fields."
                loaded_applications.append(
                    JobApplication(
                        entry["company"],
                        entry["position"],
                        entry["application_date"],
                        entry["status"],
                        entry.get("notes", ""),
                    )
                )

            self.applications = loaded_applications
            return f'Loaded applications from "{filename}".'
        except FileNotFoundError:
            return f'File "{filename}" not found.'
        except json.JSONDecodeError:
            return f'Error loading file: "{filename}" is not valid JSON.'
        except Exception as e:
            return f"Error loading file: {e}"

class JobApplicationGUI:
    def __init__(self, root):
        self.tracker = JobApplicationTracker()
        self.displayed_indexes = []
        self.current_filter = None
        self.root = root
        self.root.title("Job Application Tracker")
        self.root.columnconfigure(1, weight=1)
        
        # Entry Fields
        tk.Label(root, text="Company:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.company_entry = tk.Entry(root, width=40)
        self.company_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=4)
        
        tk.Label(root, text="Position:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.position_entry = tk.Entry(root, width=40)
        self.position_entry.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
        
        tk.Label(root, text="Date Applied:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
        self.date_entry = tk.Entry(root, width=40)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=6, pady=4)
        
        tk.Label(root, text="Status:").grid(row=3, column=0, sticky="w", padx=6, pady=4)
        self.status_entry = tk.Entry(root, width=40)
        self.status_entry.grid(row=3, column=1, sticky="ew", padx=6, pady=4)
        
        tk.Label(root, text="Notes:").grid(row=4, column=0, sticky="w", padx=6, pady=4)
        self.notes_entry = tk.Entry(root, width=40)
        self.notes_entry.grid(row=4, column=1, sticky="ew", padx=6, pady=4)
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=6, pady=6)
        tk.Button(button_frame, text="Add Application", command=self.add_application).pack(side=tk.LEFT, padx=(0, 4))
        tk.Button(button_frame, text="Delete Selected", command=self.delete_application).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Search", command=self.search_application).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Show All", command=self.show_all_applications).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Save", command=self.save_to_file).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Load", command=self.load_from_file).pack(side=tk.LEFT, padx=4)
        
        # Listbox
        self.listbox = tk.Listbox(root, width=80, height=10)
        self.listbox.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
        self.root.rowconfigure(6, weight=1)
        
    def add_application(self):
        company = self.company_entry.get().strip()
        position = self.position_entry.get().strip()
        date = self.date_entry.get().strip()
        status = self.status_entry.get().strip()
        notes = self.notes_entry.get().strip()
        
        if company and position and date and status:
            self.tracker.add_application(company, position, date, status, notes)
            self.clear_entries()
            self.current_filter = None
            self.update_listbox()
        else:
            messagebox.showwarning("Input Error", "Please fill company, position, date applied, and status.")
        
    def delete_application(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            if selected_index[0] >= len(self.displayed_indexes):
                messagebox.showwarning("Selection Error", "Please select an application to delete.")
                return
            application_index = self.displayed_indexes[selected_index[0]]
            result = self.tracker.delete_application(application_index)
            self.update_listbox()
            messagebox.showinfo("Delete Application", result)
        else:
            messagebox.showwarning("Selection Error", "Please select an application to delete.")
    
    def search_application(self):
        keyword = simpledialog.askstring("Search", "Enter company or position:")
        if keyword and keyword.strip():
            self.current_filter = keyword.strip()
            self.update_listbox()
            if not self.displayed_indexes:
                self.listbox.insert(tk.END, f'No applications found for "{self.current_filter}".')
    
    def save_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            messagebox.showinfo("Save File", self.tracker.save_to_file(filename))
    
    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filename:
            result = self.tracker.load_from_file(filename)
            messagebox.showinfo("Load File", result)
            if result.startswith("Loaded"):
                self.current_filter = None
                self.update_listbox()

    def show_all_applications(self):
        self.current_filter = None
        self.update_listbox()

    def clear_entries(self):
        for entry in (
            self.company_entry,
            self.position_entry,
            self.date_entry,
            self.status_entry,
            self.notes_entry,
        ):
            entry.delete(0, tk.END)
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        rows = self.tracker.get_application_rows(self.current_filter)
        self.displayed_indexes = [index for index, _ in rows]
        for _, app in rows:
            self.listbox.insert(tk.END, app)

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationGUI(root)
    root.mainloop()

<<<<<<< HEAD
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from update_jsons import run_update, run_revert, scan_all_paths

class JSONUpdaterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 JSON Updater Tool")

        # -------------------------------
        # Variables
        # -------------------------------
        self.json_dir = None              # JSON directory
        self.update_file = None           # Update file
        self.available_paths = []         # All JSON paths (for Mode 2 dropdown)
        self.mode_var = tk.IntVar(value=1)  # 1=Mode1, 2=Mode2, 3=Mode3

        # -------------------------------
        # Title
        # -------------------------------
        tk.Label(root, text="🔧 JSON Updater Tool", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        # -------------------------------
        # Directory & file selection
        # -------------------------------
        tk.Button(root, text="📂 Select JSON Directory", command=self.select_json_dir).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="📄 Select Update JSON File", command=self.select_update_file).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Mode selection
        # -------------------------------
        tk.Radiobutton(root, text="➕ Mode 1: Add top-level object", variable=self.mode_var, value=1, command=self.on_mode_change).grid(row=3, column=0, sticky="w", padx=5)
        tk.Radiobutton(root, text="🧩 Mode 2: Add inside existing object/array", variable=self.mode_var, value=2, command=self.on_mode_change).grid(row=4, column=0, sticky="w", padx=5)
        tk.Radiobutton(root, text="🎯 Mode 3: Update string(s) in specific file(s)", variable=self.mode_var, value=3, command=self.on_mode_change).grid(row=5, column=0, sticky="w", padx=5)

        # -------------------------------
        # Mode 2 input: target path (dot notation)
        # -------------------------------
        tk.Label(root, text="Target Path (dot notation):").grid(row=6, column=0, sticky="w", padx=5)
        self.target_entry = ttk.Combobox(root)
        self.target_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        self.target_entry.bind("<KeyRelease>", self.refresh_mode2_dropdown)

        # -------------------------------
        # Mode 3 inputs
        # -------------------------------
        tk.Label(root, text="Mode 3: File name filter").grid(row=8, column=0, sticky="w", padx=5)
        self.filename_entry = tk.Entry(root)
        self.filename_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew")

        tk.Label(root, text="Mode 3: Target Path (dot notation to string)").grid(row=10, column=0, sticky="w", padx=5)
        self.mode3_target_entry = tk.Entry(root)
        self.mode3_target_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Action buttons
        # -------------------------------
        tk.Button(root, text="▶️ Run Update", bg="#dff0d8", command=self.run_update_gui).grid(row=12, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="↩️ Revert", bg="#f2dede", command=self.run_revert_gui).grid(row=13, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="❓ Help", command=self.show_help).grid(row=14, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Log window
        # -------------------------------
        log_frame = tk.Frame(root)
        log_frame.grid(row=1, column=1, rowspan=14, padx=10, pady=5, sticky="nsew")
        self.log = tk.Text(log_frame, wrap="none", height=20, width=80, bg="black", fg="white")
        self.log.grid(row=0, column=0, sticky="nsew")
        yscroll = tk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll = tk.Scrollbar(log_frame, orient="horizontal", command=self.log.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.log.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # -------------------------------
        # Tag colors for log
        # -------------------------------
        self.log.tag_config("success", foreground="lightgreen")   # updated
        self.log.tag_config("notfound", foreground="orange")      # skipped-not-found
        self.log.tag_config("exists", foreground="lightblue")     # skipped-exists
        self.log.tag_config("total", foreground="grey")           # total scanned
        self.log.tag_config("info", foreground="cyan")            # general info

        # -------------------------------
        # Expand behavior
        # -------------------------------
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(14, weight=1)

        self.on_mode_change()

    def select_json_dir(self):
        self.json_dir = filedialog.askdirectory()
        if self.json_dir:
            self.log_message(f"📂 Directory selected: {self.json_dir}\n", "info")
            self.available_paths = scan_all_paths(self.json_dir)
            self.target_entry["values"] = self.available_paths

    def select_update_file(self):
        self.update_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if self.update_file:
            self.log_message(f"📄 Update file selected: {self.update_file}\n", "info")

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == 1:
            self.target_entry.config(state="disabled")
            self.filename_entry.config(state="disabled")
            self.mode3_target_entry.config(state="disabled")
        elif mode == 2:
            self.target_entry.config(state="normal")
            self.filename_entry.config(state="disabled")
            self.mode3_target_entry.config(state="disabled")
        elif mode == 3:
            self.target_entry.config(state="disabled")
            self.filename_entry.config(state="normal")
            self.mode3_target_entry.config(state="normal")

    def refresh_mode2_dropdown(self, event=None):
        current = self.target_entry.get().strip()
        values = set()

        if not current:
            for path in self.available_paths:
                if "." not in path:
                    values.add(path)
        else:
            for path in self.available_paths:
                if current.endswith("."):
                    prefix = current[:-1]
                    if path.startswith(prefix + ".") and path.count(".") == current.count("."):
                        values.add(path)
                else:
                    if path.startswith(current) and path.count(".") == current.count("."):
                        values.add(path)

        self.target_entry["values"] = sorted(values)

    def run_update_gui(self):
        if not self.json_dir or not self.update_file:
            messagebox.showerror("Error", "Please select JSON directory and update file first.")
            return

        mode = self.mode_var.get()
        target_path = None
        filename_filter = None

        if mode == 2:
            target_path = self.target_entry.get().strip()
            if not target_path:
                messagebox.showerror("Error", "Please enter/select a target path for Mode 2.")
                return
        if mode == 3:
            filename_filter = self.filename_entry.get().strip()
            target_path = self.mode3_target_entry.get().strip()
            if not filename_filter or not target_path:
                messagebox.showerror("Error", "Please enter filename and target path for Mode 3.")
                return
            self.log_message(f"🔎 Scanning for files named '{filename_filter}'...\n", "info")

        results = run_update(self.json_dir, self.update_file, mode, target_path, filename_filter)
        self.display_results(results)

    def run_revert_gui(self):
        backup_dir = filedialog.askdirectory(title="Select Backup Directory (older version)")
        if not backup_dir:
            return
        target_dir = filedialog.askdirectory(title="Select Target Directory (current version)")
        if not target_dir:
            return

        results = run_revert(backup_dir, target_dir)
        self.display_results(results)

    def display_results(self, results):
        self.log.insert("end", "\n=== Update Results ===\n", "info")
        self.log.insert("end", f"📊 Total files scanned: {results['scanned']}\n", "total")

        # Successful
        self.log.insert("end", f"\n✅ Successful ({len(results['updated'])}):\n", "success")
        for f in results["updated"]:
            self.log.insert("end", f"   {f}\n", "success")

        # Not found
        self.log.insert("end", f"\n⚠ Not affected - no target object found ({len(results['skipped_not_found'])}):\n", "notfound")
        if results["skipped_not_found"]:
            for f in results["skipped_not_found"]:
                self.log.insert("end", f"   {f}\n", "notfound")
        else:
            self.log.insert("end", "   (none)\n", "notfound")

        # Already exists / same value
        self.log.insert("end", f"\nℹ Not affected - already updated / same value ({len(results['skipped_exists'])}):\n", "exists")
        if results["skipped_exists"]:
            for f in results["skipped_exists"]:
                self.log.insert("end", f"   {f}\n", "exists")
        else:
            self.log.insert("end", "   (none)\n", "exists")

        self.log.insert("end", "\n=======================\n", "info")
        self.log.see("end")

    def log_message(self, msg, tag="info"):
        self.log.insert("end", msg, tag)
        self.log.see("end")

    def show_help(self):
        help_text = (
            "📘 JSON Updater Tool Manual\n\n"
            "MAIN FEATURE (Update Modes):\n"
            "1️⃣ Mode 1: Add new object(s) at the root level.\n"
            "   - Example: Add { \"newKey\": \"value\" } to all files.\n\n"
            "2️⃣ Mode 2: Add inside an existing object/array.\n"
            "   - Enter target path in dot notation.\n"
            "   - Example: errors.messages → inserts into messages inside errors.\n\n"
            "3️⃣ Mode 3: Update strings inside files with the same name.\n"
            "   - Enter filename (e.g., it-IT.json).\n"
            "   - Enter target path (e.g., errors.messages).\n"
            "   - Example: updates 'messages' string value inside 'errors' object.\n\n"
            "↩️ REVERT FEATURE:\n"
            "   - Select backup directory (older version).\n"
            "   - Select target directory (current version).\n"
            "   - Tool restores all JSON files from backup.\n"
        )
        messagebox.showinfo("Manual / Help", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONUpdaterGUI(root)
    root.mainloop()
=======
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from update_jsons import run_update, run_revert, scan_all_paths

class JSONUpdaterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 JSON Updater Tool")

        # -------------------------------
        # Variables
        # -------------------------------
        self.json_dir = None              # JSON directory
        self.update_file = None           # Update file
        self.available_paths = []         # All JSON paths (for Mode 2 dropdown)
        self.mode_var = tk.IntVar(value=1)  # 1=Mode1, 2=Mode2, 3=Mode3

        # -------------------------------
        # Title
        # -------------------------------
        tk.Label(root, text="🔧 JSON Updater Tool", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        # -------------------------------
        # Directory & file selection
        # -------------------------------
        tk.Button(root, text="📂 Select JSON Directory", command=self.select_json_dir).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="📄 Select Update JSON File", command=self.select_update_file).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Mode selection
        # -------------------------------
        tk.Radiobutton(root, text="➕ Mode 1: Add top-level object", variable=self.mode_var, value=1, command=self.on_mode_change).grid(row=3, column=0, sticky="w", padx=5)
        tk.Radiobutton(root, text="🧩 Mode 2: Add inside existing object/array", variable=self.mode_var, value=2, command=self.on_mode_change).grid(row=4, column=0, sticky="w", padx=5)
        tk.Radiobutton(root, text="🎯 Mode 3: Update string(s) in specific file(s)", variable=self.mode_var, value=3, command=self.on_mode_change).grid(row=5, column=0, sticky="w", padx=5)

        # -------------------------------
        # Mode 2 input: target path (dot notation)
        # -------------------------------
        tk.Label(root, text="Target Path (dot notation):").grid(row=6, column=0, sticky="w", padx=5)
        self.target_entry = ttk.Combobox(root)
        self.target_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        self.target_entry.bind("<KeyRelease>", self.refresh_mode2_dropdown)

        # -------------------------------
        # Mode 3 inputs
        # -------------------------------
        tk.Label(root, text="Mode 3: File name filter").grid(row=8, column=0, sticky="w", padx=5)
        self.filename_entry = tk.Entry(root)
        self.filename_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew")

        tk.Label(root, text="Mode 3: Target Path (dot notation to string)").grid(row=10, column=0, sticky="w", padx=5)
        self.mode3_target_entry = tk.Entry(root)
        self.mode3_target_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Action buttons
        # -------------------------------
        tk.Button(root, text="▶️ Run Update", bg="#dff0d8", command=self.run_update_gui).grid(row=12, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="↩️ Revert", bg="#f2dede", command=self.run_revert_gui).grid(row=13, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="❓ Help", command=self.show_help).grid(row=14, column=0, padx=5, pady=5, sticky="ew")

        # -------------------------------
        # Log window
        # -------------------------------
        log_frame = tk.Frame(root)
        log_frame.grid(row=1, column=1, rowspan=14, padx=10, pady=5, sticky="nsew")
        self.log = tk.Text(log_frame, wrap="none", height=20, width=80, bg="black", fg="white")
        self.log.grid(row=0, column=0, sticky="nsew")
        yscroll = tk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll = tk.Scrollbar(log_frame, orient="horizontal", command=self.log.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.log.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # -------------------------------
        # Tag colors for log
        # -------------------------------
        self.log.tag_config("success", foreground="lightgreen")   # updated
        self.log.tag_config("notfound", foreground="orange")      # skipped-not-found
        self.log.tag_config("exists", foreground="lightblue")     # skipped-exists
        self.log.tag_config("total", foreground="grey")           # total scanned
        self.log.tag_config("info", foreground="cyan")            # general info

        # -------------------------------
        # Expand behavior
        # -------------------------------
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(14, weight=1)

        self.on_mode_change()

    def select_json_dir(self):
        self.json_dir = filedialog.askdirectory()
        if self.json_dir:
            self.log_message(f"📂 Directory selected: {self.json_dir}\n", "info")
            self.available_paths = scan_all_paths(self.json_dir)
            self.target_entry["values"] = self.available_paths

    def select_update_file(self):
        self.update_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if self.update_file:
            self.log_message(f"📄 Update file selected: {self.update_file}\n", "info")

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == 1:
            self.target_entry.config(state="disabled")
            self.filename_entry.config(state="disabled")
            self.mode3_target_entry.config(state="disabled")
        elif mode == 2:
            self.target_entry.config(state="normal")
            self.filename_entry.config(state="disabled")
            self.mode3_target_entry.config(state="disabled")
        elif mode == 3:
            self.target_entry.config(state="disabled")
            self.filename_entry.config(state="normal")
            self.mode3_target_entry.config(state="normal")

    def refresh_mode2_dropdown(self, event=None):
        current = self.target_entry.get().strip()
        values = set()

        if not current:
            for path in self.available_paths:
                if "." not in path:
                    values.add(path)
        else:
            for path in self.available_paths:
                if current.endswith("."):
                    prefix = current[:-1]
                    if path.startswith(prefix + ".") and path.count(".") == current.count("."):
                        values.add(path)
                else:
                    if path.startswith(current) and path.count(".") == current.count("."):
                        values.add(path)

        self.target_entry["values"] = sorted(values)

    def run_update_gui(self):
        if not self.json_dir or not self.update_file:
            messagebox.showerror("Error", "Please select JSON directory and update file first.")
            return

        mode = self.mode_var.get()
        target_path = None
        filename_filter = None

        if mode == 2:
            target_path = self.target_entry.get().strip()
            if not target_path:
                messagebox.showerror("Error", "Please enter/select a target path for Mode 2.")
                return
        if mode == 3:
            filename_filter = self.filename_entry.get().strip()
            target_path = self.mode3_target_entry.get().strip()
            if not filename_filter or not target_path:
                messagebox.showerror("Error", "Please enter filename and target path for Mode 3.")
                return
            self.log_message(f"🔎 Scanning for files named '{filename_filter}'...\n", "info")

        results = run_update(self.json_dir, self.update_file, mode, target_path, filename_filter)
        self.display_results(results)

    def run_revert_gui(self):
        backup_dir = filedialog.askdirectory(title="Select Backup Directory (older version)")
        if not backup_dir:
            return
        target_dir = filedialog.askdirectory(title="Select Target Directory (current version)")
        if not target_dir:
            return

        results = run_revert(backup_dir, target_dir)
        self.display_results(results)

    def display_results(self, results):
        self.log.insert("end", "\n=== Update Results ===\n", "info")
        self.log.insert("end", f"📊 Total files scanned: {results['scanned']}\n", "total")

        # Successful
        self.log.insert("end", f"\n✅ Successful ({len(results['updated'])}):\n", "success")
        for f in results["updated"]:
            self.log.insert("end", f"   {f}\n", "success")

        # Not found
        self.log.insert("end", f"\n⚠ Not affected - no target object found ({len(results['skipped_not_found'])}):\n", "notfound")
        if results["skipped_not_found"]:
            for f in results["skipped_not_found"]:
                self.log.insert("end", f"   {f}\n", "notfound")
        else:
            self.log.insert("end", "   (none)\n", "notfound")

        # Already exists / same value
        self.log.insert("end", f"\nℹ Not affected - already updated / same value ({len(results['skipped_exists'])}):\n", "exists")
        if results["skipped_exists"]:
            for f in results["skipped_exists"]:
                self.log.insert("end", f"   {f}\n", "exists")
        else:
            self.log.insert("end", "   (none)\n", "exists")

        self.log.insert("end", "\n=======================\n", "info")
        self.log.see("end")

    def log_message(self, msg, tag="info"):
        self.log.insert("end", msg, tag)
        self.log.see("end")

    def show_help(self):
        help_text = (
            "📘 JSON Updater Tool Manual\n\n"
            "MAIN FEATURE (Update Modes):\n"
            "1️⃣ Mode 1: Add new object(s) at the root level.\n"
            "   - Example: Add { \"newKey\": \"value\" } to all files.\n\n"
            "2️⃣ Mode 2: Add inside an existing object/array.\n"
            "   - Enter target path in dot notation.\n"
            "   - Example: errors.messages → inserts into messages inside errors.\n\n"
            "3️⃣ Mode 3: Update strings inside files with the same name.\n"
            "   - Enter filename (e.g., it-IT.json).\n"
            "   - Enter target path (e.g., errors.messages).\n"
            "   - Example: updates 'messages' string value inside 'errors' object.\n\n"
            "↩️ REVERT FEATURE:\n"
            "   - Select backup directory (older version).\n"
            "   - Select target directory (current version).\n"
            "   - Tool restores all JSON files from backup.\n"
        )
        messagebox.showinfo("Manual / Help", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONUpdaterGUI(root)
    root.mainloop()
>>>>>>> 927c3f2b0c37f192b42dd04cffcd4272d7c6db27

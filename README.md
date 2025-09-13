# json-updater-tool
Tool to modify JSON files


# 🔧 JSON Updater Tool

A **Tkinter-based GUI tool** to bulk update JSON files with multiple modes, including top-level object insertion, nested updates, and file-specific string updates. Also includes a revert option to restore backups.  

---

## Features

### **Modes of Update**
1. **Mode 1: Add Top-Level Object**  
   Add new key(s) at the root of all JSON files.

2. **Mode 2: Add Nested Content (One-Level Deep)**  
   Add content into an existing object or array.  
   - Dynamic autocomplete dropdown for immediate children only.  
   - Type freely while seeing suggestions.

3. **Mode 3: Update String Values in Specific File(s)**  
   Update string fields inside a JSON file with the same name.  
   - Useful for translations or standardizing messages.

### **Revert Feature**
- Restore JSON files from a backup directory.  
- Select backup and target directories via GUI.  

### **Logging**
- Shows absolute paths of:  
  - Successfully updated files ✅  
  - Skipped files due to missing target ⚠️  
  - Skipped files due to already existing values ℹ️  

---

## Screenshot in the folder displayed

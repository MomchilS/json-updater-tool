# json-updater-tool
Tool to modify JSON files


# 🔧 JSON Updater Tool

A **Tkinter-based GUI tool** to bulk update JSON files with multiple modes, including top-level object insertion, nested updates, and file-specific string updates. Also includes a revert option to restore backups.  

---
First select target directory full of json files or subfolders full of json files
Second select a json file full with new content (objects, arrays, strings) which we feed or modify depending on the mode used

## Features

### **Modes of Update**
1. **Mode 1: Add Top-Level Object**  
   Add new key(s) at the root of all JSON files.

2. **Mode 2: Add Nested Content (One-Level Deep)**  
   Add content into an existing object or array.
   - Scans all files in target directory
   - Automatically recognizes all repeating root level objects
   - Typing a root level object will add content in all scanned objects inside target directory with the target content
   - Typing a root level object and adding "." to it opens all nested objects and arrays inside it (If needed updating) 
   - Dynamic autocomplete dropdown for immediate children only.  
   - Type freely while seeing suggestions.

4. **Mode 3: Update String Values in Specific File(s)**  
   Update string fields inside a JSON file with the same name.  
   - First search bar type name of target repeating JSON files located in different subfolders in the target directory.
   - Scans all files with the target name
   - Second search bar has same functionalities as mode 2
   - Typing a root level object will add content in all scanned objects inside target directory with the target content
   - Typing a root level object and adding "." to it opens all nested objects and arrays inside it (If needed updating) 

### **Revert Feature**
- Restore JSON files from a backup directory.  
- Select backup and target directories via GUI.  

### **Logging**
- Shows number of files and absolute paths of:  
  - Successfully updated files ✅  
  - Skipped files due to missing target ⚠️  
  - Skipped files due to already existing values ℹ️  

---

## Screenshot attached above

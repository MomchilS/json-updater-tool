# json-updater-tool
Tool to modify JSON files


# 🔧 JSON Updater Tool

A **Tkinter-based GUI tool** to bulk update JSON files with multiple modes, including top-level object insertion, nested updates, and file-specific string updates. Also includes a revert option to restore backups.  

---

- Initial steps:
 - Choose a target directory full with json files or subfolders full with json files.
 - Choose a json file which has the new content to use for upgrading or replacing, depending on the mode.

## Features

### **Modes of Update**
1. **Mode 1: Add Top-Level Object**  
   Add new key(s) at the root of all JSON files.

2. **Mode 2: Add Nested Content (One-Level Deep)**  
   Add content into an existing object or array.  
   - In the search bar type in the root level object that needs to be updated
   - If a nested object or array inside the root object needs to be updated add "." to go 1 level deep.
   - Dynamic autocomplete dropdown for immediate children only.  
   - Type freely while seeing suggestions.

3. **Mode 3: Update String Values in Specific File(s)**  
   Update string fields inside a JSON file with the same name.  
   - Useful for json files with same names in different subfolder in the target directory.
   - In the first text bar, type the name of the json files with repeating names.
   - In the second text bar, type in the root level object then "." to select the nested string.
   - This will replace the value of the target string with the new content slected from before.

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
>>>>>>> 927c3f2b0c37f192b42dd04cffcd4272d7c6db27

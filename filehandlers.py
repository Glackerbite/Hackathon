import os
import pathlib as Path
import shutil


def getData(filedir: str, dataTypes: list = None, dataType: str = ""):
    """Read a simple key:comma,separated,value file and return parsed values.

    - Returns a dict of key -> list-of-values when no filters given.
    - If dataType is provided, returns list for that key (or empty list).
    - If dataTypes (list) is provided, returns a filtered dict containing only those keys.

    Notes: keys and values are stripped of surrounding whitespace. Empty values produce an empty list.
    """
    data = {}

    with open(filedir, 'r') as f:
        for line in f:
            if ':' not in line:
                continue

            key, rest = line.split(':', 1)
            key = key.strip()
            value = rest.strip()

            # convert comma-separated values into list; empty value -> empty list
            if value == "":
                items = []
            else:
                items = [item.strip() for item in value.split(',') if item.strip()]

            # save to dictionary
            data[key] = items

    # --- return behavior ---
    if dataType:  # single key requested
        try:
            return data.get(dataType, [])
        except KeyError:
            raise KeyError(f"No line found for dataType '{dataType}' in {filedir}")
    elif dataTypes:  # specific list of keys requested
        try:
            return {k: v for k, v in data.items() if k in dataTypes}
        except KeyError:
            raise KeyError(f"No line found for one of the dataTypes {dataTypes}")
    else:  # no filter: return everything
        return data
    
def writeData(filedir: str, dataType: str, data: str = "", add: bool = False, remove: bool = False):
    """Update a line in the data file for a given dataType.

    - If add=True: append comma-separated tokens from `data` to the existing list (no duplicates).
    - If remove=True: remove comma-separated tokens from existing list.
    - Otherwise, replace the list for the key with `data` (comma-separated string).

    Raises KeyError if the key is not present in the file.
    """
    filelines = []
    changed = False

    with open(filedir, "r") as file:
        for line in file:
            # split the first ':' to separate key and value
            if ':' in line:
                key, rest = line.split(':', 1)
                key_stripped = key.strip()
                if key_stripped == dataType:
                    changed = True
                    # get current items as list
                    current_items = getData(filedir=filedir, dataType=dataType)

                    if add:
                        to_add = [d.strip() for d in data.split(',') if d.strip()]
                        # avoid duplicates while preserving order
                        for tok in to_add:
                            if tok not in current_items:
                                current_items.append(tok)
                        if current_items:
                            line = f"{dataType}:{','.join(current_items)}\n"
                        else:
                            line = f"{dataType}:\n"
                    elif remove:
                        to_remove = [d.strip() for d in data.split(',') if d.strip()]
                        current_items = [i for i in current_items if i not in to_remove]
                        if current_items:
                            line = f"{dataType}:{','.join(current_items)}\n"
                        else:
                            line = f"{dataType}:\n"
                    else:
                        # direct replace (normalize whitespace and split/strip)
                        new_items = [d.strip() for d in data.split(',') if d.strip()]
                        if new_items:
                            line = f"{dataType}:{','.join(new_items)}\n"
                        else:
                            line = f"{dataType}:\n"
            filelines.append(line)

    if not changed:
        raise KeyError(f"No line found for dataType '{dataType}' in {filedir}")

    with open(filedir, "w") as file:
        file.writelines(filelines)
def delete(deldir: str,fileType: str):

    if fileType == "folder":
        try:
            shutil.rmtree(deldir)
        except FileNotFoundError:
            raise FileNotFoundError(f"{deldir} Folder was not found")
        except Exception as e:
            raise Exception(f'Error in delete function:\n {e} ')
        
    elif fileType == "file":
        try:
            os.remove(f'{deldir}')
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {deldir} doesnt exist.")
        except Exception as e:
            raise Exception(f'Error in delete function:\n {e} ')
    else:
        raise SyntaxError("ERROR in delete function: fileType syntax error.")

def createFile(filedir: str,params: dict):
    try:
        with open(filedir, 'w') as f:
            for key, value in params.items():
                value = ','.join(value) if isinstance(value, list) else value
                key, value = key.strip(), value.strip()
                f.write(f"{key}:{value}\n")
            
    except FileExistsError:
        raise FileExistsError(f"Create File Error:\n File '{filedir}' already exists.")
    except Exception as e:
        raise Exception(f"Create File Error:\nError creating file '{filedir}': {e}")
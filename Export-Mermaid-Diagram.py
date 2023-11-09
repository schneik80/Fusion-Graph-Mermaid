# Author - Kevin S
# Description - Export an assembly as a mermaid graph

import os, subprocess
import adsk.core, adsk.fusion
import traceback

# Performs a recursive traversal of an entire assembly structure.


def traverseAssembly(parent, occurrences, currentLevel, inputString):
    for i in range(0, occurrences.count):
        occ = occurrences.item(i)

        foo2 = occ.name
        foo2 = foo2.replace("-", "_")
        foo2 = foo2.replace('"', "")

        parent = parent.replace("-", "_")

        foo = parent + " --> " + foo2 + "\n"
        foo = foo.replace(" ", "")
        foo = foo.replace("(", "")
        foo = foo.replace(")", "")
        foo = foo.replace('"', "")

        inputString += foo

        if occ.childOccurrences:
            inputString = traverseAssembly(
                occ.name, occ.childOccurrences, currentLevel + 1, inputString
            )
    return inputString


# Returns a string containing the specified number of spaces.
def spaces(spaceCount):
    result = ""
    for i in range(0, spaceCount):
        result += " "

    return result


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox("No active Fusion design", "No Design")
            return

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create the title for the output.
        parentOcc = design.parentDocument.name
        resultString = "graph LR" + "\n"
        # resultString += parentOcc + '\n'

        # Call the recursive function to traverse the assembly and build the output string.
        resultString = traverseAssembly(
            parentOcc, rootComp.occurrences.asList, 1, resultString
        )

        msg = ""
        # Set styles of file dialog.
        folderDlg = ui.createFolderDialog()
        folderDlg.title = "Choose Folder to save Mermai Graph"

        # Show file save dialog
        dlgResult = folderDlg.showDialog()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            filepath = os.path.join(folderDlg.folder, parentOcc + ".mmd")
            #imagepath = os.path.join(folderDlg.folder, parentOcc + ".png")  # path needed for image export

            # Write the results to the file
            with open(filepath, "w") as f:
                f.write(resultString)

            # Unable to get calling mmdc from command line
            # #command = f'/usr/local/bin/mmdc -i "{filepath}" -o "{imagepath}"'
            # print(command)
            # subprocess.run(
            #     [command],
            #     shell=True,
            #     capture_output=True
            #     )

            ui.messageBox("Graph and PNG Image saved at: " + filepath, "Graph Saved", 0, 2 )

        else:
            return

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


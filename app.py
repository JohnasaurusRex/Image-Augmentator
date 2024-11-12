import Augmentor
import PySimpleGUI as sg
import os


# Function to open the output folder
def open_output_folder(input_folder):
    output_folder = os.path.join(input_folder, 'output')
    os.startfile(output_folder)  # Opens the output folder using the default file explorer


# Define the layout of the app
layout = [
    [sg.Text("Image Augmentation App")],
    [sg.Text("Enter the path to the images folder:")],
    [sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
    [sg.Text("Enter the probability for crop_random:")],
    [sg.Slider(range=(0, 1), resolution=0.01, default_value=0.5, key="-CROP-", orientation="h")],
    [sg.Text("Enter the probability for rotate_random_90:")],
    [sg.Slider(range=(0, 1), resolution=0.01, default_value=0.3, key="-ROTATE-", orientation="h")],
    [sg.Text("Enter the probability for flip_random:")],
    [sg.Slider(range=(0, 1), resolution=0.01, default_value=0.5, key="-FLIP-", orientation="h")],
    [sg.Text("Enter the number of samples to generate:")],
    [sg.Input(key="-SAMPLES-")],
    [sg.Button("Run"), sg.Button("Exit")]
]

# Create the window object
window = sg.Window("Image Augmentation App", layout)

# Create a loop to handle the user events
while True:
    event, values = window.read()
    # If the user clicks the Exit button or closes the window, exit the loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # If the user clicks the Run button, run the augmentation pipeline
    elif event == "Run":
        # Get the user input values
        folder = values["-FOLDER-"]
        crop_prob = values["-CROP-"]
        rotate_prob = values["-ROTATE-"]
        flip_prob = values["-FLIP-"]
        samples = int(values["-SAMPLES-"])

        # Create the output folder inside the input folder
        output_folder = os.path.join(folder, 'output')
        os.makedirs(output_folder, exist_ok=True)

        # Create the augmentation pipeline
        p = Augmentor.Pipeline(folder, output_directory=output_folder)
        p.crop_random(probability=crop_prob, percentage_area=0.8)
        p.resize(probability=1, width=400, height=400)
        p.rotate_random_90(probability=rotate_prob)
        p.flip_random(probability=flip_prob)
        # Generate the augmented images
        p.sample(samples)
        # Show a message box to indicate the completion
        popup_layout = [
            [sg.Text("Done", font=("Helvetica", 18))],
            [sg.Text(f"{samples} augmented images have been generated.")],
            [sg.Button("Open Output Folder")]
        ]
        popup_window = sg.Window("Augmentation Complete", popup_layout)
        while True:
            popup_event, popup_values = popup_window.read()
            if popup_event == sg.WIN_CLOSED or popup_event == "Open Output Folder":
                open_output_folder(folder)  # Redirect to the 'output' folder in the input folder
                break
        popup_window.close()

# Close the main window
window.close()
import os
import pyautogui
import time

def get_first_21_files(directory):
    """Get the first 21 files in the specified directory."""
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files[:21]

def drag_and_drop_files(file_icon_position, drop_position, num_files):
    """Drag and drop a specified number of files."""
    for _ in range(num_files):
        # Move to the file's icon position and click to select
        pyautogui.moveTo(file_icon_position[0], file_icon_position[1], duration=1)
        pyautogui.click()

        # Drag to the drop position in the browser
        pyautogui.dragTo(drop_position[0], drop_position[1], duration=2)

        # Add a delay for the next iteration
        time.sleep(2)

def main():
    file_icon_position = (56, 300)  # Replace with the coordinates of the file icons
    drop_position = (1000, 500)  # Replace with the drop position coordinates in the browser
    num_files_per_batch = 21

    # Repeat the process for the number of batches
    for _ in range(5):  # Adjust the range based on how many files/batches you have
        drag_and_drop_files(file_icon_position, drop_position, num_files_per_batch)
        time.sleep(10)  # Adjust the delay as needed

if __name__ == "__main__":
    main()
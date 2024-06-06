import os
from tkinter import Tk, filedialog, messagebox, Button, Label, Entry, Listbox, SINGLE, Frame
from tkinter import ttk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    video_path_entry.delete(0, 'end')
    video_path_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, 'end')
    output_folder_entry.insert(0, folder_path)

def split_video():
    video_path = video_path_entry.get()
    output_folder = output_folder_entry.get()
    clip_length = length_entry.get()

    if not video_path or not os.path.isfile(video_path):
        messagebox.showerror("Error", "Please select a valid video file.")
        return
    
    if not output_folder or not os.path.isdir(output_folder):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return

    try:
        clip_length = int(clip_length)
        if clip_length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid clip length in seconds.")
        return

    try:
        video = VideoFileClip(video_path)
        duration = int(video.duration)
        base_name = os.path.basename(video_path)
        name, ext = os.path.splitext(base_name)

        for start in range(0, duration, clip_length):
            end = min(start + clip_length, duration)
            output_path = os.path.join(output_folder, f"{name}_clip_{start//clip_length + 1}{ext}")
            ffmpeg_extract_subclip(video_path, start, end, targetname=output_path)
        
        messagebox.showinfo("Success", "Video successfully split.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def add_videos():
    files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    for file in files:
        if file not in video_files:
            video_files.append(file)
            video_listbox.insert('end', os.path.basename(file))

def remove_video():
    selected = video_listbox.curselection()
    if selected:
        video_files.pop(selected[0])
        video_listbox.delete(selected[0])

def move_up():
    selected = video_listbox.curselection()
    if selected and selected[0] > 0:
        index = selected[0]
        video_files[index], video_files[index - 1] = video_files[index - 1], video_files[index]
        video_listbox.delete(index)
        video_listbox.insert(index - 1, os.path.basename(video_files[index - 1]))
        video_listbox.select_set(index - 1)

def move_down():
    selected = video_listbox.curselection()
    if selected and selected[0] < len(video_files) - 1:
        index = selected[0]
        video_files[index], video_files[index + 1] = video_files[index + 1], video_files[index]
        video_listbox.delete(index)
        video_listbox.insert(index + 1, os.path.basename(video_files[index + 1]))
        video_listbox.select_set(index + 1)

def default_sort():
    video_files.sort()
    video_listbox.delete(0, 'end')
    for file in video_files:
        video_listbox.insert('end', os.path.basename(file))

def select_merge_output_folder():
    folder_path = filedialog.askdirectory()
    merge_output_folder_entry.delete(0, 'end')
    merge_output_folder_entry.insert(0, folder_path)

def merge_videos():
    if not video_files:
        messagebox.showerror("Error", "Please add at least two video files.")
        return

    output_folder = merge_output_folder_entry.get()
    if not output_folder or not os.path.isdir(output_folder):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return

    output_file = os.path.join(output_folder, "merged_video.mp4")

    try:
        clips = [VideoFileClip(file) for file in video_files]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_file, codec="libx264")
        messagebox.showinfo("Success", "Videos successfully merged.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

app = Tk()
app.title("Video Tool")

tab_control = ttk.Notebook(app)
tab_split = Frame(tab_control)
tab_merge = Frame(tab_control)
tab_control.add(tab_split, text="Split Video")
tab_control.add(tab_merge, text="Merge Videos")
tab_control.pack(expand=1, fill='both')

# Split Video Tab
Label(tab_split, text="Select Video File:").grid(row=0, column=0, padx=10, pady=10)
video_path_entry = Entry(tab_split, width=50)
video_path_entry.grid(row=0, column=1, padx=10, pady=10)
Button(tab_split, text="Browse", command=select_video_file).grid(row=0, column=2, padx=10, pady=10)

Label(tab_split, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=10)
output_folder_entry = Entry(tab_split, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
Button(tab_split, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

Label(tab_split, text="Clip Length (seconds):").grid(row=2, column=0, padx=10, pady=10)
length_entry = Entry(tab_split, width=50)
length_entry.grid(row=2, column=1, padx=10, pady=10)

Button(tab_split, text="Split Video", command=split_video).grid(row=3, column=0, columnspan=3, pady=20)

# Merge Videos Tab
video_files = []

Button(tab_merge, text="Add Videos", command=add_videos).grid(row=0, column=0, padx=10, pady=10)
Button(tab_merge, text="Remove Selected", command=remove_video).grid(row=0, column=1, padx=10, pady=10)
Button(tab_merge, text="Move Up", command=move_up).grid(row=0, column=2, padx=10, pady=10)
Button(tab_merge, text="Move Down", command=move_down).grid(row=0, column=3, padx=10, pady=10)
Button(tab_merge, text="Default Sort", command=default_sort).grid(row=0, column=4, padx=10, pady=10)

video_listbox = Listbox(tab_merge, selectmode=SINGLE, width=80)
video_listbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

Label(tab_merge, text="Select Output Folder:").grid(row=2, column=0, padx=10, pady=10)
merge_output_folder_entry = Entry(tab_merge, width=50)
merge_output_folder_entry.grid(row=2, column=1, padx=10, pady=10)
Button(tab_merge, text="Browse", command=select_merge_output_folder).grid(row=2, column=2, padx=10, pady=10)

Button(tab_merge, text="Merge Videos", command=merge_videos).grid(row=3, column=0, columnspan=5, pady=20)

app.mainloop()

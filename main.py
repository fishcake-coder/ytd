import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import subprocess
import os
import sys

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Set default download folder
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Downloader", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # URL Label and Entry
        url_label = ttk.Label(main_frame, text="YouTube URL:")
        url_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, pady=5)
        
        # Download folder label
        folder_label = ttk.Label(main_frame, text=f"Save to: {self.download_folder}")
        folder_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.folder_label = folder_label
        
        # Change folder button
        change_folder_btn = ttk.Button(main_frame, text="Change Folder", command=self.change_folder)
        change_folder_btn.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        # Download button
        download_btn = ttk.Button(main_frame, text="Download 720p MP4", command=self.download_video)
        download_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Open folder button
        self.open_folder_btn = ttk.Button(main_frame, text="Open Download Folder", command=self.open_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=7, column=0, columnspan=2, pady=10)
    
    def change_folder(self):
        folder = filedialog.askdirectory(title="Select Download Folder")
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=f"Save to: {self.download_folder}")
    
    def download_video(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not url.startswith(("http://", "https://")):
            messagebox.showerror("Error", "Please enter a valid URL starting with http:// or https://")
            return
        
        # Create download folder if it doesn't exist
        os.makedirs(self.download_folder, exist_ok=True)
        
        # Start download in separate thread
        thread = threading.Thread(target=self._download_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url):
        try:
            self.progress.start()
            self.status_label.config(text="Downloading...", foreground="blue")
            self.root.update()
            
            # yt-dlp command for 720p MP4
            command = [
                "yt-dlp",
                "-f", "best[height<=720]/best",
                "-o", os.path.join(self.download_folder, "%{title}s.%{ext}s"),
                url
            ]
            
            result = subprocess.run(command, capture_output=True, text=True)
            
            self.progress.stop()
            
            if result.returncode == 0:
                self.status_label.config(text="✓ Download completed successfully!", foreground="green")
                self.open_folder_btn.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Video downloaded successfully!")
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.status_label.config(text="✗ Download failed", foreground="red")
                messagebox.showerror("Error", f"Download failed:\n{error_msg}")
        
        except FileNotFoundError:
            self.progress.stop()
            self.status_label.config(text="✗ yt-dlp not found", foreground="red")
            messagebox.showerror("Error", "yt-dlp is not installed. Please run: pip install yt-dlp")
        
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="✗ Error occurred", foreground="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def open_folder(self):
        if os.path.exists(self.download_folder):
            if sys.platform == "win32":
                os.startfile(self.download_folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.download_folder])
            else:
                subprocess.Popen(["xdg-open", self.download_folder])

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
# My code is shit.
import os
import time
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
running = False

def create_gui():
    root = tk.Tk()
    root.title("影片修復器 GUI by AvianJay")
    root.geometry("500x550")
    
    #menubar = tk.Menu(root)

    def select_file():
        file_path = filedialog.askopenfilename(title="選擇要修復的影片", filetypes=[("影片檔", "*.mp4 *.avi *.mov *.wmv *.mkv *.webm")])
        if file_path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)

    def select_sample_file():
        sample_file_path = filedialog.askopenfilename(title="選擇樣本影片", filetypes=[("影片檔", "*.mp4 *.avi *.mov *.wmv *.mkv *.webm")])
        if sample_file_path:
            sample_entry.delete(0, tk.END)
            sample_entry.insert(0, sample_file_path)

    def select_output_file():
        output_file_path = filedialog.asksaveasfilename(defaultextension=".mp4", title="選擇輸出的影片", filetypes=[("影片檔", "*.mp4 *.avi *.mov *.wmv *.mkv *.webm")])
        if output_file_path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, output_file_path)

    def run_repair():
        global running
        if running:
            messagebox.showerror("錯誤", "程序正在進行中！")
        
        input_file = input_entry.get()
        output_file = output_entry.get()
        sample_file = sample_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("錯誤", "請選擇輸入與輸出檔案")
            return
        running = True

        if sample_file:
            command = ["VideoFileRepairer.exe", "-a", input_file, output_file, sample_file]
        else:
            command = ["VideoFileRepairer.exe", "-r", input_file, output_file]

        try:
            
            output_text.insert(tk.END, "")
            output_text.insert(tk.END, "[GUI] 開始修復...\n")
            output_text.see(tk.END)
            time.sleep(1)
            error = False
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            
            for line in process.stdout:
                output_text.insert(tk.END, line)
                output_text.see(tk.END)
                if "error code:" in line:
                    error = True

            process.wait()
            if process.returncode == 0 and not error:
                messagebox.showinfo("成功", "影片修復完成")
            else:
                if sample_file:
                    messagebox.showerror("錯誤", "修復失敗，請檢查日誌！")
                else:
                    messagebox.showerror("錯誤", "修復失敗，請試著新增範例檔案（在同一個裝置拍的影片，格式相同，必須是好的）！")
        except Exception as e:
            messagebox.showerror("錯誤", f"修復過程中出現錯誤: {str(e)}")
        running = False
    def repair_button():
        threading.Thread(target=run_repair).start()
        

    # 元件設置
    tk.Label(root, text="選擇要修復的影片:").pack(pady=5)
    input_entry = tk.Entry(root, width=50)
    input_entry.pack(pady=5)
    tk.Button(root, text="選擇檔案", command=select_file).pack(pady=5)

    tk.Label(root, text="選擇輸出檔案:").pack(pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.pack(pady=5)
    tk.Button(root, text="選擇輸出檔案", command=select_output_file).pack(pady=5)

    tk.Label(root, text="（選擇樣本影片，可選）:").pack(pady=5)
    sample_entry = tk.Entry(root, width=50)
    sample_entry.pack(pady=5)
    tk.Button(root, text="選擇樣本影片", command=select_sample_file).pack(pady=5)

    tk.Button(root, text="修復！", command=repair_button).pack(pady=20)

    tk.Label(root, text="日誌:").pack(pady=5)
    output_text = tk.Text(root, height=10, width=60)
    output_text.pack(pady=5)

    root.mainloop()

create_gui()

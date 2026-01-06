import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
from pathlib import Path

class JPGtoPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG 轉 PDF 轉換器")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.image_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # 標題
        title_label = tk.Label(self.root, text="JPG 轉 PDF 轉換器", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 按鈕框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # 選擇資料夾按鈕
        folder_btn = tk.Button(button_frame, text="📁 選擇資料夾", 
                              command=self.select_folder,
                              bg="#4CAF50", fg="white", 
                              font=("Arial", 11), padx=20, pady=8)
        folder_btn.grid(row=0, column=0, padx=5)
        
        # 選擇個別檔案按鈕
        files_btn = tk.Button(button_frame, text="📄 選擇檔案", 
                             command=self.select_files,
                             bg="#2196F3", fg="white", 
                             font=("Arial", 11), padx=20, pady=8)
        files_btn.grid(row=0, column=1, padx=5)
        
        # 清除列表按鈕
        clear_btn = tk.Button(button_frame, text="🗑️ 清除列表", 
                             command=self.clear_list,
                             bg="#f44336", fg="white", 
                             font=("Arial", 11), padx=20, pady=8)
        clear_btn.grid(row=0, column=2, padx=5)
        
        # 檔案列表標籤
        list_label = tk.Label(self.root, text="已選擇的圖片:", 
                             font=("Arial", 11, "bold"))
        list_label.pack(pady=(10, 5))
        
        # 建立帶有捲軸的列表框架
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # 捲軸
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框
        self.file_listbox = tk.Listbox(list_frame, 
                                       yscrollcommand=scrollbar.set,
                                       font=("Arial", 10),
                                       selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # 檔案計數標籤
        self.count_label = tk.Label(self.root, text="已選擇 0 個檔案", 
                                   font=("Arial", 10))
        self.count_label.pack(pady=5)
        
        # 轉換按鈕
        convert_btn = tk.Button(self.root, text="✨ 轉換為 PDF", 
                               command=self.convert_to_pdf,
                               bg="#FF9800", fg="white", 
                               font=("Arial", 12, "bold"), 
                               padx=30, pady=10)
        convert_btn.pack(pady=15)
        
        # 狀態標籤
        self.status_label = tk.Label(self.root, text="", 
                                     font=("Arial", 9), fg="gray")
        self.status_label.pack(pady=5)
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="選擇包含 JPG 圖片的資料夾")
        if folder_path:
            jpg_files = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg')):
                    full_path = os.path.join(folder_path, file)
                    jpg_files.append(full_path)
            
            if jpg_files:
                # 按檔名排序
                jpg_files.sort()
                self.image_files.extend(jpg_files)
                self.update_listbox()
                self.status_label.config(
                    text=f"從資料夾匯入了 {len(jpg_files)} 個 JPG 檔案", 
                    fg="green"
                )
            else:
                messagebox.showwarning("警告", "該資料夾中沒有找到 JPG 檔案!")
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="選擇 JPG 圖片",
            filetypes=[("JPG 圖片", "*.jpg *.jpeg"), ("所有檔案", "*.*")]
        )
        if files:
            self.image_files.extend(files)
            self.update_listbox()
            self.status_label.config(
                text=f"新增了 {len(files)} 個檔案", 
                fg="green"
            )
    
    def clear_list(self):
        self.image_files = []
        self.update_listbox()
        self.status_label.config(text="列表已清除", fg="gray")
    
    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.image_files:
            filename = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, filename)
        self.count_label.config(text=f"已選擇 {len(self.image_files)} 個檔案")
    
    def convert_to_pdf(self):
        if not self.image_files:
            messagebox.showwarning("警告", "請先選擇要轉換的圖片!")
            return
        
        # 選擇儲存位置
        output_path = filedialog.asksaveasfilename(
            title="儲存 PDF 檔案",
            defaultextension=".pdf",
            filetypes=[("PDF 檔案", "*.pdf"), ("所有檔案", "*.*")]
        )
        
        if not output_path:
            return
        
        try:
            # 開啟所有圖片
            images = []
            for img_path in self.image_files:
                img = Image.open(img_path)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            
            # 儲存為 PDF
            if len(images) == 1:
                images[0].save(output_path, 'PDF', resolution=100.0)
            else:
                images[0].save(output_path, 'PDF', resolution=100.0, 
                              save_all=True, append_images=images[1:])
            
            messagebox.showinfo("成功", f"PDF 已成功儲存至:\n{output_path}")
            self.status_label.config(text="轉換成功!", fg="green")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"轉換失敗:\n{str(e)}")
            self.status_label.config(text="轉換失敗!", fg="red")

def main():
    root = tk.Tk()
    app = JPGtoPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
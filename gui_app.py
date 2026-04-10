import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import threading
import gpt_script as auto_publish
import os

class BlogPublisherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 블로그 자동 발행기")
        self.root.geometry("500x400")
        
        # 1. Keyword Selection Section
        self.keyword_frame = ttk.LabelFrame(root, text="키워드 선택")
        self.keyword_frame.pack(fill="x", padx=10, pady=10)
        
        self.keywords = self.load_keywords()
        self.selected_keyword = tk.StringVar()
        
        self.keyword_combo = ttk.Combobox(self.keyword_frame, textvariable=self.selected_keyword, values=self.keywords, state="readonly")
        self.keyword_combo.pack(fill="x", padx=10, pady=10)
        if self.keywords:
            self.keyword_combo.current(0)
            
        # 2. Action Section
        self.action_frame = ttk.Frame(root)
        self.action_frame.pack(fill="x", padx=10, pady=5)
        
        self.publish_btn = ttk.Button(self.action_frame, text="글 발행하기", command=self.start_publish_thread)
        self.publish_btn.pack(fill="x", ipady=5)
        
        # 3. Log Section
        self.log_frame = ttk.LabelFrame(root, text="진행 로그")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(self.log_frame, state='disabled', height=10)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        
    def load_keywords(self):
        try:
            if not os.path.exists("keywords.xlsx"):
                self.log("❌ 'keywords.xlsx' 파일을 찾을 수 없습니다.")
                return []
            
            df = pd.read_excel("keywords.xlsx")
            if "Keywords" not in df.columns:
                self.log("❌ 엑셀 파일에 'Keywords' 컬럼이 없습니다.")
                return []
                
            return df["Keywords"].dropna().tolist()
        except Exception as e:
            self.log(f"❌ 키워드 로딩 실패: {e}")
            return []
            
    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, str(message) + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        
    def start_publish_thread(self):
        keyword = self.selected_keyword.get()
        if not keyword:
            messagebox.showwarning("경고", "키워드를 선택해주세요.")
            return
            
        self.publish_btn.config(state="disabled")
        self.log(f"--- '{keyword}' 주제로 발행 시작 ---")
        
        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.run_publish, args=(keyword,))
        thread.start()
        
    def run_publish(self, keyword):
        try:
            # Pass self.log as the callback to capture output
            auto_publish.post_to_naver_blog(keyword, log=self.log)
        except Exception as e:
            self.log(f"❌ 치명적 오류 발생: {e}")
        finally:
            self.root.after(0, lambda: self.publish_btn.config(state="normal"))
            self.log("--- 작업 종료 ---")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogPublisherApp(root)
    root.mainloop()

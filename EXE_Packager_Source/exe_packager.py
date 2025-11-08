#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXE打包工具 - Python脚本转EXE工具
用于将Python脚本打包成独立的可执行文件
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import threading
import time
from datetime import datetime
import PyInstaller.__main__


class EXEPackager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EXE打包工具 - Python转EXE")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # 打包参数
        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.one_file = tk.BooleanVar(value=True)
        self.windowed = tk.BooleanVar(value=True)
        self.icon_path = tk.StringVar()
        
        # 创建界面
        self.create_main_area()
        self.create_status_bar()
        
        # 设置样式
        self.setup_styles()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('TButton', background='#3c3f41', foreground='white')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TCheckbutton', background='#2b2b2b', foreground='white')
        
    def create_main_area(self):
        """创建主界面"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        title_label = ttk.Label(main_frame, text="EXE打包工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=10)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="1. 选择Python文件", padding=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Python文件:").grid(row=0, column=0, sticky=tk.W, pady=2)
        file_entry = ttk.Entry(file_frame, textvariable=self.script_path, width=60)
        file_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)
        ttk.Button(file_frame, text="浏览", command=self.select_script).grid(row=0, column=2, padx=5, pady=2)
        
        # 输出目录
        ttk.Label(file_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=2)
        output_entry = ttk.Entry(file_frame, textvariable=self.output_dir, width=60)
        output_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
        ttk.Button(file_frame, text="浏览", command=self.select_output_dir).grid(row=1, column=2, padx=5, pady=2)
        
        file_frame.columnconfigure(1, weight=1)
        
        # 打包选项
        options_frame = ttk.LabelFrame(main_frame, text="2. 打包选项", padding=10)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(options_frame, text="单文件模式 (--onefile)", variable=self.one_file).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="窗口模式 (--windowed)", variable=self.windowed).pack(anchor=tk.W, pady=2)
        
        # 图标选择
        icon_frame = ttk.Frame(options_frame)
        icon_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(icon_frame, text="图标文件:").pack(side=tk.LEFT)
        icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_path, width=50)
        icon_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(icon_frame, text="浏览", command=self.select_icon).pack(side=tk.LEFT)
        
        # 打包按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="开始打包", command=self.start_packaging, style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除日志", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # 日志输出
        log_frame = ttk.LabelFrame(main_frame, text="3. 打包日志", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#00ff00',
            height=15
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.status_progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.status_progress.pack(side=tk.RIGHT, padx=5)
        
    def select_script(self):
        """选择Python脚本"""
        file_path = filedialog.askopenfilename(
            title="选择Python脚本",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.script_path.set(file_path)
            # 默认输出目录为脚本所在目录
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(file_path))
            
    def select_output_dir(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        
        if dir_path:
            self.output_dir.set(dir_path)
            
    def select_icon(self):
        """选择图标文件"""
        file_path = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.icon_path.set(file_path)
            
    def log_message(self, message):
        """向日志框添加消息"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def start_packaging(self):
        """开始打包"""
        if not self.script_path.get():
            messagebox.showerror("错误", "请选择要打包的Python脚本")
            return
            
        if not self.output_dir.get():
            messagebox.showerror("错误", "请选择输出目录")
            return
            
        if not os.path.exists(self.script_path.get()):
            messagebox.showerror("错误", "Python脚本不存在")
            return
            
        # 在新线程中执行打包
        threading.Thread(target=self._packaging_thread, daemon=True).start()
        
    def _packaging_thread(self):
        """打包线程"""
        self.root.after(0, self._before_packaging)
        
        try:
            # 构建PyInstaller命令参数
            args = [self.script_path.get(), '--distpath', self.output_dir.get()]
            
            if self.one_file.get():
                args.append('--onefile')
                
            if self.windowed.get():
                args.append('--windowed')
                
            if self.icon_path.get() and os.path.exists(self.icon_path.get()):
                args.extend(['--icon', self.icon_path.get()])
                
            # 执行PyInstaller
            self.root.after(0, lambda: self.log_message("开始执行PyInstaller..."))
            self.root.after(0, lambda: self.log_message(f"命令: pyinstaller {' '.join(args)}"))
            
            # 创建临时spec文件以更好地控制打包过程
            spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.script_path.get()}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=os.path.splitext(os.path.basename('{self.script_path.get()}'))[0],
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=not {str(self.windowed.get()).lower()},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{self.icon_path.get()}' if self.icon_path.get() and os.path.exists(self.icon_path.get()) else None
)
"""
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.spec', delete=False, encoding='utf-8') as spec_file:
                spec_file.write(spec_content)
                spec_file_path = spec_file.name
            
            # 使用spec文件执行PyInstaller
            result = subprocess.run(
                [sys.executable, '-m', 'PyInstaller', spec_file_path],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            # 清理临时spec文件
            os.remove(spec_file_path)
            
            self.root.after(0, lambda: self._after_packaging(result))
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_packaging_error(str(e)))
            
    def _before_packaging(self):
        """打包前的UI更新"""
        self.status_progress.start()
        self.status_label.config(text="正在打包...")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def _after_packaging(self, result):
        """打包后的UI更新"""
        self.status_progress.stop()
        self.status_label.config(text="打包完成")
        
        if result.returncode == 0:
            self.log_message("打包成功！")
            self.log_message(f"输出目录: {self.output_dir.get()}")
            messagebox.showinfo("成功", f"打包成功！\nEXE文件已保存到: {self.output_dir.get()}")
        else:
            self.log_message("打包失败！")
            self.log_message(f"错误信息: {result.stderr}")
            messagebox.showerror("错误", f"打包失败！\n{result.stderr}")
        
    def _handle_packaging_error(self, error):
        """处理打包错误"""
        self.status_progress.stop()
        self.status_label.config(text="打包出错")
        self.log_message(f"打包错误: {error}")
        messagebox.showerror("错误", f"打包过程中发生错误: {error}")
        
    def clear_log(self):
        """清除日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """主函数，用于启动EXE打包工具"""
    app = EXEPackager()
    app.run()


if __name__ == "__main__":
    main()
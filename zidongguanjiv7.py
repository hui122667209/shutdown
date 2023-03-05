import os
import time
import tkinter as tk
import tkinter.messagebox as messagebox
import threading

class ShutdownGUI:
    def __init__(self, master):
        self.master = master
        master.title("自动关机程序")

        # 标题
        self.label_title = tk.Label(master, text="自动关机程序", font=("Arial", 20))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # 输入关机时间的标签和文本框
        self.label_shutdown_time = tk.Label(master, text="关机时间（格式：年-月-日-时-分-秒）：", font=("Arial", 12))
        self.label_shutdown_time.grid(row=1, column=0, padx=20, pady=10)
        self.entry_shutdown_time = tk.Entry(master, font=("Arial", 12), width=30)
        self.entry_shutdown_time.grid(row=1, column=1, padx=20, pady=10)

        # 显示倒计时的标签和文本框
        self.label_countdown = tk.Label(master, text="倒计时：", font=("Arial", 12))
        self.label_countdown.grid(row=2, column=0, padx=20, pady=10)
        self.var_countdown = tk.StringVar(value="00:00:00")
        self.entry_countdown = tk.Entry(master, font=("Arial", 12), textvariable=self.var_countdown, state="readonly")
        self.entry_countdown.grid(row=2, column=1, padx=20, pady=10)

        # 开始关机按钮
        self.button_shutdown = tk.Button(master, text="开始关机", font=("Arial", 12), command=self.shutdown)
        self.button_shutdown.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        ...
        # 停止关机按钮
        self.stop = False  # 初始化stop属性
        self.button_stop = tk.Button(master, text="停止关机", font=("Arial", 12), command=self.stop_shutdown)
        self.button_stop.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
        ...
    def countdown(self, shutdown_time,lock):
        # 计算倒计时并更新文本框
        while True:
            current_time = time.time()
            time_diff = shutdown_time - current_time
            if time_diff <= 0:
                break
            hours, remainder = divmod(time_diff, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_str = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
            with lock:
                self.var_countdown.set(countdown_str)
                
             # 添加判断停止关机按钮是否被按下
            with lock:
                if self.stop:
                    return
            

            time.sleep(1)  # 使用 after 方法代替 time.sleep   
            # 关机
        if not self.stop:
            os.system("shutdown /s /t 0")
        
        with lock:
            self.master.update()    
    def shutdown(self):
        # 获取要关机的时间并计算倒计时
        shutdown_time_str = self.entry_shutdown_time.get()
        try:
            shutdown_time = time.mktime(time.strptime(shutdown_time_str, "%Y-%m-%d-%H-%M-%S"))
        except ValueError:
            tk.messagebox.showerror("错误", "时间格式不正确，请按照格式输入")
            self.entry_shutdown_time.delete(0, tk.END)  # 清空输入框
            return  # return提前结束函数  # pass则不返回并执行后续操作
        
        # 判断输入的关机时间是否小于电脑当前时间
        current_time = time.time()
        if shutdown_time <= current_time:
            tk.messagebox.showwarning("警告", "输入的关机时间已过，请重新输入")
            self.entry_shutdown_time.delete(0, tk.END)  # 清空输入框
            return
        # 创建锁对象
        lock = threading.Lock()
        # 禁用文本框和按钮
        self.entry_shutdown_time.config(state="disabled")
        self.button_shutdown.config(state="disabled")

        # 创建新线程并运行 countdown() 函数
        countdown_thread = threading.Thread(target=self.countdown, args=(shutdown_time, lock))
        countdown_thread.start()


        # 开始倒计时和关机
        
        # 获取要关机的时间并计算倒计时
        lock = threading.Lock()  # 创建锁
        # 添加停止关机按钮
        self.stop = False
        
         # 创建新线程并运行 countdown() 函数
        countdown_thread = threading.Thread(target=self.countdown, args=(shutdown_time, lock))
        countdown_thread.start()

        
    def stop_shutdown(self):
        self.stop = True
        self.var_countdown.set("00:00:00")
        self.entry_shutdown_time.config(state="normal")
        self.button_shutdown.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownGUI(root)
    root.mainloop()
    

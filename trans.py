import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
class TranslatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("简易翻译小插件")
        self.root.configure(bg="white")  # 设置窗口背景颜色为白色


        # Create a Canvas widget
        self.canvas = tk.Canvas(root, width=620, height=390,bg="white")
        self.canvas.pack(fill="both", expand=True)

        # SecretKey Input Label
        self.school_name = tk.Label(root, text="信阳师范大学")
        self.canvas.create_window(510, 360, anchor="nw", window=self.school_name)

        # Load and resize the background image
        self.bg_image = Image.open("./logo.jpg")
        self.bg_image = self.bg_image.resize((100, 100),  Image.LANCZOS )
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(500, 250, anchor="nw", image=self.bg_image)

        # Input Text Label
        self.input_text_label = tk.Label(root, text="输入文本:")
        self.canvas.create_window(10, 10, anchor="nw", window=self.input_text_label)

        # Input Text
        self.input_text = tk.Text(root, height=10, width=40,bg="white")
        self.canvas.create_window(10, 40, anchor="nw", window=self.input_text)

        # Output Text Label
        self.output_text_label = tk.Label(root, text="译文:")
        self.canvas.create_window(320, 10, anchor="nw", window=self.output_text_label)

        # Output Text
        self.output_text = tk.Text(root, height=10, width=40,bg="white")
        self.canvas.create_window(320, 40, anchor="nw", window=self.output_text)

        # Language Selection
        self.language_label = tk.Label(root, text="选择语言:")
        self.canvas.create_window(10, 220, anchor="nw", window=self.language_label)

        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(root, textvariable=self.language_var)
        self.language_combobox['values'] = ('en', 'zh', 'zh-TW', 'ja', 'ko', 'fr', 'es', 'it', 'de', 'tr', 'ru', 'pt', 'vi', 'id', 'th', 'ms', 'ar', 'hi')
        self.canvas.create_window(100, 220, anchor="nw", window=self.language_combobox)

        # SecretId Input Label
        self.secret_id_label = tk.Label(root, text="输入SecretId:")
        self.canvas.create_window(10, 260, anchor="nw", window=self.secret_id_label)

        # SecretId Input
        self.secret_id_entry = tk.Entry(root, width=40,bg="white")
        self.canvas.create_window(120, 260, anchor="nw", window=self.secret_id_entry)

        # SecretKey Input Label
        self.secret_key_label = tk.Label(root, text="输入SecretKey:")
        self.canvas.create_window(10, 300, anchor="nw", window=self.secret_key_label)

        # SecretKey Input
        self.secret_key_entry = tk.Entry(root, width=40,bg="white")
        self.canvas.create_window(120, 300, anchor="nw", window=self.secret_key_entry)

        # Translate Button
        self.translate_button = tk.Button(root, text="翻译", command=self.translate_text, bg="white", fg="black", bd=2,
                                          relief="raised", font=("Arial", 12, "bold"))
        self.canvas.create_window(10, 340, anchor="nw", window=self.translate_button)

    def translate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        target_language = self.language_var.get()
        secret_id = self.secret_id_entry.get().strip()
        secret_key = self.secret_key_entry.get().strip()

        if not input_text or not target_language or not secret_id or not secret_key:
            messagebox.showwarning("警告", "请填写所有字段")
            return

        try:
            # Instantiate a credential object with the SecretId and SecretKey
            cred = credential.Credential(secret_id, secret_key)
            # Instantiate the client object for the TMT service
            client = tmt_client.TmtClient(cred, "ap-guangzhou")
            # Instantiate a request object
            req = models.TextTranslateRequest()
            req.SourceText = input_text
            req.Source = "auto"
            req.Target = target_language
            req.ProjectId = 0

            # Call the TextTranslate method
            resp = client.TextTranslate(req)
            # Get the translated text
            translated_text = resp.TargetText

            # Display the translated text in the output text widget
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)

        except TencentCloudSDKException as err:
            messagebox.showerror("错误", f"翻译失败: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
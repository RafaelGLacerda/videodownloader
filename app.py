# video_downloader_app.py
import os
import threading
import shutil
import yt_dlp

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup


class VideoDownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.ffmpeg_instalado = shutil.which("ffmpeg") is not None
        self.download_path = os.getcwd()

        self.add_widget(Label(text="📥 Downloader de Vídeos (YouTube, TikTok, Insta...)", size_hint_y=None, height=40))

        # Campo de links
        self.links_input = TextInput(
            hint_text="Cole os links (um por linha)",
            multiline=True,
            size_hint_y=None,
            height=150
        )
        self.add_widget(self.links_input)

        # Botão de pasta
        self.folder_button = Button(text="📂 Escolher pasta de destino", size_hint_y=None, height=50)
        self.folder_button.bind(on_release=self.choose_folder)
        self.add_widget(self.folder_button)

        self.path_label = Label(text=f"Pasta atual: {self.download_path}", size_hint_y=None, height=30)
        self.add_widget(self.path_label)

        # Botão de download
        self.download_button = Button(text="⬇️ Baixar Vídeos", size_hint_y=None, height=50)
        self.download_button.bind(on_release=lambda x: self.start_download())
        self.add_widget(self.download_button)

        # Caixa de status
        self.status = TextInput(readonly=True, size_hint_y=1)
        scroll = ScrollView()
        scroll.add_widget(self.status)
        self.add_widget(scroll)

    def choose_folder(self, instance):
        chooser = FileChooserIconView(path=self.download_path)

        def select_path(instance, selection):
            if selection:
                self.download_path = selection[0]
                self.path_label.text = f"Pasta atual: {self.download_path}"
            popup.dismiss()

        popup = Popup(title="Escolher Pasta", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=select_path)
        popup.open()

    def log_status(self, msg):
        self.status.text += msg + "\n"

    def start_download(self):
        links = [l.strip() for l in self.links_input.text.split("\n") if l.strip()]
        if not links:
            self.log_status("⚠️ Insira pelo menos um link!")
            return
        threading.Thread(target=self.download_videos, args=(links,), daemon=True).start()

    def download_videos(self, links):
        self.log_status("🚀 Iniciando downloads...\n")
        for link in links:
            self.log_status(f"Baixando: {link}")
            try:
                if self.ffmpeg_instalado:
                    ydl_opts = {
                        'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                        'format': 'bestvideo+bestaudio/best',
                        'merge_output_format': 'mp4',
                        'quiet': True,
                        'noprogress': True,
                    }
                else:
                    ydl_opts = {
                        'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                        'format': 'best',
                        'quiet': True,
                        'noprogress': True,
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                self.log_status(f"✅ Concluído: {link}\n")
            except Exception as e:
                self.log_status(f"❌ Erro ao baixar {link}: {str(e)}\n")

        self.log_status("🎉 Todos os downloads foram finalizados!")


class VideoDownloaderApp(App):
    def build(self):
        return VideoDownloaderUI()


if __name__ == "__main__":
    VideoDownloaderApp().run()

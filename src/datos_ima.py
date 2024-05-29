import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class Watcher:
    DIRECTORY_TO_WATCH = "C:/Users/Utilities99/Pictures/consumos"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    def on_modified(self, event):
        if not event.is_directory and event.event_type in ['modified', 'created']:
            print(f"Received {event.event_type} event - {event.src_path}")
            copy_and_update_git(event.src_path)

def copy_and_update_git(src_path):
    # Copia el archivo modificado a la carpeta del proyecto
    copy_file(src_path)
    # Inicia un hilo para actualizar el repositorio en GitHub
    git_thread = threading.Thread(target=update_git)
    git_thread.start()

def copy_file(src_path):
    # Ruta del directorio de destino dentro del proyecto
    dst_path = os.path.join('C:/Users/Utilities99/Documents/pruebasubir')  # Actualiza esta ruta a tu carpeta del proyecto
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    shutil.copy(src_path, dst_path)

def update_git():
    try:
        os.system("git add .")
        os.system('git commit -m "Auto-update images"')
        os.system("git push")
    except Exception as e:
        print(f"Error al subir a GitHub: {e}")

def start_watcher():
    w = Watcher()
    w.run()

if __name__ == '__main__':
    start_watcher()

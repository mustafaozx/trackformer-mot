import streamlit as st
import os
import subprocess
import uuid

# Streamlit uygulamasını başlat
st.title("Video Gösterme Uygulaması")

# Video dosyasını seçme
video_file = st.file_uploader(
    "Lütfen bir video dosyası seçin", type=["mp4", "avi", "mov"]
)

if video_file is not None:
    # Videoyu geçici bir klasöre kaydetme
    temp_folder = str(uuid.uuid4())
    os.makedirs(temp_folder)

    video_path = os.path.join(temp_folder, video_file.name)

    with open(video_path, "wb") as f:
        f.write(video_file.read())

    # Videoyu Streamlit ile gösterme
    st.video(video_path)

    # ffmpeg kullanarak videoyu çerçevelere ayırma
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", "fps=30",  # Çerçeve hızı (örnekte 30 FPS olarak ayarlanmıştır)
        os.path.join(temp_folder, "%06d.png"),  # Çerçeve dosya adı formatı
    ]
    subprocess.run(cmd)

    # python src/track.py with \
    #     dataset_name=DEMO \
    #     data_root_dir=data/snakeboard \
    #     output_dir=data/snakeboard \
    #     write_images=pretty
    
    cmd = [
        "python", "src/track.py",
        "with", "dataset_name=DEMO",
        "data_root_dir={}".format(temp_folder),
        "output_dir={}".format(temp_folder),
        "write_images=pretty",
    ]
    
    subprocess.run(cmd)
    
    # merge frames
        # Çerçeveleri yeniden videoya dönüştürme
    output_video_path = os.path.join(temp_folder, "output_video.mp4")
    processed_frames_folder = os.path.join(temp_folder, "DEMO", temp_folder)
    cmd = [
        "ffmpeg",
        "-i", os.path.join(temp_folder, "DEMO", temp_folder, "%06d.png"),
        "-vf", "fps=30",  # Aynı çerçeve hızıyla ayarlayın
        output_video_path
    ]
    subprocess.run(cmd)
    
    st.video(output_video_path)


# Uygulama sonu
st.write("Uygulama sona erdi.")

import cv2
import numpy as np
from pypylon import pylon


# Fungsi untuk mengatur frame rate menggunakan trackbar
def set_fps(val):
    global camera
    fps = val / 2.0  # Membagi val untuk mengatur FPS lebih halus
    camera.AcquisitionFrameRate.SetValue(fps)  # Set FPS pada kamera Pylon
    # print(f"Frame rate set to: {fps} FPS")


# Inisialisasi kamera Pylon
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Konfigurasi resolusi dan frame rate default
camera.Open()
camera.Width.Value = 1920  # Set lebar gambar
camera.Height.Value = 1080  # Set tinggi gambar
camera.AcquisitionFrameRateEnable.SetValue(True)
initial_fps = 4.5
camera.AcquisitionFrameRate.SetValue(initial_fps)  # Frame rate default 8 FPS

# Image Format Converter untuk mengonversi gambar ke format BGR yang kompatibel dengan OpenCV
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed  # Konversi ke format BGR 8-bit
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned  # Alignment bit

# Start capturing video
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Inisialisasi variabel
last_printed_row_sums = None
all_value_intensity = []
capturing_data = False
data_captured = False
key_start_threshold = (0, 60)

# Buat window dengan trackbar untuk mengubah frame rate
cv2.namedWindow("Layar dengan ROI")
cv2.createTrackbar(
    "FPS", "Layar dengan ROI", int(initial_fps * 2), 60, set_fps
)  # Trackbar FPS, dengan pembagian 2

# Loop utama untuk menangkap dan memproses frame
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Konversi gambar ke format yang kompatibel dengan OpenCV (BGR)
        image = converter.Convert(grabResult).GetArray()

        # Definisi koordinat awal (x1, y1) dan panjang serta lebar bounding box
        x1, y1, width, height = 900, 200, 1, 648  # Area yang dipantau

        # Salin gambar dan gambar kotak persegi panjang di atasnya
        rectangle_image = image.copy()
        cv2.rectangle(
            rectangle_image, (x1, y1), (x1 + width, y1 + height), (255, 0, 0), 2
        )

        # Tampilkan gambar asli dengan kotak persegi panjang
        cv2.imshow("Layar dengan ROI", rectangle_image)

        # Ambil nilai intensitas di dalam ROI (hanya channel biru)
        row_sums = [
            int(np.sum(row)) for row in image[y1 : y1 + height, x1 : x1 + width, 2]
        ]

        # Deteksi saat memulai data jika ada 60 data <= key_start_threshold di dalam row_sums
        if (
            sum(value <= key_start_threshold[1] for value in row_sums) >= 60
            and not capturing_data
            and not data_captured
        ):
            capturing_data = True
            all_value_intensity = []  # Reset data intensitas sebelumnya
            print("Start Capturing data...")
        # Kondisi baru: panjang data harus 648, dan nilai awal serta akhir berada dalam threshold key start
        # print("row_sums01", row_sums)
        if capturing_data and (
            len(row_sums) == 648
            and all(value <= key_start_threshold[1] for value in row_sums[:3])
            and all(value <= key_start_threshold[1] for value in row_sums[-3:])
        ):
            # print("row_sums02", row_sums)

            if (
                any(value > key_start_threshold[1] for value in row_sums)
                and row_sums != last_printed_row_sums
            ):
                # Hapus nilai di awal dan di akhir dalam rentang key start
                while len(row_sums) > 0 and row_sums[0] <= key_start_threshold[1]:
                    row_sums.pop(0)

                while len(row_sums) > 0 and row_sums[-1] <= key_start_threshold[1]:
                    row_sums.pop()

                # # Update: Ambil rata-rata dari pasangan nilai (2,3), (8,9), ..., (596,597)
                value_intensity = []
                # print("row_sums03", row_sums)
                for i in range(3, 598, 6):
                    pair_avg = int((row_sums[i] + row_sums[i + 1]) / 2)
                    value_intensity.append(pair_avg)
                # else:
                #     print(f"Skipping index {i} and {i + 1}, out of range")

                if value_intensity != last_printed_row_sums:
                    print("Value Intensity (pair avg): ", value_intensity)
                    all_value_intensity.extend(value_intensity)
                    last_printed_row_sums = value_intensity.copy()

        if (
            capturing_data
            and sum(value <= key_start_threshold[1] for value in row_sums) >= 60
            and all_value_intensity
        ):
            print("All Value Intensity: ", all_value_intensity)
            all_value_intensity = []
            capturing_data = False
            data_captured = True
            print("End Capturing data...")

        if data_captured:
            data_captured = False

        # Tunggu input kunci 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    grabResult.Release()

# Tutup semua jendela OpenCV dan kamera
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
# Real time testing_2

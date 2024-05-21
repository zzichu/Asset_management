import qrcode

def generate_qr_code(id, file_path):
    data = f"http://127.0.0.1/myapp/item/{id}"  # item의 ID를 URL에 포함
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

id = input("아이템 ID를 입력하세요: ")
file_path = "qr_code.png"  # QR 코드가 저장될 파일 경로

generate_qr_code(id, file_path)

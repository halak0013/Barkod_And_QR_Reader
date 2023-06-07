import qrcode


class QRCode():
    # Create a QR code instance
    def __init__(self):
        self.qr = qrcode.QRCode(
        version=10,  # QR code version (integer from 1 to 40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4  # Border size in boxes
    )



    def generate_qr_code(self,data):
        # Add data to the QR code
        #? id-name-price
        #data = "3 varan3 999.9"
        data2:str=data+""
        self.qr.add_data(data=data2)

        # Create the QR code image
        self.qr.make(fit=True)
        qr_image = self.qr.make_image(fill_color="black", back_color="white")

        # Save the image to a file
        image_path = f"image/{data}.png"
        qr_image.save(image_path)

        print("QR code generated and saved as", image_path)
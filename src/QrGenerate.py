import qrcode

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # QR code version (integer from 1 to 40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction level
    box_size=10,  # Size of each box in pixels
    border=4  # Border size in boxes
)

# Add data to the QR code
#? id-name-price
data = "123456"
qr.add_data(data)

# Create the QR code image
qr.make(fit=True)
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
image_path = f"image/{data}.png"

qr_image.save(image_path)

print("QR code generated and saved as", image_path)

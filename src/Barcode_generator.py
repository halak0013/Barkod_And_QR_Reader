import barcode
from barcode.writer import ImageWriter

# Generate barcode
def generate_barcode(data, barcode_type, output_path):
    # Create a barcode object
    barcode_class = barcode.get_barcode_class(barcode_type)
    barcode_object = barcode_class(data, writer=ImageWriter())

    # Save the barcode image
    barcode_object.save(output_path)


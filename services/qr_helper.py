import requests

QR_API_URL = "https://api.qrserver.com/v1/create-qr-code/"


def generate_qr_code(data_url, save_path):
    """
    Generate a QR code image for the given URL and save it to disk.
    data_url: the URL to encode into the QR code (e.g. a file download link).
    save_path: where to save the resulting PNG image.
    """
    params = {
        "size": "200x200",
        "data": data_url,
    }

    response = requests.get(QR_API_URL, params=params, timeout=10)
    response.raise_for_status()  # raises an exception for non-200 responses

    with open(save_path, "wb") as qr_file:
        qr_file.write(response.content)
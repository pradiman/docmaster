import os

import requests
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from forms.pdf_forms import ImagesToPdfForm, MergeForm, SplitForm
from services.image_manager import ImageManager
from services.pdf_manager import PDFManager
from services.qr_helper import generate_qr_code

app = Flask(__name__)

# Needed for flash messages and Flask-WTF forms (CSRF protection).
app.config["SECRET_KEY"] = "key"

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/merge", methods=["GET", "POST"])
def merge():
    form = MergeForm()
    if form.validate_on_submit():
        uploaded_files = form.pdf_files.data  # list of FileStorage objects

        # Save each uploaded PDF into uploads/
        saved_paths = []
        for file in uploaded_files:
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)
            saved_paths.append(save_path)

        # Merge them into a single PDF in outputs/
        output_filename = "merged.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        pdf_manager = PDFManager()
        pdf_manager.merge_pdf(saved_paths, output_path)

        flash("PDFs merged successfully!", "success")
        return render_template("merge.html", form=form, output_filename=output_filename)

    return render_template("merge.html", form=form)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


@app.route("/generate-qr/<filename>")
def generate_qr(filename):
    # Build the full download URL for this file, e.g.
    # http://127.0.0.1:5000/download/merged.pdf
    download_url = url_for("download", filename=filename, _external=True)

    qr_filename = f"qr_{filename}.png"
    qr_path = os.path.join(OUTPUT_FOLDER, qr_filename)

    try:
        generate_qr_code(download_url, qr_path)
    except requests.RequestException:
        flash("Could not generate QR code. Please try again.", "danger")
        return redirect(request.referrer or url_for("index"))

    flash("QR code generated!", "success")
    return redirect(url_for("show_qr", filename=filename))


@app.route("/qr/<filename>")
def show_qr(filename):
    qr_filename = f"qr_{filename}.png"
    return render_template("qr_result.html", filename=filename, qr_filename=qr_filename)

@app.route("/qr-image/<filename>")
def qr_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route("/split", methods=["GET", "POST"])
def split():
    form = SplitForm()
    if form.validate_on_submit():
        uploaded_file = form.pdf_file.data
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(save_path)

        start_str, end_str = form.page_range.data.split("-")
        start_page, end_page = int(start_str), int(end_str)

        output_filename = "split.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        pdf_manager = PDFManager()
        try:
            pdf_manager.split_pdf(save_path, start_page, end_page, output_path)
        except ValueError as error:
            flash(str(error), "danger")
            return render_template("split.html", form=form)

        flash("PDF split successfully!", "success")
        return render_template("split.html", form=form, output_filename=output_filename)

    return render_template("split.html", form=form)


@app.route("/images-to-pdf", methods=["GET", "POST"])
def images_to_pdf():
    form = ImagesToPdfForm()
    if form.validate_on_submit():
        uploaded_files = form.image_files.data  # list of FileStorage objects

        saved_paths = []
        for file in uploaded_files:
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)
            saved_paths.append(save_path)

        output_filename = "images.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        image_manager = ImageManager()
        image_manager.images_to_pdf(saved_paths, output_path)

        flash("Images converted to PDF successfully!", "success")
        return render_template("images_to_pdf.html", form=form, output_filename=output_filename)

    return render_template("images_to_pdf.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
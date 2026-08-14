import os
import uuid

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
from PIL import UnidentifiedImageError
from pypdf.errors import PdfReadError

from forms.pdf_forms import ImagesToPdfForm, MergeForm, SplitForm
from services.image_manager import ImageManager
from services.pdf_manager import PDFManager
from services.qr_helper import generate_qr_code

app = Flask(__name__)

# Needed for flash messages and Flask-WTF forms (CSRF protection).
app.config["SECRET_KEY"] = "key"
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB limit

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/merge", methods=["GET", "POST"])
def merge():
    form = MergeForm()
    if form.validate_on_submit():
        uploaded_files = form.pdf_files.data

        valid_files = [f for f in uploaded_files if f and f.filename]
        if len(valid_files) < 2:
            flash("Please select at least 2 PDF files to merge.", "danger")
            return render_template("merge.html", form=form)

        saved_paths = []
        for file in valid_files:
            unique_name = f"{uuid.uuid4().hex}_{file.filename}"
            save_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(save_path)
            saved_paths.append(save_path)

        output_filename = f"merged_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        pdf_manager = PDFManager()
        try:
           page_count = pdf_manager.merge_pdf(saved_paths, output_path)
        except PdfReadError:
            flash("One of the uploaded files is not a valid PDF.", "danger")
            return render_template("merge.html", form=form)

        for path in saved_paths:
            os.remove(path)

        flash(f"Merged {len(valid_files)} PDFs into a {page_count}-page document!", "success")
        return render_template("merge.html", form=form, output_filename=output_filename)

    return render_template("merge.html", form=form)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        flash("That file no longer exists. Please generate it again.", "danger")
        return redirect(url_for("index"))
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
        unique_name = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)
        uploaded_file.save(save_path)

        start_str, end_str = form.page_range.data.split("-")
        start_page, end_page = int(start_str), int(end_str)

        output_filename = f"split_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        pdf_manager = PDFManager()
        try:
            page_count = pdf_manager.split_pdf(save_path, start_page, end_page, output_path)
        except ValueError as error:
            flash(str(error), "danger")
            return render_template("split.html", form=form)
        except PdfReadError:
            flash("The uploaded file is not a valid PDF.", "danger")
            return render_template("split.html", form=form)

        os.remove(save_path)

        flash(f"Split successful! Extracted a {page_count}-page PDF.", "success")
        return render_template("split.html", form=form, output_filename=output_filename)

    return render_template("split.html", form=form)


@app.route("/images-to-pdf", methods=["GET", "POST"])
def images_to_pdf():
    form = ImagesToPdfForm()
    if form.validate_on_submit():
        uploaded_files = form.image_files.data

        saved_paths = []
        for file in uploaded_files:
            unique_name = f"{uuid.uuid4().hex}_{file.filename}"
            save_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(save_path)
            saved_paths.append(save_path)

        output_filename = f"images_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        image_manager = ImageManager()
        try:
            page_count = image_manager.images_to_pdf(saved_paths, output_path)
        except UnidentifiedImageError:
            flash("One of the uploaded files is not a valid image.", "danger")
            return render_template("images_to_pdf.html", form=form)

        for path in saved_paths:
            os.remove(path)

        flash(f"Converted {page_count} images into a PDF!", "success")
        return render_template("images_to_pdf.html", form=form, output_filename=output_filename)

    return render_template("images_to_pdf.html", form=form)


@app.errorhandler(500)
def handle_server_error(error):
    flash("Something went wrong. Please try again.", "danger")
    return redirect(url_for("index"))


@app.errorhandler(413)
def handle_file_too_large(error):
    flash("File too large. Maximum upload size is 20MB.", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
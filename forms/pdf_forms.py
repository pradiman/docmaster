from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired, MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp


class MergeForm(FlaskForm):
    """Form for uploading multiple PDFs to merge into one."""

    pdf_files = MultipleFileField(
        "Select PDF files (choose 2 or more)",
        validators=[
            FileRequired(message="Please select at least one PDF file."),
            FileAllowed(["pdf"], message="Only PDF files are allowed."),
        ],
    )
    submit = SubmitField("Merge PDFs")


class SplitForm(FlaskForm):
    """Form for uploading one PDF and specifying a page range to extract."""

    pdf_file = FileField(
        "Select a PDF file",
        validators=[
            FileRequired(message="Please select a PDF file."),
            FileAllowed(["pdf"], message="Only PDF files are allowed."),
        ],
    )
    page_range = StringField(
        "Page range (e.g. 1-3)",
        validators=[
            DataRequired(message="Please enter a page range."),
            Regexp(
                r"^\d+-\d+$",
                message="Page range must look like '1-3'.",
            ),
        ],
    )
    submit = SubmitField("Split PDF")


class ImagesToPdfForm(FlaskForm):
    """Form for uploading multiple images to combine into one PDF."""

    image_files = MultipleFileField(
        "Select images (JPG, JPEG, or PNG)",
        validators=[
            FileRequired(message="Please select at least one image."),
            FileAllowed(["jpg", "jpeg", "png"], message="Only JPG, JPEG, and PNG files are allowed."),
        ],
    )
    submit = SubmitField("Convert to PDF")
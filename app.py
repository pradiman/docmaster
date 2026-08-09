from flask import Flask, render_template

from forms.pdf_forms import ImagesToPdfForm, MergeForm, SplitForm

app = Flask(__name__)

# Needed for flash messages and Flask-WTF forms (CSRF protection).
app.config["SECRET_KEY"] = "dev-secret-key-change-later"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge", methods=["GET", "POST"])
def merge():
    form = MergeForm()
    if form.validate_on_submit():
        # Processing logic (actually merging the PDFs) is added in later phase.
        pass
    return render_template("merge.html", form=form)


@app.route("/split", methods=["GET", "POST"])
def split():
    form = SplitForm()
    if form.validate_on_submit():
        # Processing logic (actually splitting the PDF) is added in later phase.
        pass
    return render_template("split.html", form=form)


@app.route("/images-to-pdf", methods=["GET", "POST"])
def images_to_pdf():
    form = ImagesToPdfForm()
    if form.validate_on_submit():
        # Processing logic (actually converting images) is added in later phase.
        pass
    return render_template("images_to_pdf.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
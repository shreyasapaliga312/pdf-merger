from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = []

        file1 = request.files.get("pdf1")
        file2 = request.files.get("pdf2")
        file3 = request.files.get("pdf3")

        if file1 and file1.filename:
            files.append(file1)
        if file2 and file2.filename:
            files.append(file2)
        if file3 and file3.filename:
            files.append(file3)

        print("FILES COUNT:", len(files))

        if len(files) < 2:
            return "Please upload at least 2 PDF files"

        merger = PdfMerger()

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            merger.append(path)

        output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
        merger.write(output_path)
        merger.close()

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

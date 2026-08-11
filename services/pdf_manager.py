from pypdf import PdfWriter


class PDFManager:
    # Handles PDF merging and splitting.
    def merge_pdf(self, input_paths, output_path):
        """
        input_paths: list of file paths to PDFs, in the order they should appear in the merged output.
        output_path: file path where the merged PDF will be saved.
        """
        writer = PdfWriter()

        for path in input_paths:
            writer.append(path)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        writer.close()
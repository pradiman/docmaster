from pypdf import PdfReader, PdfWriter


class PDFManager:
    """Handles PDF operations: merging and splitting."""

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

    def split_pdf(self, input_path, start_page, end_page, output_path):
        """
        Extract a range of pages (1-indexed, inclusive) from a PDF and save them as a new PDF.
        start_page, end_page: page numbers as shown to a human, e.g. start_page=1 means the first page.
        """
        reader = PdfReader(input_path)
        writer = PdfWriter()

        total_pages = len(reader.pages)

        if start_page < 1 or end_page > total_pages or start_page > end_page:
            raise ValueError(
                f"Invalid page range {start_page}-{end_page}. "
                f"This PDF has {total_pages} pages."
            )

        # Convert to 0-indexed for pypdf
        for page_number in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_number])

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        writer.close()
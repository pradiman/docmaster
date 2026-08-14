from PIL import Image


class ImageManager:
    #Handles image operations: converting images into a PDF.

    def images_to_pdf(self, input_paths, output_path):
        """
        input_paths: list of file paths to images, in the order they should appear in the PDF.
        output_path: file path where the resulting PDF will be saved.
        """
        images = []

        for path in input_paths:
            image = Image.open(path)
            # PDFs need RGB mode; PNGs can be RGBA (with transparency),
            # which Pillow can't save directly into a PDF.
            if image.mode != "RGB":
                image = image.convert("RGB")
            images.append(image)

        first_image, remaining_images = images[0], images[1:]

        first_image.save(
            output_path,
            save_all=True,
            append_images=remaining_images,
        )

        return len(images)
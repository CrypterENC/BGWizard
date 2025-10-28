from flask import Flask, render_template, request, send_file, redirect, url_for
from backgroundremover.bg import remove
from PIL import Image
from io import BytesIO
import os
import zipfile
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle both single file (legacy) and multiple files
        if 'files' in request.files:
            files = request.files.getlist('files')
        elif 'file' in request.files:
            files = [request.files['file']]
        else:
            return redirect(url_for('upload_file', error='No files uploaded'))

        # Filter out empty files
        files = [f for f in files if f.filename]

        if not files:
            return redirect(url_for('upload_file', error='No valid files selected'))

        try:
            # Get parameters from form
            model_name = request.form.get('model', 'u2net')
            fg_threshold = int(request.form.get('fg_threshold', 240))
            bg_threshold = int(request.form.get('bg_threshold', 10))
            erode_size = int(request.form.get('erode_size', 10))
            output_format = request.form.get('output_format', 'png')

            # Validate files
            for file in files:
                # Validate file type
                allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
                if not file.filename.lower().split('.')[-1] in allowed_extensions:
                    return redirect(url_for('upload_file', error=f'Invalid file type: {file.filename}. Please upload PNG, JPG, JPEG, or WebP'))

                # Validate file size (10MB limit per file)
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                if file_size > 10 * 1024 * 1024:
                    return redirect(url_for('upload_file', error=f'File too large: {file.filename}. Maximum size is 10MB'))

            # Process single file
            if len(files) == 1:
                file = files[0]
                file_data = file.read()

                # Remove background using backgroundremover with user parameters
                output_data = remove(
                    file_data,
                    model_name=model_name,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=fg_threshold,
                    alpha_matting_background_threshold=bg_threshold,
                    alpha_matting_erode_structure_size=erode_size,
                    alpha_matting_base_size=1000
                )

                # Convert format if needed
                if output_format != 'png':
                    # Convert to PIL Image for format conversion
                    img = Image.open(BytesIO(output_data))
                    output_buffer = BytesIO()

                    if output_format == 'jpg':
                        # Convert transparent PNG to JPG with white background
                        if img.mode in ('RGBA', 'LA', 'P'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1])
                            img = background
                        img.save(output_buffer, 'JPEG', quality=95)
                        mime_type = 'image/jpeg'
                    elif output_format == 'webp':
                        img.save(output_buffer, 'WebP', quality=95)
                        mime_type = 'image/webp'

                    output_data = output_buffer.getvalue()

                # Return single processed image
                return send_file(
                    BytesIO(output_data),
                    mimetype=f'image/{output_format}' if output_format != 'jpg' else 'image/jpeg',
                    as_attachment=True,
                    download_name=f'bg_removed_{file.filename.rsplit(".", 1)[0]}.{output_format}'
                )

            # Process multiple files - create ZIP
            else:
                # Create temporary directory for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_path = os.path.join(temp_dir, 'processed_images.zip')

                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file in files:
                            file_data = file.read()

                            # Remove background
                            output_data = remove(
                                file_data,
                                model_name=model_name,
                                alpha_matting=True,
                                alpha_matting_foreground_threshold=fg_threshold,
                                alpha_matting_background_threshold=bg_threshold,
                                alpha_matting_erode_structure_size=erode_size,
                                alpha_matting_base_size=1000
                            )

                            # Convert format if needed
                            if output_format != 'png':
                                img = Image.open(BytesIO(output_data))
                                output_buffer = BytesIO()

                                if output_format == 'jpg':
                                    if img.mode in ('RGBA', 'LA', 'P'):
                                        background = Image.new('RGB', img.size, (255, 255, 255))
                                        if img.mode == 'P':
                                            img = img.convert('RGBA')
                                        background.paste(img, mask=img.split()[-1])
                                        img = background
                                    img.save(output_buffer, 'JPEG', quality=95)
                                elif output_format == 'webp':
                                    img.save(output_buffer, 'WebP', quality=95)

                                output_data = output_buffer.getvalue()

                            # Add to ZIP with processed filename
                            base_name = file.filename.rsplit(".", 1)[0]
                            zip_file.writestr(f'bg_removed_{base_name}.{output_format}', output_data)

                    # Return ZIP file
                    return send_file(
                        zip_path,
                        mimetype='application/zip',
                        as_attachment=True,
                        download_name='background_removed_images.zip'
                    )

        except Exception as e:
            error_msg = f'Processing failed: {str(e)}'
            return redirect(url_for('upload_file', error=error_msg))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)

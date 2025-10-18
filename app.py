from flask import Flask, request, send_file
import subprocess
import os
import shutil

app = Flask(__name__)

@app.route("/stitch", methods=["POST"])
def stitch_images():
    data = request.json
    urls = data.get("images", [])

    if not urls:
        return {"error": "No images provided"}, 400

    # Create working folder
    workdir = "/app/images"
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir, exist_ok=True)

    # Download images sequentially
    for i, url in enumerate(urls):
        filename = os.path.join(workdir, f"img{i+1:03}.png")
        subprocess.run(["wget", "-O", filename, url], check=True)

    # Output video path
    output_path = "/app/output.mp4"

    # Stitch images into video (3 seconds per image)
    subprocess.run([
        "ffmpeg",
        "-framerate", "1/3",
        "-i", os.path.join(workdir, "img%03d.png"),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_path
    ], check=True)

    # Cleanup images folder
    shutil.rmtree(workdir)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

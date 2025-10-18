from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/stitch", methods=["POST"])
def stitch_images():
    data = request.json
    urls = data.get("images", [])

    if not urls:
        return {"error": "No images provided"}, 400

    os.makedirs("/app/images", exist_ok=True)
    # Download images sequentially
    for i, url in enumerate(urls):
        filename = f"/app/images/img{i+1:03}.png"
        subprocess.run(["wget", "-O", filename, url])

    # Run FFmpeg to stitch images
    output_path = "/app/output.mp4"
    subprocess.run([
        "ffmpeg",
        "-framerate", "1/3",      # 3 seconds per image
        "-i", "/app/images/img%03d.png",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_path
    ])

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

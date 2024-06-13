![oasis](https://socialify.git.ci/0zean/oasis/image?font=Source%20Code%20Pro&forks=1&issues=1&language=1&logo=https%3A%2F%2Fwww.nicepng.com%2Fpng%2Ffull%2F176-1762253_circle-water-ocean-blue-wave-aesthetic-overlay-tumblr.png&name=1&owner=1&pattern=Solid&pulls=1&stargazers=1&theme=Auto)


A streamlit web-app built using Python for Counter-Strike 2 modification. **For Educational purposes only.**

<div align="center">
<img src="./assets/demo.png" alt="icon"/>
</div>

# Setup

You'll need [a2x's cs2-dumper](https://github.com/a2x/cs2-dumper) for updating offsets at launch. You can finde the `cs2-dumper.exe` under releases.

Once downloaded, place it in the same folder as this repo after cloning.


### 🧬 1. Clone the Repo

```bash
git clone https://github.com/0zean/oasis.git
```

### 📦 2. Install libraries

Install `pip` dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 3. Run the application

To start the streamlit app, have CS2 running and double-click `start.bat`. This will run the offset dumper and start the streamlit server.

The web app will compile and then start running at `http://localhost:8501` which will be automatically copied to the clipboard.
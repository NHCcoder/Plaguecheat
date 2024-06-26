<h1 align="center">
    <img src="/assets/banner.png" width="450"/>
</h1>


<p align="center">
    <a href="https://raw.githubusercontent.com/0zean/oasis/master/LICENSE" target="_blank">MIT License</a>
</p>


<div align="center">
    <img src="https://img.shields.io/github/stars/0zean/oasis?style=for-the-badge&logo=github&color=dfb216"/>
    <img src="https://img.shields.io/github/issues/0zean/oasis?style=for-the-badge&logo=github&color=3380F5"/>
    <img src="https://img.shields.io/github/commit-activity/t/0zean/oasis?style=for-the-badge&logo=github&color=fe7d37"/>
    <img src="https://img.shields.io/github/forks/0zean/oasis?style=for-the-badge&logo=github&color=96ca01"/>
</div>


A streamlit web-app framework for Counter-Strike 2 mods built using Python. **For Educational purposes only.**

<div align="center">
<img src="/assets/demo.png" alt="icon"/>
</div>

# Setup

You'll need [a2x's cs2-dumper](https://github.com/a2x/cs2-dumper) for updating offsets at launch. You can finde the `cs2-dumper.exe` under releases.

Once downloaded, place it in the same folder as this repo after cloning.

## 🎚️ Features:
- [x] RCS (amount slider)
- [x] Trigger Bot (trigger key)
- [X] ESP (box, health, name, skeleton) 
- [ ] Misc


### 🧬 1. Clone the Repo

```bash
git clone https://github.com/0zean/oasis.git
```

### 🛠️ 2. Create virtual 

Using [Anaconda](https://docs.anaconda.com/miniconda/miniconda-install/), create a new env:

```bash
conda create -n oasis python=3.10
```

### 📦 3. Install libraries

Install `pip` dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 4. Run the application

To start the streamlit app, have CS2 running and double-click `start.bat`. This will run the offset dumper and start the streamlit server.

The web app will compile and then start running at `http://localhost:8501` which will be automatically copied to the clipboard.

The web app can also be accessed through your phone if you create an exception for port `8501` in your firewall Inbound Rules.

### ⚠️ Warning

Cheating in Counter-Strike 2 is not condoned and there is no guarentee this app won't result in a ban. This project is intended for educational purposes showcasing read-only memory applications. **Use at your own risk!**
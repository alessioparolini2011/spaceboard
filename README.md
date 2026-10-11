
![spaceboard logo](/assets/spaceboard_logo.jpg)

This is a simple, open-source and self-hosted dashboard to visualize space data, particularly **NEOs** (*Near Earth Objects*) and datas related to them. 

![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Nasa](https://img.shields.io/badge/NASA-2026-0B3D91?style=for-the-badge&logo=nasa&logoColor=white) ![Hack Club](https://img.shields.io/badge/Hack%20Club-Stardance-191970?style=for-the-badge&logo=hackclub&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-8.2.8-FF69B4?style=for-the-badge&logo=Textual&logoColor=white) ![Rich](https://img.shields.io/badge/Rich-15.0.0-FF69B4?style=for-the-badge&logo=Rich&logoColor=white) ![httpx](https://img.shields.io/badge/httpx-0.28.1-FF69B4?style=for-the-badge&logo=httpx&logoColor=white) ![pathlib](https://img.shields.io/badge/pathlib-1.0.1-FF69B4?style=for-the-badge) ![pyinstaller](https://img.shields.io/badge/pyinstaller-6.22.3-FF69B4?style=for-the-badge)

**LATEST RELEASE**: ---> https://github.com/alessioparolini2011/spaceboard/releases/tag/v1.2.8 <---

## Why I built this stuff?

Good question. I built it for an **[Hack Club](https://hackclub.com/)** x **[NASA](https://www.nasa.gov/)** event called **[Stardance](https://stardance.hackclub.com/home)**. The goal of this project is to provide a simple and easy access to datas about space objects that will get closer to our planet. 

When I had to choose a project for the event, I asked myself a question: **"What's a thing about space people can be interested in, but there aren't so much things about it?"**. Then I thought about *2024 YR4*, a NEO which, at one point, had as much as 3% of chance to hit the Earth. I remebered that this news went so much viral at the time, in 2024. So I thinked: **"Maybe something can show this objects data can be a cool stuff!"**. So **I started to work on show this data in a simple way**, and now, here we are.

## Software structure

```
spaceboard/
├── src/
│   ├── spaceboard/
│   │   ├── tcss/
│   │   │   ├── spaceboard.tcss
│   │   │   └── error_screen.tcss
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── onboard.py
│   │   ├── client.py
│   │   └── tui_dashboard.py
│   └── assets/ # all the images and GIF for the README
├── pyproject.toml
├── README.md
├── .gitignore
├── LICENSE
└── spaceboard.spec  #for the .exe
```

## How it works?

When you start the software for the first time, it will ask you for a NASA API key. The interface provides a full guide to get the key. 
When it's done, it creates a **`.spaceboard_env`** file where saves the API in your user profile directory. All this is done by **`onboard.py`**

Then, the TUI starts and makes a request on a secondary thread (so the interface doesn't freeze) to get the datas using the **`fetch_neo_data()`** function from **`client.py`**. The whole process is managed by **`tui_dashboard.py`**.

Then you can easily use your dashboard!

## Features

When you run the software, you can see a simple dashboard with a list of NEOs for the current day. You can navigate through the list with the **arrow keys** and change units system using the **c** key. The tab is well-spaced and easy to read. It uses a special system of layout for keep the scrool level costant and avoid the annoying "jumping" effect when you scroll through the list.

## Installation

You have 2 ways to install **spaceboard**: using the **Python package** or the **Windows .exe file**. 

### Python package 

To use the software, first check to have Python 3.11+ installed on your device. If you don't have it, you can download it from the [official Python website](https://www.python.org/downloads/). Then, you can install the software using the following command (paste it in the terminal, in the directory you want to install the software):


```bash
pip install spaceboard
```

and then 

```bash
spaceboard
```

> [!NOTE]
>This is the first release of the software, and my first package. I know the structure and the logic aren't perfect, but I'm working on it (I'm splitting files in different sub-packages, improving functions and features, adding \_\_init\_\_.py for every package and \_\_main\_\_.py...) in a V2 version. It was important to me to release it as soon as possible, for get feedbacks and improve it. Also Stardance event incorages developers to ship their projects starting from the MVP.

### Windows .exe file

Go to the latest release of the executable file [here](https://github.com/alessioparolini2011/spaceboard/releases/tag/v1.2.8). Then, install the **`spaceboard.zip`** on your device, then extract the directory, open it and click on **`spaceboard.exe`**.

**Antivirus Warning (False Positives)**: When you run the standalone .exe version for the first time, Windows Defender or other antivirus software might pop up an alert (like "Windows Protected your PC"). Don't panic! This is a 100% false positive. Because this application is compiled using PyInstaller and is not signed with an expensive Microsoft Developer Certificate, Windows blocks it by default to be safe. To run it, simply click on "More info" and then select "Run anyway". If you want to be completely sure, you can always inspect the full open-source code inside this repository or use the standard pip install spaceboard method.



At the first start, the software will give you the instructions to get your free NASA API key (**don't share it with anyone!**). If you want to have only a look, use "DEMO_KEY" as API key value (you'll get a really small nunber of requets per day, but it's ok to avoid the configuration of a really one). Follow them and you will finally enjoy **spaceboard**!

This is a preview of the dashboard in action:

![Spaceboard preview](/assets/sb_preview.gif)


> [!NOTE]
> GitHub and Hack Club are two amazing communities for developers. Please, if you want to edit and improve the project, do it in a good way and respect the code of conduct of both communities. Make sure to respect the [Hack Club Code of Conduct](https://hackclub.com/conduct/) and the [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines) before contributing. Make coding a better place for everyone. That said, happy coding!

## AI usage

I used AI to learn some of the skills I used in this project. **No code in this software is created by AI.**

## Credits

Credits go to the [Hack Club](https://hackclub.com/) and [NASA](https://www.nasa.gov/) for the event (thanks to NASA also for the [API](https://api.nasa.gov/)), to [Will McGugan](https://github.com/willmcgugan) for Rich and the Textual amazing framework, to [ProjectDiscovery](https://github.com/projectdiscovery) for httpx, to [pathlib](https://pypi.org/project/pathlib2/) and [pyinstaller](https://pypi.org/project/pyinstaller/) teams. Also, thanks to all the people that will contribute to this project in the future.
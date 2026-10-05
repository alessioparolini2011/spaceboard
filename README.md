

![spaceboard logo](/assets/ascii-art-text%20(1).png)

![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Nasa](https://img.shields.io/badge/NASA-2026-0B3D91?style=for-the-badge&logo=nasa&logoColor=white) ![Hack Club](https://img.shields.io/badge/Hack%20Club-Stardance-191970?style=for-the-badge&logo=hackclub&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-8.2.8-FF69B4?style=for-the-badge&logo=Textual&logoColor=white) ![Rich](https://img.shields.io/badge/Rich-15.0.0-FF69B4?style=for-the-badge&logo=Rich&logoColor=white) ![httpx](https://img.shields.io/badge/httpx-0.28.1-FF69B4?style=for-the-badge&logo=httpx&logoColor=white)

## What's this stuff?

Good question. This is a simple, open-source and self-hosted dashboard to visualize space datas, particularly **NEOs** (*Near Earth Objects*) and datas related to them. 

I built it for an **[Hack Club](https://hackclub.com/)** x **[NASA](https://www.nasa.gov/)** event called **[Stardance](https://stardance.hackclub.com/home)**. The goal of this project is to provide a simple and easy access to datas about space objects that will get closer to our planet. 

When I had to choose a project for the event, I asked myself a question: **"What's a thing about space people can be interestd in, but there aren't so much things about it?"**. Then I thinked about *2024 YR4*, a NEO which, at one point, had as much as 3% of chance to hit the Earth. I remebered that this news went so much viral at the time, in 2024. So I thinked: **"Maybe something can show this objects data can be a cool stuff!"**. So **I started to work on show this data in a simple way**, and now, here we are.

## How it works?

Well, it uses, as I mentioned before, the Python framework **[Textual](https://textual.textualize.io/)** to create a simple and interactive dashboard. It also uses the **[NASA API](https://api.nasa.gov/)** to get datas about NEOs with an [httpx](https://www.python-httpx.org/) client request. 

## Features

When you run the dashboard, you can see a simple dashboard with a list of NEOs for the current day. You can navigate through the list with the **arrow keys** and change units system using the **`c`** key. The tab is well-spaced and easy to read. It uses a special system of layout for keep the scrool level costant and avoid the annoying "jumping" effect when you scroll through the list.

## Installation and use


## Software structure

The **`main.py`** handles the interaction between **`onboard.py`** (that gets the currents 5-days window and the API key -after checking if it's present in the .env file-), and the **`tui_dashboard.py`**(that creates the dashboard and displays the datas). This one uses a function from **`client.py`** to get the datas from the API. Particularly, this request function has a sub-function to create a object for each NEO, using a different class for the two different metric sistems (imperial and metric). I choose to create 2 different classes, instead of one that used conversion methods to keep the code well-organized and for future improvements.

I spent a lot  of time to improve and optimize the code logic and structure, to provide a better experience and to encourage others developers to contribute to this project. So if you want to contribute, no problem! Just fork the repo and make a pull request. I will be happy to review it and merge it.

> [!NOTE]
> GitHub and Hack Club are two amazing communities for developers. Please, if you want to edit and improve the project, do it in a good way and respect the code of conducet of both communities. Make sure to respect the [Hack Club Code of Conduct](https://hackclub.com/conduct/) and the [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines) before contributing. Make coding a better place for everyone. That said, happy coding!
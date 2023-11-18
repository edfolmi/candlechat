# candlechat

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This is a simple chat web app that includes group and one-to-one chat; I relate the terminologies with that of blockchain i call group chat as blocks, because a block in blockchain contains series of transaction so also we've series of chat in block in this web app -- EDFolmi.

Here's why:
* To have a practical understanding of websockets.
* Curious to know how chat apps works
* I love coding! :smile:

I will add more features and AI technology to this project!

<!-- Use the `BLANK_README.md` to get started. -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



### Built With

This section include list of major frameworks/libraries used to bootstrap this project. <!-- Leave any add-ons/plugins for the acknowledgements section. Here are a few examples. -->

* Django Framework
* Django Rest Framework
* Javascript Websocket
* Django channels
* Django-redis
* Redis Tool
* HTML
* CSS

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you will set up this project locally.
To get a local copy up and running follow these simple example steps.


### Prerequisites

You need to utilize redis tool as message broker, you can simply get redis tool in docker.
- Install docker desktop.
- run redis from the terminal.

* pip
  ```sh
  docker run redis
  ```

### Installation

_Below is an example of how you can set up this app. <!-- This template doesn't rely on any external dependencies or services._ -->

1. Clone the repo
   ```sh
   git clone https://github.com/edfolmi/candlechat.git
   ```
2. Install Django packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create a .env file in projects folder, Enter your SECRET KEY in `.env`
   ```js
   SECRET_KEY=<ENTER YOUR API>;
   ```
4. Run Django project
   ```sh
   python manage.py runserver
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

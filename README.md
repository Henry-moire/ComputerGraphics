This project's goal is to efficiently process a large dataset by creating language-specific files like en-xx.xlsx for various languages, including English, Swahili and German. It will also generate separate JSONL files for training, testing and development data in these languages. Furthermore, it will produce a single JSON file containing translations from English to all languages, focusing on handling the dataset efficiently without resorting to recursive algorithms to prevent memory and time complexity problems.
# Prerequisites
Python Version 3.12.0 (https://www.python.org/downloads/)

PyCharm Version 2023.2.1 (https://www.jetbrains.com/pycharm/download/)
# Installation
1. To get started, clone the repository:
```sh
  https://github.com/Henry-moire/ComputerGraphics.git
```
2. Navigate to the project directory and create a virtual environment using:
```sh
  py -m venv myenv
```
3. Activate your virtual environent:
```sh
  myenv\Scripts\activate
```
4. Install project dependencies on your project:
Pandas: You can install it using pip
  ```bash
  pip install pandas
  ```
Jsonlines
  ```bash
  pip install jsonlines
  ```

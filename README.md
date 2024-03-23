# Labelling Tool

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

The Labelling Tool is a software application designed to assist in the process of labeling data for machine learning tasks. It provides an intuitive user interface for annotating and categorizing data, making it easier to create high-quality labeled datasets.

## Features

- Support for segmentations annotations
- Easy to install and configure
- Easy to integrate your model as preprocess

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/Nastarii/LabelingTool.git
    ```

2. Install the required dependencies:

    ```shell
    cd LabelingTool
    pip install -r requirements.txt
    ```

3. Add your dataset on this folder structure:

    ```
    - src
    |
    |-assets
        |
        |- imgs/
        |- masks/
    ```

4. Run the application:

    ```shell
    python main.py
    ```

## Usage

1. Launch the Labelling Tool application.
2. Import your dataset into the tool.
3. Start labeling your data using the provided annotation tools.
4. Save the labeled data to a desired format.
5. Use the labeled data for training your deep learning models.

## Contributing

Contributions are welcome! If you would like to contribute to the Labelling Tool, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
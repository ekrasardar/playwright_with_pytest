# DTAC LITE TEST AUTOMATION
This repository contains the code for test automation logics and test cases

## Prerequisites

1. Install any IDE where you can use python(E.g:Pycharm,VSCode)
2. Install Python

## Virtual environment setup
1. Clone the project
2. In the project directory run `python -m venv venv`.
3. Enable venv by running activate script in venv folder, for Windows run `.\venv\Scripts\Activate.ps1` and for Linux/Mac run `source venv`
4. Install Pytest `pip install pytest`
5. Run `pytest install requirements.txt`
6. Run `playwright install`

## Run test cases

# Pytest
### Arguments to pass for pytest are:
| Argument             | Description      | Default        | Choice                         | Mandatory | Remarks                                           |
|----------------------|------------------|----------------|--------------------------------|-----------|---------------------------------------------------|
| `--browser`          | Browser          | `chromium`     | `chromium` `firefox` `webkit`  | `N`       |                                                   |
| `--device`           | Device Name      | -              | -                              | `N`       | Take the device list from another list            |
| `--video`            | Video record     | `off`          | `on` `off` `retain-on-failure` | `N`       |                                                   |
| `--video-path`       | Video Path       | -              | -                              | `Y`       | If Video is `off` then path is not required       |
| `--resolution`       | Video Resolution | `720p`         | `480p` `720p` `1080p`          | `N`       | If Video is `off` then resolution is not required |
| `--testrail`         | Testrail Result  | Not applicable | Not applicable                 | `N`       |                                                   |
| `--tracing`          | Trace Test       | `off`          | `on` `off` `retain-on-failure` | `N`       |                                                   |
| `-n`                 | Parallel test    | -              | -                              | `N`       |                                                   |
| `--tr-testrun-name`  | Test run name    | -              | -                              | `Y`       | If `--testrail` is there then name is mandatory   |
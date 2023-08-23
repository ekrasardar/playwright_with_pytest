from typing import Any, Callable, Dict, Generator, List, Optional
import pytest
import json
from _pytest.fixtures import SubRequest
from _pytest.config.argparsing import Parser
from utils import helper_functions as hf
from utils.utils import Env, Lang
from utils.pages import Pages
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page
)
import os


def pytest_configure(config):
    config.addinivalue_line("markers", "skip_for_prod: skip test for production")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--env") != "prod":
        return
    skip_prod = pytest.mark.skip(reason="skipped for environment production")
    for item in items:
        if "skip_for_prod" in item.keywords:
            item.add_marker(skip_prod)


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--env",
        action="store",
        default=Env.STAGING.value,
        required=False,
        help="Set video resolution",
        choices=(Env.PROD.value, Env.PREPROD.value, Env.STAGING.value, Env.SANDBOX.value)
    )
    parser.addoption(
        "--resource-path",
        action="store",
        default="uploads/test-results",
        required=False,
        help="Set video directory path"
    )
    parser.addoption(
        "--uuid",
        action="store",
        default="10cf00a8_37db-49a9_8584_db5618eed788",
        required=False,
        help="Set unique id"
    )
    parser.addoption(
        "--resolution",
        action="store",
        default="720p",
        required=False,
        help="Set video resolution",
        choices=("480p", "720p", "1080p")
    )


def _handle_page_goto(page: Page, args: List[Any], kwargs: Dict[str, Any], base_url: str) -> None:
    url = args.pop()

    if not (url.startswith("http://") or url.startswith("https://")):
        url = base_url + url

    return page._goto(url, *args, **kwargs)  # type: ignore


def get_resolution(resolution):
    resolutions = {
        "480p": {"width": 854, "height": 480},
        "720p": {"width": 1280, "height": 720},
        "1080p": {"width": 1920, "height": 1080}
    }
    return resolutions.get(resolution, None) or ValueError("Invalid resolution parameter")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, video_path, request: SubRequest):
    return {
        **browser_context_args,
        **{
            key: value
            for key, value in [
                ("record_video_dir", video_path),
                ("record_video_size", get_resolution(request.config.getoption("--resolution")))
            ]
            if (request.config.getoption('--video') != 'off' or key == "http_credentials") and
               (not request.config.getoption('--device') or key != "record_video_size")
        }
    }


@pytest.fixture(scope="session")
def video_path(request):
    return request.config.getoption("--resource-path")


@pytest.fixture
def context(browser: Browser, browser_context_args: Dict, browser_name, video_path, request: SubRequest) \
        -> Generator[BrowserContext, None, None]:
    env = Env(request.config.getoption("--env"))
    storage_path = None
    context = None

    try:
        storage_path = hf.get_file_path('Authentication', f'{request.param.value}.json', env.value)
        data = storage_path
        if request.param:
            context = browser.new_context(storage_state=storage_path, **browser_context_args)
    except AttributeError:
        context = browser.new_context(**browser_context_args)
    current_failed_tests = request.session.testsfailed
    context.set_default_navigation_timeout(30000)
    context.set_default_timeout(20000)

    if request.config.getoption('--tracing') != 'off':
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    if storage_path:
        context.storage_state(path=storage_path)

    if request.config.getoption('--tracing') != 'off':
        trace_path = os.path.join(video_path, f'{request.config.getoption("--uuid")}_{request.node.name}.zip')
        context.tracing.stop(path=trace_path)
        if request.config.getoption('--tracing') not in ['on']:
            if request.session.testsfailed == current_failed_tests:
                # test should have been successful no real reason to keep it
                os.remove(trace_path)

    if request.config.getoption('--video') != 'off':
        current_video_name = context.current_video_name
        current_video_path = os.path.join(video_path, current_video_name)
        updated_video_path = os.path.join(video_path, f'{request.config.getoption("--uuid")}_{request.node.name}.webm')
        context.close()
        os.rename(current_video_path, updated_video_path)
        if request.config.getoption('--video') not in ['on']:
            if request.session.testsfailed == current_failed_tests:
                # test should have been successful no real reason to keep it
                os.remove(updated_video_path)
    else:
        context.close()


@pytest.fixture
def page(context: BrowserContext, base_url: str, request: SubRequest) -> Generator[Page, None, None]:
    page = context.new_page()
    page._goto = page.goto  # type: ignore
    page.goto = lambda *args, **kwargs: _handle_page_goto(  # type: ignore
        page, list(args), kwargs, base_url
    )

    yield page

    # save off the test unique id
    if request.config.getoption('--video') != 'off':
        current_path_name = os.path.split(context.pages[0].video.path())[1]
        BrowserContext.current_video_name = current_path_name
    page.close()


@pytest.fixture
def driver(page, request):
    try:
        page.goto("https://google.com", wait_until='networkidle')
    except TimeoutError:
        pass
    return Pages(page, request)

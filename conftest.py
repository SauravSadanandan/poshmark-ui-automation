import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help = "Choose environment: qa or prod"
        )
    
    parser.addoption(
        "--item",
        action="store",
        default="Nike Shoes",
        help = "Choose item to search for"
        )
    
    parser.addoption(
        "--filter_by",
        action="store",
        default="availability",
        help = "Choose filter category"
        )
    
    parser.addoption(
        "--filter_with",
        action="store",
        default="Available Items",
        help = "Choose filter within category"
        )
    
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": "other_scripts/posh_login.json",
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--disable-blink-features=AutomationControlled"]
    }

@pytest.fixture(scope="session")
def base_url(request):
    """Return the base URL based on the selected environment."""
    env_choice = request.config.getoption("--env")

    if env_choice == "qa":
        return "https://poshmark.com/feed"
    elif env_choice == "prod":
        return "https://poshmark.com/feed"
    else:
        raise ValueError(f"Unknown environment: {env_choice}")
    
    

@pytest.fixture(scope="session")
def search_item(request):
    """Choose item to search for."""
    return request.config.getoption("--item")


@pytest.fixture(scope="session")
def filter_category(request):
    """Choose filter category."""
    return request.config.getoption("--filter_by")

@pytest.fixture(scope="session")
def filter_option(request):
    """Choose filter within category."""
    return request.config.getoption("--filter_with")

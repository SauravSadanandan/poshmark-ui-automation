import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": ".auth/posh_login.json",
        "viewport": {"width": 1920, "height": 1080}
    }

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help = "Choose environment: qa or prod"
        )

@pytest.fixture(scope="session")
def base_url(request):
    env_choice = request.config.getoption("--env")

    if env_choice == "qa":
        return "https://poshmark.com/feed"
    elif env_choice == "prod":
        return "https://poshmark.com/feed"
    else:
        raise ValueError(f"Unknown environment: {env_choice}")
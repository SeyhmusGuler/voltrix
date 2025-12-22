import os

import pytest
from hypothesis import HealthCheck, Verbosity, settings

# Define Hypothesis profiles
settings.register_profile("ci", max_examples=50, deadline=None)
settings.register_profile("dev", max_examples=10, verbosity=Verbosity.verbose)
settings.register_profile(
    "debug", max_examples=10, verbosity=Verbosity.debug, suppress_health_check=[HealthCheck.too_slow]
)

# Load profile based on environment or default to dev (change to "ci" in CI envs)
# You can override this by setting the HYPOTHESIS_PROFILE_NAME env var
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE_NAME", "dev"))


@pytest.fixture(scope="session")
def hypothesis_settings():
    return settings()

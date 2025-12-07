import string

from hypothesis import given
from hypothesis import strategies as st
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Pydantic Models
# -----------------------------------------------------------------------------


class User(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    email: str
    age: int = Field(ge=18, le=120)
    is_active: bool = True


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

# Strategy to generate valid User data dictionaries
# Fix: Ensure username only contains ASCII alphanumeric + underscore to match regex
ascii_alphanum = string.ascii_letters + string.digits + "_"
user_strategy = st.fixed_dictionaries(
    {
        "id": st.integers(min_value=1),
        "username": st.text(alphabet=ascii_alphanum, min_size=3, max_size=20),
        "email": st.emails(),
        "age": st.integers(min_value=18, max_value=120),
        "is_active": st.booleans(),
    }
)


@given(data=user_strategy)
def test_user_model_instantiation(data):
    """
    Property: Valid strategy data should always create a valid Pydantic model.
    """
    user = User(**data)
    assert user.id == data["id"]
    assert user.username == data["username"]
    assert user.age == data["age"]


# We override the username strategy because Hypothesis inference for Pydantic 'pattern'
# might be incomplete or warn about it.
@given(st.builds(User, username=st.text(alphabet=ascii_alphanum, min_size=3, max_size=20)))
def test_pydantic_hypothesis_integration(user: User):
    """
    Using `st.builds(User)` automatically infers strategies from Pydantic fields!
    This is the "magic" way to do it.
    """
    assert isinstance(user, User)
    assert 18 <= user.age <= 120
    assert len(user.username) >= 3

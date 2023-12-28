# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

# strenum to allow for code backward-compat between Python 3.10 and Python 3.11+
from strenum import StrEnum


class Keyword(StrEnum):
    """
    Reserved keywords for the Streamlit app.

    - `DATA`: Streamlit variable holding the data :octicons-arrow-both-24: `"_DATA_"`

    """
    DATA             = "_DATA_"                 # noqa: E-221

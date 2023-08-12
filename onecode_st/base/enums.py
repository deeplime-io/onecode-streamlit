# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from enum import Enum


class Keyword(str, Enum):
    """
    Reserved keywords for the Streamlit app.

    - `DATA`: Streamlit variable holding the data :octicons-arrow-both-24: `"_DATA_"`

    """
    DATA             = "_DATA_"                 # noqa: E-221

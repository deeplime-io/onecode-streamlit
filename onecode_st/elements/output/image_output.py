# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..output_streamlit_element import OutputStreamlitElement


class ImageOutput(OutputStreamlitElement, onecode.ImageOutput):
    @staticmethod
    def streamlit() -> str:
        """
        Returns:
            The Streamlit code to show an image as part of the image carousel.

        !!! tip
            A static function `_show_img(filepath: str)` is available for any Streamlit code to use.
            It will automatically add the given image to the carousel without you needing to deal
            with the carousel.

        """
        return "_show_img(value)"

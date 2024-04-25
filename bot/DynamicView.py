from discord.ui import Button, View
from functools import partial
from discord import ButtonStyle


class DynamicView(View):
    """
    A dynamic view that allows for the addition of buttons with custom callbacks.
    """

    def __init__(self, view_id, logger, timeout=None):
        """
        Initializes the DynamicView with a specific view ID.

        :param view_id: A unique identifier for the view.
        """
        super().__init__(timeout=timeout)  # Disable timeout for persistence.
        self.view_id = view_id
        self.logger = logger

    async def on_timeout(self) -> None:
        self.logger.info(f"Timeout for view {self.view_id} reached.")

    def add_button(
        self, button_id, button_label, button_callback, style=ButtonStyle.secondary
    ):
        """
        Adds a button to the view with a specified callback.

        :param button_id: A unique identifier for the button within the view.
        :param button_label: The text label displayed on the button.
        :param button_callback: The callback function to be executed on click.
        :param style: The style of the button, defaults to ButtonStyle.secondary.
        """
        # Create a new Button instance with the provided parameters.
        button = Button(
            label=button_label,
            custom_id=f"{self.view_id}:button:{button_id}",
            style=style,
        )

        # Use functools.partial to pass additional arguments to the callback.
        button.callback = partial(button_callback, button=button)

        # Add the button to the view.
        self.add_item(button)

"""FedCm domain: Federated Credential Management.

This domain allows interacting with the FedCM dialog.

Types:

    ``LoginState`` — str. Whether this is a sign-up or sign-in action
    for this account, i.e. whether this account has ever been used to
    sign in to this RP before. Values: ``"SignIn"``, ``"SignUp"``.

    ``DialogType`` — str. The types of FedCM dialogs. Values:
    ``"AccountChooser"``, ``"AutoReauthn"``, ``"ConfirmIdpLogin"``,
    ``"Error"``.

    ``DialogButton`` — str. The buttons on the FedCM dialog. Values:
    ``"ConfirmIdpLoginContinue"``, ``"ErrorGotIt"``,
    ``"ErrorMoreDetails"``.

    ``AccountUrlType`` — str. The URLs that each account has. Values:
    ``"TermsOfService"``, ``"PrivacyPolicy"``.

    ``Account`` — dict. Corresponds to IdentityRequestAccount.
    Fields: ``accountId`` (str), ``email`` (str), ``name`` (str),
    ``givenName`` (str), ``pictureUrl`` (str), ``idpConfigUrl``
    (str), ``idpLoginUrl`` (str), ``loginState`` (LoginState),
    ``termsOfServiceUrl`` (str, optional), ``privacyPolicyUrl``
    (str, optional).

Events:

    ``FedCm.dialogShown`` — [no description]. Params: ``dialogId``
    (str), ``dialogType`` (DialogType), ``accounts`` (list[Account]),
    ``title`` (str), ``subtitle`` (str, optional).

    ``FedCm.dialogClosed`` — Triggered when a dialog is closed, either
    by user action, JS abort, or a command below. Params: ``dialogId``
    (str).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class FedCmDomain(BaseDomain):
    """Wrapper for the CDP FedCm domain.

    This domain allows interacting with the FedCM dialog.

    **Experimental domain.**

    Events:

    - ``dialogShown`` — [no description]. Params: ``dialogId`` (str),
      ``dialogType`` (DialogType), ``accounts`` (list[Account]),
      ``title`` (str), ``subtitle`` (str, optional).
    - ``dialogClosed`` — Triggered when a dialog is closed, either by
      user action, JS abort, or a command below. Params: ``dialogId``
      (str).
    """

    async def click_dialog_button(
        self,
        dialog_id: str,
        dialog_button: str,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            dialog_id: Dialog ID.
            dialog_button: Button type (``"ConfirmIdpLoginContinue"``,
                ``"ErrorGotIt"``, ``"ErrorMoreDetails"``).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``dialog_id`` or ``dialog_button`` is not
                a str.
        """
        if not isinstance(dialog_id, str):
            raise TypeError(
                f"dialog_id must be a str, got {type(dialog_id).__name__}"
            )
        if not isinstance(dialog_button, str):
            raise TypeError(
                f"dialog_button must be a str, "
                f"got {type(dialog_button).__name__}"
            )
        return await self._call(
            "FedCm.clickDialogButton",
            {"dialogId": dialog_id, "dialogButton": dialog_button},
        )

    async def disable(self) -> dict[str, Any]:
        """[no description].

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("FedCm.disable")

    async def dismiss_dialog(
        self,
        dialog_id: str,
        trigger_cooldown: bool = False,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            dialog_id: Dialog ID.
            trigger_cooldown: Whether to trigger a cooldown.
                Always sent (default ``False``).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``dialog_id`` is not a str or
                ``trigger_cooldown`` is not a bool.
        """
        if not isinstance(dialog_id, str):
            raise TypeError(
                f"dialog_id must be a str, got {type(dialog_id).__name__}"
            )
        if not isinstance(trigger_cooldown, bool):
            raise TypeError(
                f"trigger_cooldown must be a bool, "
                f"got {type(trigger_cooldown).__name__}"
            )
        return await self._call(
            "FedCm.dismissDialog",
            {"dialogId": dialog_id, "triggerCooldown": trigger_cooldown},
        )

    async def enable(
        self,
        disable_rejection_delay: bool = False,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            disable_rejection_delay: Allows callers to disable the
                promise rejection delay that would normally happen,
                if this is unimportant to what's being tested.
                Always sent (default ``False``).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``disable_rejection_delay`` is not a bool.
        """
        if not isinstance(disable_rejection_delay, bool):
            raise TypeError(
                f"disable_rejection_delay must be a bool, "
                f"got {type(disable_rejection_delay).__name__}"
            )
        return await self._call(
            "FedCm.enable",
            {"disableRejectionDelay": disable_rejection_delay},
        )

    async def open_url(
        self,
        dialog_id: str,
        account_index: int,
        account_url_type: str,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            dialog_id: Dialog ID.
            account_index: Index of the account to open the URL for.
            account_url_type: URL type (``"TermsOfService"``,
                ``"PrivacyPolicy"``).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``dialog_id`` is not a str,
                ``account_index`` is not an int, or
                ``account_url_type`` is not a str.
        """
        if not isinstance(dialog_id, str):
            raise TypeError(
                f"dialog_id must be a str, got {type(dialog_id).__name__}"
            )
        if not isinstance(account_index, int) or isinstance(
            account_index, bool
        ):
            raise TypeError(
                f"account_index must be an int, "
                f"got {type(account_index).__name__}"
            )
        if not isinstance(account_url_type, str):
            raise TypeError(
                f"account_url_type must be a str, "
                f"got {type(account_url_type).__name__}"
            )
        return await self._call(
            "FedCm.openUrl",
            {
                "dialogId": dialog_id,
                "accountIndex": account_index,
                "accountUrlType": account_url_type,
            },
        )

    async def reset_cooldown(self) -> dict[str, Any]:
        """Resets the cooldown time, if any, to allow the next FedCM
        call to show a dialog even if one was recently dismissed by
        the user.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("FedCm.resetCooldown")

    async def select_account(
        self,
        dialog_id: str,
        account_index: int,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            dialog_id: Dialog ID.
            account_index: Index of the account to select.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``dialog_id`` is not a str or
                ``account_index`` is not an int.
        """
        if not isinstance(dialog_id, str):
            raise TypeError(
                f"dialog_id must be a str, got {type(dialog_id).__name__}"
            )
        if not isinstance(account_index, int) or isinstance(
            account_index, bool
        ):
            raise TypeError(
                f"account_index must be an int, "
                f"got {type(account_index).__name__}"
            )
        return await self._call(
            "FedCm.selectAccount",
            {"dialogId": dialog_id, "accountIndex": account_index},
        )

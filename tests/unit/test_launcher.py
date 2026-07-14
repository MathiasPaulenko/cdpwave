

from cdpwave.browser.launcher import BrowserLauncher


class TestBrowserLauncherArgs:
    def test_build_args_includes_required_flags(self) -> None:
        launcher = BrowserLauncher(
            browser_path="/fake/chrome",
            port=9222,
            headless=True,
            user_data_dir="/tmp/profile",
        )
        args, port_socket = launcher._build_args()
        assert "/fake/chrome" in args
        assert "--remote-debugging-port=9222" in args
        assert "--user-data-dir=/tmp/profile" in args
        assert "--no-first-run" in args
        assert "--no-default-browser-check" in args
        assert "--disable-features=Translate" in args
        assert "--headless=new" in args
        assert "about:blank" in args
        assert port_socket is None

    def test_build_args_headless_false(self) -> None:
        launcher = BrowserLauncher(
            browser_path="/fake/chrome",
            port=9222,
            headless=False,
            user_data_dir="/tmp/profile",
        )
        args, _ = launcher._build_args()
        assert not any(a.startswith("--headless") for a in args)

    def test_build_args_extra_args(self) -> None:
        launcher = BrowserLauncher(
            browser_path="/fake/chrome",
            port=9222,
            headless=True,
            user_data_dir="/tmp/profile",
            extra_args=["--window-size=1920,1080", "--disable-gpu"],
        )
        args, _ = launcher._build_args()
        assert "--window-size=1920,1080" in args
        assert "--disable-gpu" in args

    def test_build_args_auto_port(self) -> None:
        launcher = BrowserLauncher(
            browser_path="/fake/chrome",
            port=0,
            headless=True,
            user_data_dir="/tmp/profile",
        )
        args, port_socket = launcher._build_args()
        port_flag = [a for a in args if a.startswith("--remote-debugging-port=")]
        assert len(port_flag) == 1
        port = int(port_flag[0].split("=")[1])
        assert port > 0
        assert port_socket is not None
        port_socket.close()

    def test_build_args_creates_temp_dir(self) -> None:
        launcher = BrowserLauncher(
            browser_path="/fake/chrome",
            port=9222,
            headless=True,
        )
        args, _ = launcher._build_args()
        user_data_flag = [a for a in args if a.startswith("--user-data-dir=")]
        assert len(user_data_flag) == 1
        import os

        assert os.path.isdir(user_data_flag[0].split("=")[1])


class TestBrowserLauncherLifecycle:
    def test_is_running_false_before_launch(self) -> None:
        launcher = BrowserLauncher(browser_path="/fake/chrome")
        assert launcher.is_running is False

    def test_info_none_before_launch(self) -> None:
        launcher = BrowserLauncher(browser_path="/fake/chrome")
        assert launcher.info is None

    async def test_close_without_launch_is_noop(self) -> None:
        launcher = BrowserLauncher(browser_path="/fake/chrome")
        await launcher.close()
        assert launcher.is_running is False

    async def test_close_is_idempotent(self) -> None:
        launcher = BrowserLauncher(browser_path="/fake/chrome")
        await launcher.close()
        await launcher.close()

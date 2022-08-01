from click import ClickException
from typing import Optional, IO, List
from kubeoven import log

class AppException(ClickException):

    hostname: str

    message = List[str]

    def __init__(self, *messages: str, hostname: str = "") -> None:
        super().__init__(",".join(messages))
        self.hostname = hostname
        self.messages = messages

    def show(self, _: Optional[IO] = None) -> None:
        for message in self.messages:
            log.error(message, self.hostname)

class CommandError(AppException):

    exit_code: int

    def __init__(self, exit_code: int, stderr: str) -> None:
        self.exit_code = exit_code
        super().__init__(*stderr.splitlines(), hostname="")


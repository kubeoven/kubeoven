import select
from socketserver import ThreadingTCPServer, BaseRequestHandler
import threading
from paramiko import SSHClient


SSH_PORT = 22
DEFAULT_PORT = 4000

g_verbose = False


class ForwardServer(ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            verbose(
                "Incoming request to %s:%d failed: %s"
                % (self.chain_host, self.chain_port, repr(e))
            )
            return
        if chan is None:
            verbose(
                "Incoming request to %s:%d was rejected by the SSH server."
                % (self.chain_host, self.chain_port)
            )
            return

        verbose(
            "Connected!  Tunnel open %r -> %r -> %r"
            % (
                self.request.getpeername(),
                chan.getpeername(),
                (self.chain_host, self.chain_port),
            )
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)
        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        verbose("Tunnel closed from %r" % (peername,))


def verbose(s):
    if g_verbose:
        print(s)

def forward(remote_host: str, remote_port: int, client: SSHClient) -> ThreadingTCPServer:
    class SubHander(Handler):
        chain_host = remote_host
        chain_port = remote_port
        ssh_transport = client.get_transport()
    server = ForwardServer(("", 0), SubHander)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server

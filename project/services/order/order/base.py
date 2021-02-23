import sys
import signal

from django.core.management.base import BaseCommand


class Signals(BaseCommand):

    def receive_signal(self, signal_number, frame):
        print(f'Received {signal_number}, lets shutdown')
        self.stdout.write(self.style.SUCCESS('Lets shutdown'))
        sys.exit()

    def signal_register(self):
        signal.signal(signal.SIGHUP, self.receive_signal)
        signal.signal(signal.SIGINT, self.receive_signal)
        signal.signal(signal.SIGQUIT, self.receive_signal)
        signal.signal(signal.SIGILL, self.receive_signal)
        signal.signal(signal.SIGTRAP, self.receive_signal)
        signal.signal(signal.SIGABRT, self.receive_signal)
        signal.signal(signal.SIGBUS, self.receive_signal)
        signal.signal(signal.SIGFPE, self.receive_signal)
        signal.signal(signal.SIGUSR1, self.receive_signal)
        signal.signal(signal.SIGSEGV, self.receive_signal)
        signal.signal(signal.SIGUSR2, self.receive_signal)
        signal.signal(signal.SIGPIPE, self.receive_signal)
        signal.signal(signal.SIGALRM, self.receive_signal)
        signal.signal(signal.SIGTERM, self.receive_signal)
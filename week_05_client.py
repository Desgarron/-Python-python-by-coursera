import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, address: str, port: int, timeout: int = None):
        self._address = address
        self._port = port
        self._timeout = timeout
        try:
            self._connection = socket.create_connection(
                    (self._address, self._port), timeout=self._timeout)
        except socket.error as err:
            raise ClientError(err)

    def _convert_response(self, response: str):
        pretty_dict = {}
        status_response, *data = [i for i in response.split(sep='\n') if i != '']

        for i in data:
            name, score, timestamp = i.split()
            pretty_dict.setdefault(name, []).append(tuple([int(timestamp), float(score)]))

        pretty_dict = {key: sorted(value, key=lambda x: x[0]) for key, value in pretty_dict.items()}
        return pretty_dict

    def get(self, metric_name: str) -> dict:
        structure = f'get {metric_name}\n'

        try:
            self._connection.sendall(structure.encode('utf-8'))
            response = self._connection.recv(1024)
            print('>>>>>>>>', response)
            if b'ok' not in response:
                raise ClientError

        except Exception:
            raise ClientError

        return self._convert_response(response.decode('utf-8'))

    def put(self, metric_name: str, score: float, timestamp: int = None) -> None:
        timestamp = timestamp or int(time.time())
        structure = f'put {metric_name} {score} {timestamp}\n'

        try:
            self._connection.sendall(structure.encode('utf-8'))
            response = self._connection.recv(1024)
            if b'ok' not in response:
                raise ClientError
        except Exception:
            raise ClientError


if __name__ == '__main__':
    obj = Client('127.0.0.1', 8888, timeout=20)
    print(obj.get('*'))

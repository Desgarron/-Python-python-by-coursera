import asyncio


class ClientServerProtocol(asyncio.Protocol):
    metric_storage = {}

    def connection_made(self, transport: asyncio.WriteTransport):
        self.transport = transport
        self.client_host, self.client_port = transport.get_extra_info('peername')
        print('transport => ', self.transport, '\n',
              'client_host = ', self.client_host, 'client_port = ', self.client_port)

    def data_received(self, data: bytearray):
        print('data_received -->>', data)
        resp = self.process_data(data)
        print('response -->>', resp, type(resp))
        self.transport.write(resp.encode())

    def process_data(self, request: bytearray):
        def _get_procces(metric):
            if len(metric.split()) == 1:
                metric = metric.strip()
                if metric == '*':
                    return 'ok\n' + '\n'.join(
                        [' '.join([k, *value])
                         for k, values in self.metric_storage.items()
                         for value in values]
                    ) + '\n\n'
                if metric in self.metric_storage:
                    return 'ok\n' + '\n'.join(
                        [' '.join([k, *value])
                         for k, values in self.metric_storage.items()
                         for value in values if k == metric]
                    ) + '\n\n'
                return ok_command
            else:
                return wrong_command

        def _put_procces(metric_name, metric_score, timestamp):
            for i, metric in enumerate(self.metric_storage.get(metric_name, '')):
                # print('sad', self.metric_storage[metric_name][i])
                to_delete = self.metric_storage[metric_name]
                if to_delete[i][1] == timestamp:
                    to_delete.remove((to_delete[i][0], timestamp))

            self.metric_storage.setdefault(metric_name, []).append((metric_score, timestamp))
            return ok_command

        wrong_command = 'error\nwrong command\n\n'
        ok_command = 'ok\n\n'
        data = request.decode().split(maxsplit=1)
        print('process_data >>>', data, type(data))

        if data[0] not in ('get', 'put'):
            return wrong_command
        if data[0] == 'get':
            return _get_procces(data[1])
        if data[0] == 'put':
            data = data[1].split()
            return _put_procces(data[0], data[1], data[2])


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    print('START Server ->')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server("127.0.0.1", 8181)

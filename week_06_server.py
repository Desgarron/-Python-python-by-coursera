import asyncio


class ClientServerProtocol(asyncio.Protocol):
    metric_storage = {}

    def connection_made(self, transport: asyncio.WriteTransport):
        self.transport = transport
        print('transport => ', self.transport, type(self.transport), '\n')

    def data_received(self, data: bytearray):
        print('data_received =>', type(data), data, '\n')
        resp = self.process_data(data)
        print('response -->>', resp, type(resp))
        self.transport.write(resp.encode())

    def process_data(self, request: bytearray):

        def _get_proccess(metric):
            print('_get_proccess -> ', metric)
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
            return 'ok\n\n'

        def _put_proccess(metric_name, metric_score, timestamp):
            for i in range(len(self.metric_storage.get(metric_name, ''))):
                print('sad', self.metric_storage[metric_name][i])
                if self.metric_storage[metric_name][i][1] == timestamp:
                    del self.metric_storage[metric_name][i]
            self.metric_storage.setdefault(metric_name, []).append((metric_score, timestamp))
            return 'ok\n\n'

        print('just for check dict ->', self.metric_storage)
        data = request.decode().split(maxsplit=1)
        print('process_data >>>', data, type(data))

        if data[0] not in ('get', 'put'):
            return 'error\nwrong command\n\n'
        if data[0] == 'get':
            return _get_proccess(data[1])
        if data[0] == 'put':
            data = data[1].split()
            return _put_proccess(data[0], data[1], data[2])



loop = asyncio.get_event_loop()
print('1')
coro = loop.create_server(ClientServerProtocol, "127.0.0.1", 8181)
print('2')
server = loop.run_until_complete(coro)
print('3')

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()



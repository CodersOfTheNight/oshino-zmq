import zmq

from zmq.asyncio import Context

from oshino import Agent


class ZmqAgent(Agent):

    @property
    def bind(self):
        return self._data.get("bind", None)

    @property
    def connect(self):
        return self._data["connect"]

    def parse_logentry(self, json_obj):
        return {"metric": 1,
                "tags": "log",
                "attributes": json_obj}

    async def process(self, event_fn):
        logger = self.get_logger()
        if self.socket_active:
            try:
                logger.trace("Trying to read msg")
                if self.socket in dict(events):
                    json_obj = await self.socket.recv_json(zmq.NOBLOCK)
                    logger.trace("Received msg: '{0}'".format(json_obj))
                    log_obj = self.parse_logentry(json_obj)
                    event_fn(service=self.prefix, **log_obj)
            except:
                logger.trace("No message received")
        else:
            logger.debug("Zmq socket is still waiting for connection")

    def on_start(self):
        logger = self.get_logger()
        logger.info("Initializing zMQ context")
        self.ctx = Context()
        self.socket = self.ctx.socket(zmq.PULL)
        if self.bind:
            self.socket.bind(self.bind)
            logger.info("Zmq socket bound on: {0}".format(self.bind))
            self.socket_active = True
        else:
            self.socket.connect(self.connect)
            logger.info("Zmq socket connected to: {0}".format(self.connect))
            self.socket_active = True

    def on_stop(self):
        self.socket.close()

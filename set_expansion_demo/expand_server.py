import logging
import socketserver
import argparse
import pickle
from set_expansion_demo import set_expand


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("handling expand request")
        self.data = str(self.request.recv(10240).strip(), 'utf-8')
        logger.debug('request data: ' + self.data)
        data = [x.strip() for x in self.data.split(',')]
        seeds = data
        res = se.expand(seeds)
        packet = pickle.dumps(res)
        # length = struct.pack('!I', len(packet))
        # packet = length + packet
        self.request.sendall(packet)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='expand_server.py')
    parser.add_argument('port', metavar='port', type=int,
                        help='set port for the server')
    parser.add_argument('model_path', metavar='model_path', type=str,
                        help='a path to the w2v model file')
    args = parser.parse_args()

    port = args.port
    model_path = args.model_path
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    logger = logging.getLogger("set_expantion_demo")
    # initialize the model:
    se = set_expand.SetExpand(model_path)
    logger.debug("loading server\n")
    HOST, PORT = "localhost", port
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    logger.debug("server loaded\n")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

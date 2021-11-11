import gc
import os

from route_guide_pb2_grpc import RouteGuideStub
from route_guide_pb2 import Point

from gevent import monkey
import grpc.experimental.gevent
import grpc
from gevent import sleep

monkey.patch_all()
grpc.experimental.gevent.init_gevent()

def count_fds():
    base = '/proc/self/fd'
    return len(os.listdir(base))

grpc_options = [
    # retry faster on tcp connect fail -> make the leak occur faster
    ("grpc.min_reconnect_backoff_ms", 100),
    ("grpc.initial_reconnect_backoff_ms", 200),
    ("grpc.max_reconnect_backoff_ms", 300),
    ("grpc.lb_policy_name", "round_robin"),
]
target = "server:5000"
channel = grpc.insecure_channel(target, options=grpc_options)
stub = RouteGuideStub(channel)
res = stub.GetFeature(Point(latitude=409146138, longitude=-746188906))
print("COUCOU")
print(res)

while True:
    num_socket_wrapper = 0
    num_sockets = 0
    num_fd = 0
    for obj in gc.get_objects():
        if not hasattr(obj, "__class__"):
            continue
        if str(obj.__class__) == "<class 'grpc._cython.cygrpc.SocketWrapper'>":
            num_socket_wrapper += 1
            continue
        if str(obj.__class__) == "<class 'gevent._socket3.socket'>":
            num_sockets += 1
            continue
    print("Found: {} objects of class SocketWrapper, {} sockets and {} file descriptors".format(num_socket_wrapper, num_sockets, count_fds()))
    sleep(1)
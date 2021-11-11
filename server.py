from concurrent import futures

import route_guide_pb2
import route_guide_pb2_grpc

import grpc

class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    def GetFeature(self, request, context):
        return route_guide_pb2.Feature(name="", location=request)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()

serve()
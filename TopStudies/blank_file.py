import grpc
import tritonclient.grpc as grpcclient

url = "triton.fnal.gov:443"
ssl_options = grpc.ssl_channel_credentials()

# Create a GRPC client
client = grpcclient.InferenceServerClient(url=url, ssl=True)

# Example usage: check if the server is live
if client.is_server_live():
    print("Server is live!")

client.close()
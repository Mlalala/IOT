from knxnet import *
import socket, sys

gateway_ip = "127.0.0.1"
gateway_port = 3671

def command(ip_source, ip_dest, port_cli, port_gate) :
  data_endpoint = (ip_dest, port_cli) #"Connection_Request","Connection_State_Request","Disconnect_Request","Connection_Response","Connection_State_Response","Disconnect_Response"
  control_endpoint = (ip_dest, port_cli) #"TunnelingRequest" and "Tunneling Ack"

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((ip_dest, port_cli)) #port ?

  # -> Connection Resquest
  conn_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,control_endpoint,data_endpoint)
  conn_req_dtgrm = conn_req_object.frame
  sock.sendto (conn_req_dtgrm, (ip_source, port_gate))

  # <- Receiving Connection Response
  data_recv, addr = sock.recvfrom(1024)
  conn_resp_object = knxnet.decode_frame(data_recv)
  
  conn_channel_id = conn_resp_object.channel_id

  # -> Connection State Request
  conn_req_stat_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,conn_channel_id,control_endpoint)
  conn_req_stat_dtgrm = conn_req_stat_object.frame
  sock.sendto (conn_req_stat_dtgrm, (ip_source, port_gate))

  # <- Connection State Response
  data_recv, addr = sock.recvfrom(1024)
  conn_resp_stat_object = knxnet.decode_frame(data_recv)
  

  print(conn_req_object)
  print(conn_resp_object)
  print(conn_req_stat_object)
  print(conn_resp_stat_object)



command(gateway_ip,"127.0.0.1",3672,gateway_port)

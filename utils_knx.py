from knxnet import *
import socket, sys

def write(ip_source, ip_dest, port_cli, port_gate, dest_addr_group,data, data_size) :
  # /!\ ports can be different
  data_endpoint = (ip_source, port_cli) #"Connection_Request","Connection_State_Request","Disconnect_Request","Connection_Response","Connection_State_Response","Disconnect_Response"
  control_endpoint = (ip_source, port_cli) #"TunnelingRequest" and "Tunneling Ack"

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((ip_source, port_cli))

  # -> Connection Resquest
  conn_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,control_endpoint,data_endpoint)
  conn_req_dtgrm = conn_req_object.frame
  sock.sendto (conn_req_dtgrm, (ip_dest, port_gate))

  # <- Receiving Connection Response
  data_recv, addr = sock.recvfrom(1024)
  conn_resp_object = knxnet.decode_frame(data_recv)
  
  conn_channel_id = conn_resp_object.channel_id

  # -> Connection State Request
  conn_req_stat_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,conn_channel_id,control_endpoint)
  conn_req_stat_dtgrm = conn_req_stat_object.frame
  sock.sendto (conn_req_stat_dtgrm, (ip_dest, port_gate))

  # <- Connection State Response
  data_recv, addr = sock.recvfrom(1024)
  conn_resp_stat_object = knxnet.decode_frame(data_recv)
  conn_status = conn_resp_stat_object.status

  # -> Tunnelling Request
  tunn_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,dest_addr_group,conn_channel_id,data,data_size)
  tunn_req_dtgrm = tunn_req_object.frame
  sock.sendto (tunn_req_dtgrm, (ip_dest, port_gate))

  # <- Tunnelling Ack
  data_recv, addr = sock.recvfrom(1024)
  tunn_resp_object = knxnet.decode_frame(data_recv)
  
  # -> Disconnect Request
  dis_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,conn_channel_id,control_endpoint)
  dis_req_dtgrm = tunn_req_object.frame
  sock.sendto (dis_req_dtgrm, (ip_dest, port_gate))

  # <- Disconnect Response
  data_recv, addr = sock.recvfrom(1024)
  dis_resp_object = knxnet.decode_frame(data_recv)
  #dis_status = conn_resp_stat_object.status


  #debug
  print("###conn_req_object\n",conn_req_object)
  print("###conn_resp_object\n",conn_resp_object)
  print("###conn_req_stat_object\n",conn_req_stat_object)
  print("###conn_resp_stat_object\n",conn_resp_stat_object)
  print("###tunn_req_objectn\n",tunn_req_object)
  print("###tunn_resp_object\n",tunn_resp_object)
  print("###dis_req_object\n",dis_req_object)
  print("###dis_resp_object\n",dis_resp_object)

def read():
  #read func
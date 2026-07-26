from socket import *
import sys, os
if len(sys.argv) <= 1:
    print('usage: "python proxyserver.py server_ip"')
    sys.exit(2)
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind((sys.argv[1], 8888))
serversocket.listen(4)
cache = {}  # key: "host/path" -> local cache filename
def recv_headers(sock):
    """Read until end of headers (\r\n\r\n), return raw bytes."""
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data
def parse_request(raw):
    header_part, _, rest = raw.partition(b"\r\n\r\n")
    lines = header_part.decode(errors="replace").split("\r\n")
    method, path, _ = lines[0].split()
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    return method, path, headers, rest  # rest = any body bytes already read
def recv_full_body(sock, already_read, content_length):
    body = already_read
    while len(body) < content_length:
        chunk = sock.recv(1024)
        if not chunk:
            break
        body += chunk
    return body
while True:
    print('Ready to serve...')
    connectionsocket, addr = serversocket.accept()
    print('Received a connection from:', addr)
    raw = recv_headers(connectionsocket)
    if not raw:
        connectionsocket.close()
        continue
    method, path, headers, rest = parse_request(raw)
    filename = path.partition("/")[2]
    print(method, filename)
    host = filename.replace("www.", "", 1).split("/")[0]
    cache_key = filename
    body = b""
    if method == "POST":
        content_length = int(headers.get("content-length", 0))
        body = recv_full_body(connectionsocket, rest, content_length)
    # --- GET: serve from cache if we have it ---
    if method == "GET" and cache_key in cache and os.path.exists(cache[cache_key]):
        print("Serving from cache:", cache[cache_key])
        with open(cache[cache_key], "rb") as f:
            outputdata = f.readlines()
        connectionsocket.send(b"HTTP/1.1 200 OK\r\n")
        connectionsocket.send(b"Content-Type: text/html\r\n\r\n")
        for line in outputdata:
            connectionsocket.send(line)
        connectionsocket.close()
        continue
    # --- Cache miss (GET) or POST: contact origin server ---
    try:
        a = socket(AF_INET, SOCK_STREAM)
        a.connect((host, 80))
        if method == "POST":
            req = (
                f"POST / HTTP/1.0\r\nHost: {host}\r\n"
                f"Content-Length: {len(body)}\r\n\r\n"
            ).encode() + body
        else:
            req = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode()
        a.send(req)
        bufferdata = a.recv(1024)
        tmp_path = "./" + cache_key.replace("/", "_")  # flatten path for filesystem safety
        tmpFile = open(tmp_path, "wb") if method == "GET" else None
        while bufferdata:
            if tmpFile:
                tmpFile.write(bufferdata)
            connectionsocket.send(bufferdata)
            bufferdata = a.recv(1024)
        if tmpFile:
            tmpFile.close()
            cache[cache_key] = tmp_path  # only GET responses get cached
        a.close()
    except Exception as e:
        print('404 not found', e)
        connectionsocket.send(b"HTTP/1.1 404 Not found\r\nContent-type: text/html\r\n\r\n")
        connectionsocket.send(b"<html><body><h1>404 not found</h1></body></html>")
    connectionsocket.close()
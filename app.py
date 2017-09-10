# --*-- coding=utf-8 --*--
import urllib     
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  
  
#自定义处理程序，用于处理HTTP请求 
class TestHTTPHandler(BaseHTTPRequestHandler):  
    #处理GET请求  
    def do_GET(self):  
        #页面输出模板字符串  
        templateStr = '''   
<html>   
<head>   
<title>first site</title>   
</head>   
<body>   
Hello  
</body>   
</html>
'''  
        self.protocal_version = 'HTTP/1.1'  #设置协议版本  
        self.send_response(200) #设置响应状态码  
        self.send_header("Welcome", "Contect")  #设置响应头  
        self.end_headers()  
        self.wfile.write(templateStr)   #输出响应内容  
          
    #启动服务函数  
def start_server(port):  
    http_server = HTTPServer(('', int(port)), TestHTTPHandler)  
    http_server.serve_forever() #设置一直监听并接收请求  
  
start_server(8080)  #启动服务，监听8080端口  

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict
from urllib.parse import urlparse, parse_qs
import requests

logger = logging.getLogger(__name__)


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        url = query_components.get("url", [None])[0]

        if url:
            try:
                headers = {
                    'User-Agent': user_agents['chrome'],
                    'Origin': get_origin_from_url(url)
                }
                # Make the external GET request
                response = requests.get(url, headers=headers)

                # Send response status code
                self.send_response(response.status_code)
                # Send headers
                self.send_header('Content-Type', response.headers['Content-Type'])
                self.end_headers()
                # Relay the content
                self.wfile.write(response.content)

            except Exception as e:
                self.send_error(500, f"Internal Server Error: {e}")
        else:
            self.send_error(400, "Bad Request: No URL provided")


def get_origin_from_url(url):
    """
    Get origin from the passed in url
    """
    parsed_url = urlparse(url)
    # The origin is scheme + hostname + port (if port is specified)
    origin = f"{parsed_url.scheme}://{parsed_url.hostname}"
    if parsed_url.port:
        origin += f":{parsed_url.port}"
    return origin


def load_json_to_dict(file_path: str) -> Dict[str, str]:
    """ Loads a json file into a dictionary"""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."
    except Exception as e:
        return f"An error occurred: {e}"


# load the static data sets into the global scope
user_agents: Dict[str, str] = load_json_to_dict(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'user-agents.json'))


def run(server_class=ThreadingHTTPServer, handler_class=ProxyHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

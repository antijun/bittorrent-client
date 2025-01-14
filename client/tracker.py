import requests
import hashlib 
import bencodepy
import urllib.parse
import random

class Tracker:
    def __init__(self, torrent):
        self.tracker_url = torrent.torrent_file[b'announce'].decode()
        self.info_hash = torrent.info_hash
        self.peer_id = self.generate_peer_id()
        self.port = 6881
        self.uploaded = 0
        self.downloaded = 0
        self.left = torrent.length
        self.compact = 1

        print(f"Tracker URL: {self.tracker_url}")
        print(f"Info Hash (Hex): {self.info_hash.hex()}")
        print(f"Peer ID: {self.peer_id}")
        print(f"Port: {self.port}")
        print(f"Uploaded: {self.uploaded}")
        print(f"Downloaded: {self.downloaded}")
        print(f"Left: {self.left}")
        print(f"Compact: {self.compact}")

    def generate_peer_id(self):
        return '-PC0001-' + ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(12))
    
    def announce(self, event="started"):
        
        params = {
            'info_hash': self.info_hash,
            'peer_id': self.peer_id,
            'port': self.port,
            'uploaded': self.uploaded,
            'downloaded': self.downloaded,
            'left': self.left,
            'compact': self.compact,
            'event': event
        }

        url = f"{self.tracker_url}?{urllib.parse.urlencode(params)}"
        print(f"Announce URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if 'bencoded' not in response.headers.get('Content-Type', ''):
                print("Unexpected response type from tracker")
                return None
            return response.content
        except requests.RequestException as e:
            print(f"Tracker request failed: {e}")
            return None

    
    def parse_response(self, response):
        try:
            decoded = bencodepy.decode(response)
            print(f"Decoded Tracker Response: {decoded}")
            return decoded
        except bencodepy.BencodeDecodeError as e:
            print(f"Error decoding bencoded response: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def extract_peers(self, decoded_response):
        try:
            peers = decoded_response[b'peers']
            if isinstance(peers, bytes):
                peer_list = [
                    {
                        "ip": ".".join(map(str, peers[i:i+4])),
                        "port": int.from_bytes(peers[i+4:i+6], "big")
                    }
                    for i in range(0, len(peers), 6)
                ]
                print(f"Extracted Peers: {peer_list}")
                return peer_list
            else:
                print(f"Peers in non-compact mode: {peers}")
                return peers
        except KeyError:
            print("No peers found in response")
            return []
        except Exception as e:
            print(f"Error parsing peers: {e}")
            return []

import bencodepy
import hashlib
import os

class Torrent(object):
    def __init__(self, file_path):
        self.file_path = file_path  # path to the .torrent file
        self.torrent_file = {}      # parsed .torrent file
        self.info_hash = b''        # hash of the info dictionary
        self.length = 0             # total length of file(s) 
        self.piece_length = 0       # length of each piece
        self.pieces = []            # list of hashes of each piece
        self.file_name = ''         # name of the file/directory
        self.files = []             # list of files/directories
        
        self.load_file()
        
    # loads the .torrent file
    def load_file(self):
        try:
            with open(self.file_path, 'rb') as f:
                self.torrent_file = bencodepy.decode(f.read())
                self.extract_metadata()
        except Exception as e:
            print(f'Error loading .torrent file: {e}')
            
    # extracts metadata from the .torrent file
    def extract_metadata(self):
        try:
            info = self.torrent_file[b'info']
            
            # calculate info hash
            self.info_hash = hashlib.sha1(bencodepy.encode(info)).digest()
            
            # extract piece length and pieces
            self.piece_length = info[b'piece length']
            self.pieces = [info[b'pieces'][i:i+20] for i in range(0, len(info[b'pieces']), 20)] 
            
            # check single or multiple files
            if b'length' in info:
                # single file
                self.length = info[b'length']
                self.file_name = info[b'name'].decode()
            else:
                # multiple files
                self.file_name = ', '.join([os.path.join(*[p.decode() for p in file[b'path']]) for file in info[b'files']])
                self.files = [
                    {
                        'length': file[b'length'],
                        'path': os.path.join(*[p.decode() for p in file[b'path']])
                    } for file in info[b'files']
                ]
                self.length = sum([file['length'] for file in self.files])
                
        except KeyError as e:
            print(f'Key missing in .torrent file: {e}')
        except Exception as e:
            print(f'Error extracting metadata: {e}')
            
        
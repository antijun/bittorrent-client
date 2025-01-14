from torrent_parser import Torrent
from tracker import Tracker

def main():
    # Testing torrent parser and tracker
    try:
        # Load .torrent file
        torrent_file = 'Mushoku Tensei - Jobless Reincarnation - Recollections {Cliff Kurt}.torrent'
        torrent = Torrent(torrent_file)
        
        # Extract metadata
        torrent.extract_metadata()
        print("\nTorrent Metadata Parsed Successfully!")
        print(f"Info Hash (Hex): {torrent.info_hash.hex()}")
        print(f"Total Length: {torrent.length}")
        print(f"Piece Length: {torrent.piece_length}")
        print(f"Number of Pieces: {len(torrent.pieces)}")
        print(f"File Name: {getattr(torrent, 'file_name', 'N/A')}")  # Single file
        if hasattr(torrent, 'files'):
            print("Files:")
            for file in torrent.files:
                print(f"  Path: {file['path']}, Length: {file['length']}")
        
        # Initialize Tracker
        tracker = Tracker(torrent)
        print("\nTracker Initialized:")
        print(f"Tracker URL: {tracker.tracker_url}")
        print(f"Peer ID: {tracker.peer_id}")
        print(f"Port: {tracker.port}")
        print(f"Uploaded: {tracker.uploaded}")
        print(f"Downloaded: {tracker.downloaded}")
        print(f"Left: {tracker.left}")
        print(f"Compact: {tracker.compact}")

        # Announce to the tracker
        print("\nSending Announce Request to Tracker...")
        response = tracker.announce(event="started")

        if response:
            print("\nTracker Response Received:")
            decoded_response = tracker.parse_response(response)
            if decoded_response:
                print(f"Decoded Tracker Response: {decoded_response}")
            else:
                print("Failed to decode tracker response.")
        else:
            print("No response from tracker.")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

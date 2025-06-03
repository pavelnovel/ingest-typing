"""
Lightweight Typing Activity Tracker
Captures typing sessions and saves them as JSON files with human-readable timestamps
"""

import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

try:
    from pynput import keyboard
    PLATFORM_SUPPORTED = True
except ImportError:
    print("ERROR: pynput not installed. Run: pip install pynput")
    PLATFORM_SUPPORTED = False


class TypingTracker:
    """Minimal typing activity tracker with session detection"""
    
    def __init__(self, output_dir: str = "/Users/pk/Desktop/content/typing-output"):
        self.output_dir = output_dir
        self.is_running = False
        self.current_session = None
        self.last_activity = None
        self.keyboard_listener = None
        self.session_gap_seconds = 5  # Add paragraph break after 5 seconds of inactivity
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    def start_tracking(self) -> bool:
        """Start tracking typing activity"""
        if not PLATFORM_SUPPORTED:
            print("Platform not supported - install pynput package")
            return False
            
        self.is_running = True
        print(f"🔥 Typing tracker started - saving to: {self.output_dir}")
        print("💡 Press Ctrl+C to stop and save")
        
        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.keyboard_listener.start()
        
        # Initialize first session
        self._start_new_session(datetime.now())
        
        return True
    
    def _on_key_press(self, key):
        """Capture keystroke and manage sessions"""
        try:
            timestamp = datetime.now()
            
            # Handle different key types
            if hasattr(key, 'char') and key.char:
                char = key.char
                key_type = 'character'
            else:
                char = str(key).replace('Key.', '')
                key_type = 'special'
            
            # Check if we need to add a paragraph break (5+ seconds gap)
            if (self.last_activity and 
                (timestamp - self.last_activity).total_seconds() > self.session_gap_seconds):
                # Add paragraph break
                self.current_session['content'] += '\n\n'
            
            # Add keystroke to current session
            if key_type == 'character':
                if char in ['\r', '\n']:
                    self.current_session['content'] += '\n'
                elif char == '\t':
                    self.current_session['content'] += '\t'
                else:
                    self.current_session['content'] += char
                    
                self.current_session['character_count'] += 1
                
            elif char == 'space':
                self.current_session['content'] += ' '
                self.current_session['character_count'] += 1
                
            elif char == 'backspace' and self.current_session['content']:
                self.current_session['content'] = self.current_session['content'][:-1]
                self.current_session['character_count'] = max(0, self.current_session['character_count'] - 1)
            
            # Update session metrics
            self.current_session['last_activity'] = timestamp.isoformat()
            self.current_session['total_keystrokes'] += 1
            self.last_activity = timestamp
            
        except Exception as e:
            print(f"Error capturing keystroke: {e}")
    
    def _on_key_release(self, key):
        """Handle key release (minimal processing)"""
        self.last_activity = datetime.now()
    
    def _start_new_session(self, timestamp: datetime):
        """Initialize a new typing session"""
        self.current_session = {
            'session_start': timestamp.isoformat(),
            'session_end': None,
            'content': '',
            'character_count': 0,
            'word_count': 0,
            'total_keystrokes': 0,
            'duration_seconds': 0,
            'last_activity': timestamp.isoformat()
        }
    
    def _save_session(self):
        """Save the current session and add to daily log"""
        if not self.current_session or self.current_session['character_count'] == 0:
            return
            
        # Finalize session
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.current_session['session_start'])
        
        self.current_session['session_end'] = end_time.isoformat()
        self.current_session['duration_seconds'] = (end_time - start_time).total_seconds()
        self.current_session['word_count'] = len(self.current_session['content'].split())
        
        # Create human-readable filename
        date_str = start_time.strftime("%Y-%m-%d")
        time_str = start_time.strftime("%I-%M%p").lower()
        filename = f"{date_str}_Typing_Session_{time_str}.json"
        
        # Load or create daily log
        daily_filename = f"{date_str}_Daily_Typing_Log.json"
        daily_filepath = os.path.join(self.output_dir, daily_filename)
        
        daily_log = self._load_daily_log(daily_filepath)
        
        # Add session to daily log
        daily_log['sessions'].append(dict(self.current_session))
        daily_log['total_sessions'] += 1
        daily_log['total_characters'] += self.current_session['character_count']
        daily_log['total_words'] += self.current_session['word_count']
        daily_log['total_keystrokes'] += self.current_session['total_keystrokes']
        daily_log['last_updated'] = datetime.now().isoformat()
        
        # Save updated daily log
        with open(daily_filepath, 'w') as f:
            json.dump(daily_log, f, indent=2)
        
        print(f"💾 Session saved: {self.current_session['character_count']} chars, {self.current_session['word_count']} words")
    
    def _load_daily_log(self, filepath: str) -> Dict:
        """Load existing daily log or create new one"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Create new daily log structure
        date_str = os.path.basename(filepath).split('_')[0]
        return {
            'date': date_str,
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_sessions': 0,
            'total_characters': 0,
            'total_words': 0,
            'total_keystrokes': 0,
            'sessions': []
        }
    
    def stop_tracking(self):
        """Stop tracking and save final session"""
        if not self.is_running:
            return
            
        self.is_running = False
        
        # Save current session
        if self.current_session:
            self._save_session()
        
        # Stop keyboard listener
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        print("\n🛑 Typing tracker stopped")
        print(f"📁 Output saved to: {self.output_dir}")


def main():
    """Main entry point"""
    tracker = TypingTracker()
    
    if not tracker.start_tracking():
        return
    
    try:
        # Keep running until interrupted
        while tracker.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔄 Shutting down gracefully...")
    finally:
        tracker.stop_tracking()


if __name__ == "__main__":
    main()
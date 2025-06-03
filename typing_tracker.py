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
    """Minimal typing activity tracker with continuous session"""
    
    def __init__(self, output_dir: str = "/Users/pk/Desktop/content/typing-output"):
        self.output_dir = output_dir
        self.is_running = False
        self.current_session = None
        self.last_activity = None
        self.keyboard_listener = None
        self.session_gap_seconds = 5  # Add paragraph break after 5 seconds of inactivity
        self.session_filename = None  # Store the single session filename
        
        # WPM tracking
        self.word_timestamps = []  # Store (timestamp, word_count) for WPM calculation
        self.last_stats_display = None
        self.stats_display_interval = 5 # Show stats every 5 seconds
        
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
        
        # Initialize the continuous session (will create file on first keystroke)
        self._initialize_session(datetime.now())
        
        # Start background stats display
        import threading
        stats_thread = threading.Thread(target=self._stats_display_loop, daemon=True)
        stats_thread.start()
        
        return True
    
    def _on_key_press(self, key):
        """Capture keystroke and manage continuous session"""
        try:
            timestamp = datetime.now()
            
            # Create session file on first keystroke
            if not self.session_filename:
                self._create_session_file(timestamp)
            
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
                # Add paragraph break for long gap
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
            
            # Track words for WPM calculation (on space or newline)
            if key_type == 'character' and char in [' ', '\r', '\n'] or char == 'space':
                current_word_count = len(self.current_session['content'].split())
                self.word_timestamps.append((timestamp, current_word_count))
                
                # Keep only last 1 minute of data
                cutoff_time = timestamp.timestamp() - 60  # 1 minute ago
                self.word_timestamps = [
                    (ts, wc) for ts, wc in self.word_timestamps 
                    if ts.timestamp() > cutoff_time
                ]
            
        except Exception as e:
            print(f"Error capturing keystroke: {e}")
    
    def _on_key_release(self, key):
        """Handle key release (minimal processing)"""
        self.last_activity = datetime.now()
    
    def _initialize_session(self, timestamp: datetime):
        """Initialize the continuous session structure"""
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
    
    def _create_session_file(self, timestamp: datetime):
        """Create the session file when first keystroke is detected"""
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%I-%M%p").lower()
        self.session_filename = f"{date_str}_Typing_Session_{time_str}.json"
        session_filepath = os.path.join(self.output_dir, self.session_filename)
        
        print(f"📝 Session started: {self.session_filename}")
        
        # Save initial session file
        with open(session_filepath, 'w') as f:
            json.dump(self.current_session, f, indent=2)
    
    def _calculate_wpm_last_1min(self) -> float:
        """Calculate WPM for the last 1 minute"""
        if len(self.word_timestamps) < 2:
            return 0.0
        
        # Get time span and word count for last 1 minute
        now = datetime.now()
        cutoff_time = now.timestamp() - 60  # 1 minute ago
        
        # Filter to last 1 minute
        recent_words = [
            (ts, wc) for ts, wc in self.word_timestamps 
            if ts.timestamp() > cutoff_time
        ]
        
        if len(recent_words) < 2:
            return 0.0
        
        # Calculate words and time span
        first_timestamp, first_word_count = recent_words[0]
        last_timestamp, last_word_count = recent_words[-1]
        
        words_typed = last_word_count - first_word_count
        time_span_minutes = (last_timestamp.timestamp() - first_timestamp.timestamp()) / 60
        
        if time_span_minutes <= 0:
            return 0.0
        
        return words_typed / time_span_minutes
    
    def _stats_display_loop(self):
        """Background thread to display typing stats"""
        while self.is_running:
            try:
                time.sleep(self.stats_display_interval)
                
                if self.current_session and self.session_filename:
                    current_words = len(self.current_session['content'].split())
                    wpm_1min = self._calculate_wpm_last_1min()
                    
                    print(f"📊 Words: {current_words} | WPM (1min): {wpm_1min:.1f}")
                    
            except Exception as e:
                print(f"Error in stats display: {e}")
                time.sleep(10)
    
    def _save_session(self):
        """Save the final session when stopping"""
        if not self.current_session or not self.session_filename:
            return
            
        # Finalize session
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.current_session['session_start'])
        
        self.current_session['session_end'] = end_time.isoformat()
        self.current_session['duration_seconds'] = (end_time - start_time).total_seconds()
        self.current_session['word_count'] = len(self.current_session['content'].split())
        
        # Save final session file
        session_filepath = os.path.join(self.output_dir, self.session_filename)
        with open(session_filepath, 'w') as f:
            json.dump(self.current_session, f, indent=2)
        
        print(f"💾 Session saved: {self.current_session['character_count']} chars, {self.current_session['word_count']} words")
        print(f"📁 File: {self.session_filename}")
    
    
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
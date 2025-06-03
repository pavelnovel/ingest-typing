# Typing Activity Tracker

A lightweight, privacy-focused typing activity tracker that captures your typing sessions and saves them as organized JSON files with human-readable timestamps.

## 🎯 What It Does

- **Captures typing activity** across all applications on your computer
- **Groups typing into sessions** (5-second gaps create new sessions)
- **Saves daily logs** with human-readable filenames
- **Tracks metrics** like characters, words, keystrokes, and session duration
- **No AI processing** - just pure activity tracking
- **Complete privacy** - everything stays local on your machine

## 📁 Output Structure

Files are saved to `/Users/pk/Desktop/content/typing-output/` with human-readable names:

```
typing-output/
├── 2025-06-03_Daily_Typing_Log.json     # Complete daily summary
├── 2025-06-03_Typing_Session_09-15am.json
├── 2025-06-03_Typing_Session_02-30pm.json
├── 2025-06-03_Typing_Session_04-45pm.json
└── 2025-06-04_Daily_Typing_Log.json     # Next day starts new file
```

## 📊 Data Format

**Daily Log Structure:**
```json
{
  "date": "2025-06-03",
  "created": "2025-06-03T09:15:30.123456",
  "last_updated": "2025-06-03T17:45:20.987654",
  "total_sessions": 8,
  "total_characters": 4521,
  "total_words": 892,
  "total_keystrokes": 5103,
  "sessions": [
    {
      "session_start": "2025-06-03T09:15:30.123456",
      "session_end": "2025-06-03T09:18:45.789012",
      "content": "Sample typing content from this session...",
      "character_count": 156,
      "word_count": 28,
      "total_keystrokes": 175,
      "duration_seconds": 195.7,
      "last_activity": "2025-06-03T09:18:45.789012"
    }
  ]
}
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- macOS, Windows, or Linux

### Installation

1. **Clone or download** this folder to your machine

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **macOS Users - Grant Accessibility Permissions:**
   - System Settings > Privacy & Security > Accessibility
   - Add your terminal application (Terminal, iTerm2, VS Code, etc.)
   - Grant permission when prompted

### Running the Tracker

```bash
python typing_tracker.py
```

**What You'll See:**
```
🔥 Typing tracker started - saving to: /Users/pk/Desktop/content/typing-output
💡 Press Ctrl+C to stop and save
⌨️  Start typing to begin capturing sessions...
💾 Session saved: 156 chars, 28 words
💾 Session saved: 89 chars, 15 words
```

**To Stop:**
- Press `Ctrl+C` to gracefully shutdown and save the final session

## 🔧 Configuration

### Change Output Directory
Edit the `output_dir` parameter in `typing_tracker.py`:
```python
tracker = TypingTracker(output_dir="/your/custom/path")
```

### Adjust Session Gap
Change how long of a pause creates a new session (default: 5 seconds):
```python
self.session_gap_seconds = 10  # 10 seconds instead of 5
```

## 📋 Features

### Session Detection
- **Automatic grouping**: Typing separated by 5+ seconds becomes a new session
- **Real-time tracking**: Characters, words, and keystrokes counted live
- **Smart timestamps**: Human-readable filenames with date and time

### Content Capture
- **Full text capture**: Everything you type (locally stored)
- **Special key handling**: Spaces, backspaces, tabs, and newlines
- **Platform support**: Works on macOS, Windows, and Linux

### File Organization
- **Daily logs**: One master file per day with all sessions
- **Human-readable names**: `2025-06-03_Typing_Session_02-30pm.json`
- **Organized structure**: Easy to find and analyze your data

## 🔐 Privacy & Security

- **100% Local**: No data leaves your computer
- **No Network**: No internet connection required or used  
- **No AI Processing**: Just captures and stores typing activity
- **Your Control**: You own all the data, delete anytime
- **Open Source**: Full code transparency

## 🛠️ Technical Details

### Dependencies
- **pynput**: Cross-platform keyboard monitoring
- **json**: Built-in JSON file handling
- **datetime**: Built-in timestamp handling
- **os**: Built-in file system operations

### Platform Support
- **macOS**: Full support (requires Accessibility permissions)
- **Windows**: Full support
- **Linux**: Full support (may require X11 tools)

### Performance
- **Lightweight**: Minimal CPU and memory usage
- **Efficient**: Only processes actual keystrokes
- **Non-intrusive**: Runs silently in background

## 📖 Usage Examples

### Basic Usage
```bash
# Start tracking
python typing_tracker.py

# Type normally in any application
# Press Ctrl+C when done
```

### View Your Data
```bash
# Check what was saved
ls /Users/pk/Desktop/content/typing-output/

# View a daily log
cat /Users/pk/Desktop/content/typing-output/2025-06-03_Daily_Typing_Log.json
```

### Integration with Other Tools
```bash
# Process with jq (JSON processor)
cat 2025-06-03_Daily_Typing_Log.json | jq '.total_words'

# Import into analysis scripts
python -c "
import json
with open('2025-06-03_Daily_Typing_Log.json') as f:
    data = json.load(f)
    print(f'Total words today: {data[\"total_words\"]}')
"
```

## 🔍 Troubleshooting

### "Platform not supported" Error
```bash
pip install pynput
```

### macOS Permission Denied
1. System Settings > Privacy & Security > Accessibility
2. Add your terminal app
3. Restart the tracker

### Output Directory Not Found
The tracker automatically creates the output directory. If you see permission errors:
```bash
mkdir -p /Users/pk/Desktop/content/typing-output
chmod 755 /Users/pk/Desktop/content/typing-output
```

### Files Not Saving
Check disk space and directory permissions:
```bash
df -h /Users/pk/Desktop/content/
ls -la /Users/pk/Desktop/content/typing-output/
```

## 🚦 Status Indicators

During operation you'll see:
- `🔥 Typing tracker started` - Successfully initialized
- `💾 Session saved: X chars, Y words` - Session completed and saved
- `🛑 Typing tracker stopped` - Gracefully shut down
- `📁 Output saved to: /path` - Final save location

## 🎮 Keyboard Shortcuts

- **Ctrl+C**: Stop tracking and save current session
- **All other keys**: Captured as part of typing sessions

---

**Simple, lightweight, and completely private typing activity tracking.**
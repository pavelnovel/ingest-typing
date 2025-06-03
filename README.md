# Typing Activity Tracker

A lightweight, privacy-focused typing activity tracker that captures your typing sessions and saves them as organized JSON files with human-readable timestamps.

## 🎯 What It Does

- **Captures typing activity** across all applications on your computer
- **One continuous session** from start to Ctrl+C
- **Paragraph breaks** for 5+ second gaps (but same session continues)
- **Creates session file** only when you start typing
- **Tracks metrics** like characters, words, keystrokes, and session duration
- **No AI processing** - just pure activity tracking
- **Complete privacy** - everything stays local on your machine

## 📁 Output Structure

Files are saved to `/Users/pk/Desktop/content/typing-output/` with human-readable names:

```
typing-output/
├── 2025-06-03_Typing_Session_09-15am.json  # One continuous session per run
├── 2025-06-03_Typing_Session_02-30pm.json  # New session if restarted
└── 2025-06-04_Typing_Session_10-45am.json  # Next day session
```

**Note:** Each time you run the tracker, it creates ONE session file that continues until you press Ctrl+C.

## 📊 Data Format

**Session File Structure:**
```json
{
  "session_start": "2025-06-03T09:15:30.123456",
  "session_end": "2025-06-03T11:45:20.987654",
  "content": "This is everything I typed...\n\nWith paragraph breaks for 5+ second gaps...\n\nAll in one continuous session until Ctrl+C",
  "character_count": 4521,
  "word_count": 892,
  "total_keystrokes": 5103,
  "duration_seconds": 8990.5,
  "last_activity": "2025-06-03T11:45:20.987654"
}
```

**Key Features:**
- `content`: All your typing with `\n\n` for 5+ second gaps
- `duration_seconds`: Total time from first keystroke to Ctrl+C
- `character_count`: Total characters typed (including spaces)
- `word_count`: Total words in the session

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
📝 Session started: 2025-06-03_Typing_Session_09-15am.json  (when you start typing)
💾 Session saved: 1247 chars, 245 words                    (when you press Ctrl+C)
📁 File: 2025-06-03_Typing_Session_09-15am.json
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
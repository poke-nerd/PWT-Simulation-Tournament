import os
import subprocess

def is_apng(filepath):
    """Check if a .png file is an animated PNG using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', filepath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True  # use for Python 3.6
        )
        return 'apng' in result.stdout.lower()
    except Exception as e:
        print(f"Error checking file {filepath}: {e}")
        return False

def rename_apngs_in_current_dir():
    """Rename .png to .apng for files that are actually animated."""
    for filename in os.listdir('.'):
        if filename.lower().endswith('.png'):
            if is_apng(filename):
                new_name = filename[:-4] + '.apng'
                os.rename(filename, new_name)
                print(f"✅ Renamed: {filename} → {new_name}")
            else:
                print(f"ℹ️ Skipped (not APNG): {filename}")

if __name__ == "__main__":
    rename_apngs_in_current_dir()


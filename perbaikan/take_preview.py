import subprocess
import os
import time

edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
art_dir = r'C:\Users\Dibra\.gemini\antigravity\brain\45548f41-2317-4b90-b652-65a7f2c7ffc5'

def capture(url, output_name, width=1920, height=1080):
    out_path = os.path.join(art_dir, output_name)
    cmd = [
        edge_exe,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--window-size={width},{height}',
        f'--screenshot={out_path}',
        url
    ]
    subprocess.run(cmd, timeout=15)
    print(f"Captured {output_name}: {os.path.exists(out_path)} ({os.path.getsize(out_path) if os.path.exists(out_path) else 0} bytes)")

if __name__ == '__main__':
    capture('http://localhost:8080/index.html', 'test_hero_current.png', 1920, 1080)

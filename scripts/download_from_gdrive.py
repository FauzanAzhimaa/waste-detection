"""
Download raw_data from Google Drive
Useful for training without manual download
"""
import os
import gdown
from pathlib import Path


def download_folder_from_gdrive(folder_url, output_dir='raw_data'):
    """
    Download entire folder from Google Drive
    
    Args:
        folder_url: Google Drive folder URL or ID
        output_dir: Local directory to save files
    
    Example URLs:
        https://drive.google.com/drive/folders/1ABC123xyz...
        or just the ID: 1ABC123xyz...
    """
    print(f"📥 Downloading from Google Drive...")
    print(f"📁 Output directory: {output_dir}")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    
    try:
        # Extract folder ID from URL if needed
        if 'drive.google.com' in folder_url:
            folder_id = folder_url.split('/')[-1].split('?')[0]
        else:
            folder_id = folder_url
        
        print(f"🔑 Folder ID: {folder_id}")
        
        # Download folder
        gdown.download_folder(
            id=folder_id,
            output=output_dir,
            quiet=False,
            use_cookies=False
        )
        
        print(f"✅ Download complete!")
        print(f"📂 Files saved to: {output_dir}")
        
        # Count downloaded files
        total_files = sum(1 for _ in Path(output_dir).rglob('*') if _.is_file())
        print(f"📊 Total files: {total_files}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tips:")
        print("1. Make sure folder is shared (Anyone with link can view)")
        print("2. Check folder URL/ID is correct")
        print("3. Install gdown: pip install gdown")


def download_file_from_gdrive(file_url, output_path):
    """
    Download single file from Google Drive
    
    Args:
        file_url: Google Drive file URL or ID
        output_path: Local path to save file
    
    Example URLs:
        https://drive.google.com/file/d/1ABC123xyz.../view
        or just the ID: 1ABC123xyz...
    """
    print(f"📥 Downloading file from Google Drive...")
    
    try:
        # Extract file ID from URL if needed
        if 'drive.google.com' in file_url:
            file_id = file_url.split('/d/')[1].split('/')[0]
        else:
            file_id = file_url
        
        print(f"🔑 File ID: {file_id}")
        
        # Download file
        gdown.download(
            id=file_id,
            output=output_path,
            quiet=False
        )
        
        print(f"✅ Download complete!")
        print(f"📄 File saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tips:")
        print("1. Make sure file is shared (Anyone with link can view)")
        print("2. Check file URL/ID is correct")
        print("3. Install gdown: pip install gdown")


if __name__ == '__main__':
    print("=" * 60)
    print("📥 Google Drive Downloader")
    print("=" * 60)
    
    # Example usage
    print("\n📖 Usage:")
    print("\n1. Download entire folder:")
    print("   python scripts/download_from_gdrive.py")
    print("   Then enter your Google Drive folder URL")
    
    print("\n2. Or edit this script and set:")
    print("   FOLDER_URL = 'your_google_drive_folder_url'")
    print("   OUTPUT_DIR = 'raw_data'")
    
    # Interactive mode
    choice = input("\n❓ Download folder? (y/n): ").lower()
    
    if choice == 'y':
        folder_url = input("📎 Enter Google Drive folder URL or ID: ").strip()
        output_dir = input("📁 Output directory (default: raw_data): ").strip() or 'raw_data'
        
        download_folder_from_gdrive(folder_url, output_dir)
    else:
        print("\n💡 To use this script:")
        print("1. Upload raw_data to Google Drive")
        print("2. Right click folder → Share → Anyone with link can view")
        print("3. Copy folder URL")
        print("4. Run this script and paste URL")
        print("\n📚 Documentation: https://github.com/wkentaro/gdown")

import os
import urllib.request
import tarfile

# Pascal VOC 2007 URLs
URLS = {
    'trainval': 'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar',
    'test':     'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar'
}

DATA_DIR = os.path.join('..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw_tar')
EXTRACT_DIR = os.path.join(DATA_DIR, 'VOCdevkit')

def download_and_extract():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    
    for split, url in URLS.items():
        tar_path = os.path.join(RAW_DIR, f"{split}_2007.tar")
        
        # Download
        if not os.path.exists(tar_path):
            print(f"Downloading {url} ...")
            def report(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                print(f"\rDownloading {split} dataset: {percent}%", end="")
            
            urllib.request.urlretrieve(url, tar_path, reporthook=report)
            print("\nDownload complete.")
        else:
            print(f"Tar file {tar_path} already exists. Skipping download.")
            
        # Extract
        print(f"Extracting {tar_path} into {DATA_DIR} ...")
        with tarfile.open(tar_path, 'r') as tar_ref:
            tar_ref.extractall(path=DATA_DIR)
        print(f"Extraction of {split} complete.\n")

if __name__ == '__main__':
    # Determine absolute path to place data at right location from the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(script_dir, '..', 'data')
    RAW_DIR = os.path.join(DATA_DIR, 'raw_tar')
    EXTRACT_DIR = os.path.join(DATA_DIR, 'VOCdevkit')
    
    download_and_extract()
    print(f"All done! Your VOCdevkit is ready at: {EXTRACT_DIR}")

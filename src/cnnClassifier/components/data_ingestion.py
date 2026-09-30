import os
import py7zr
import gdown
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    
    def download_file(self)-> str:
        '''
        Fetch data from the url
        '''
        dataset_url = self.config.source_URL
        download_path = os.fspath(self.config.local_data_file)
        os.makedirs(self.config.root_dir, exist_ok=True)

        if os.path.isfile(download_path) and py7zr.is_7zfile(download_path):
            logger.info(f"Using existing archive at {download_path}")
            return download_path

        logger.info(f"Downloading data from {dataset_url} into file {download_path}")
        downloaded_path = gdown.download(url=dataset_url, output=download_path)
        if not downloaded_path:
            raise RuntimeError(f"Failed to download dataset from {dataset_url}")

        logger.info(f"Downloaded data from {dataset_url} into file {downloaded_path}")
        return os.fspath(downloaded_path)

        
    def extract_zip_file(self):
        """
        Extracts the 7z archive into the data directory.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with py7zr.SevenZipFile(self.config.local_data_file, mode='r') as archive:
            archive.extractall(path=unzip_path)
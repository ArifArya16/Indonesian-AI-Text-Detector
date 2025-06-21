"""
Configuration file for AI Text Detector
"""

import os

class Config:
    # Model settings
    MODEL_PATH = "indobert_ai_detector"
    BASE_MODEL_NAME = "indobenchmark/indobert-base-p1"
    MAX_LENGTH = 512
    
    # Thresholds
    AI_THRESHOLD = 0.7  # 70% confidence untuk menentukan teks AI
    HIGH_CONFIDENCE_THRESHOLD = 0.85  # 85% untuk confidence tinggi
    
    # Database - Gunakan path relatif yang aman untuk Streamlit Cloud
    DATABASE_PATH = "users.db"  # Langsung di root directory
    
    # UI Settings
    APP_TITLE = "🤖 Detector Teks AI Indonesia"
    APP_DESCRIPTION = "Sistem deteksi teks yang dibuat oleh AI menggunakan IndoBERT + LoRA"
    
    # Styling
    DARK_THEME = {
        "primary_color": "#FF6B6B",
        "background_color": "#0E1117",
        "secondary_background_color": "#262730",
        "text_color": "#FAFAFA"
    }
    
    # Logging - Disesuaikan untuk Streamlit Cloud
    LOG_LEVEL = "INFO"
    LOG_FILE = None  # Disable file logging untuk Streamlit Cloud
    
    # Session settings
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    @classmethod
    def setup_directories(cls):
        """
        Setup directories yang diperlukan jika memungkinkan
        """
        directories = []
        
        # Hanya buat directory jika LOG_FILE digunakan
        if cls.LOG_FILE and cls.LOG_FILE != "None":
            log_dir = os.path.dirname(cls.LOG_FILE)
            if log_dir:
                directories.append(log_dir)
        
        # Buat directories jika memungkinkan
        for directory in directories:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
            except (PermissionError, OSError) as e:
                print(f"Warning: Cannot create directory {directory}: {e}")
    
    @classmethod
    def get_safe_database_path(cls):
        """
        Dapatkan path database yang aman
        """
        try:
            # Test apakah bisa write di current directory
            test_file = "test_write.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return cls.DATABASE_PATH
        except (PermissionError, OSError):
            # Jika tidak bisa write, gunakan in-memory database
            return ":memory:"
    
    @classmethod
    def is_streamlit_cloud(cls):
        """
        Deteksi apakah running di Streamlit Cloud
        """
        return (
            os.getenv("STREAMLIT_SHARING_MODE") is not None or
            os.getenv("STREAMLIT_CLOUD") is not None or
            "streamlit" in os.getcwd().lower()
        )

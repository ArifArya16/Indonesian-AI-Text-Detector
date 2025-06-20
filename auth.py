"""
Authentication functions for AI Text Detector
"""

import streamlit as st
import re
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password harus minimal 6 karakter"
        return True, "Password valid"
    
    def validate_username(self, username):
        """Validate username"""
        if len(username) < 3:
            return False, "Username harus minimal 3 karakter"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username hanya boleh mengandung huruf, angka, dan underscore"
        return True, "Username valid"
    
    def login_form(self):
        """Display login form - UBAH METHOD INI"""
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if not username or not password:
                    st.error("Username dan password harus diisi")
                    return False
                
                result = self.db.authenticate_user(username, password)
                if isinstance(result, tuple) and len(result) == 2:
                    user_id, role = result
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.user_role = role
                        st.session_state.authenticated = True
                        st.session_state.login = False
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error(role)  # role contains error message
                        return False
                else:
                    st.error("Username atau password salah")
                    return False
        
        return False
    
    
    def register_form(self):
        """Display registration form"""
        st.subheader("📝 Daftar Akun Baru")
        
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Konfirmasi Password", type="password")
            submit_button = st.form_submit_button("Daftar")
            
            if submit_button:
                # Validation
                if not all([username, email, password, confirm_password]):
                    st.error("Semua field harus diisi")
                    return False
                
                # Validate username
                username_valid, username_msg = self.validate_username(username)
                if not username_valid:
                    st.error(username_msg)
                    return False
                
                # Validate email
                if not self.validate_email(email):
                    st.error("Format email tidak valid")
                    return False
                
                # Validate password
                password_valid, password_msg = self.validate_password(password)
                if not password_valid:
                    st.error(password_msg)
                    return False
                
                # Check password confirmation
                if password != confirm_password:
                    st.error("Password dan konfirmasi password tidak sama")
                    return False
                
                # Try to create user
                user_id = self.db.create_user(username, email, password)
                if user_id:
                    st.success("Akun berhasil dibuat! Silakan login.")
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error("Username atau email sudah digunakan")
                    return False
        
        return False
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        for key in ['user_id', 'username', ]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.show_detailed_analysis = False
        st.session_state.analisis_text = None
        st.rerun()
    
    def check_authentication(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user_role(self):
        """Get current user role"""
        return st.session_state.get('user_role', 'user')
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.get_current_user_role() == 'admin'
    
    def get_current_user_id(self):
        """Get current user ID"""
        return st.session_state.get('user_id')
    
    def get_current_username(self):
        """Get current username"""
        return st.session_state.get('username')
    
    def authentication_page(self):
        """Display authentication page"""
        st.title("🤖 Detector Teks AI Indonesia")
        st.markdown("---")
        
        # Toggle between login and register
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.session_state.show_register:
                self.register_form()
            else:
                self.login_form()
        
        with col2:
            st.markdown("### ")
            if st.session_state.show_register:
                if st.button("← Kembali ke Login"):
                    st.session_state.show_register = False
                    st.rerun()
            else:
                if st.button("Daftar Akun Baru"):
                    st.session_state.show_register = True
                    st.rerun()
        # Info section
        st.markdown("---")
        st.markdown("""
        ### 🔍 Tentang Sistem Ini
        
        Sistem ini menggunakan model **IndoBERT + LoRA** yang telah di-fine-tune khusus untuk:
        - Mendeteksi teks bahasa Indonesia yang dibuat oleh AI
        - Memberikan skor kepercayaan dalam persentase
        - Menyorot bagian teks yang dicurigai sebagai hasil AI
        - Menyimpan riwayat analisis untuk setiap pengguna
        
        **Fitur Utama:**
        - ✅ Analisis teks real-time
        - ✅ Visualisasi tingkat kepercayaan
        - ✅ Riwayat prediksi
        - ✅ Download hasil analisis
        - ✅ Interface yang user-friendly
        """)
    
    def init_session_state(self):
        """Initialize session state - UBAH METHOD INI"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_role' not in st.session_state:
            st.session_state.user_role = 'user'
        if 'login' not in st.session_state:
            st.session_state.login = False
        if 'show_detailed_analysis' not in st.session_state:
            st.session_state.show_detailed_analysis = False
        if 'analisis_text' not in st.session_state:
            st.session_state.analisis_text = None
"""
Test script to verify the setup and dependencies
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    print("=" * 60)
    print("Checking Dependencies...")
    print("=" * 60)
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'xgboost': 'XGBoost',
        'imblearn': 'imbalanced-learn'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            missing.append(name)
    
    if missing:
        print("\n" + "=" * 60)
        print("Missing packages detected!")
        print("Please install them using:")
        print("pip install -r requirements.txt")
        print("=" * 60)
        return False
    else:
        print("\n" + "=" * 60)
        print("✓ All dependencies are installed!")
        print("=" * 60)
        return True

def check_files():
    """Check if all required files exist"""
    print("\n" + "=" * 60)
    print("Checking Files...")
    print("=" * 60)
    
    required_files = [
        'cirrhosis.csv',
        'index.html',
        'style.css',
        'script.js',
        'app.py',
        'requirements.txt'
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} exists ({size:,} bytes)")
        else:
            print(f"✗ {file} is MISSING")
            missing.append(file)
    
    if missing:
        print("\n" + "=" * 60)
        print("Missing files detected!")
        print("Please ensure all files are in the same directory.")
        print("=" * 60)
        return False
    else:
        print("\n" + "=" * 60)
        print("✓ All required files are present!")
        print("=" * 60)
        return True

def test_csv_loading():
    """Test if CSV can be loaded"""
    print("\n" + "=" * 60)
    print("Testing CSV Loading...")
    print("=" * 60)
    
    try:
        import pandas as pd
        df = pd.read_csv('cirrhosis.csv')
        print(f"✓ CSV loaded successfully!")
        print(f"  - Rows: {len(df)}")
        print(f"  - Columns: {len(df.columns)}")
        print(f"  - Columns: {', '.join(df.columns[:5])}...")
        return True
    except Exception as e:
        print(f"✗ Error loading CSV: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CIRRHOSIS PREDICTION SYSTEM - SETUP VERIFICATION")
    print("=" * 60)
    
    deps_ok = check_dependencies()
    files_ok = check_files()
    csv_ok = test_csv_loading() if files_ok else False
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if deps_ok and files_ok and csv_ok:
        print("✓ Setup is complete! You're ready to run the application.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nThen open your browser to:")
        print("  http://localhost:5000")
    else:
        print("✗ Setup incomplete. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Ensure all files are in the same directory")
        print("  3. Verify cirrhosis.csv is not corrupted")
    
    print("=" * 60)

if __name__ == '__main__':
    main()

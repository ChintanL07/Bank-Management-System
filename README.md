# 🏦 Bank Management System - Modern Web Application

## 🎯 Overview

**Bank Management System** has been completely transformed from a basic C++ console application into a **modern, feature-rich web application** using Streamlit with beautiful UI/UX design and enterprise-level features.

### 🔄 **Dual Implementation Available:**
1. **📱 Modern Web App** - Streamlit-based with advanced features *(New & Recommended)*
2. **⌨️ Original Console App** - C++ console-based application *(Legacy)*

## ✨ **Modern Web Application Features**

### 🔐 **Authentication & Security**
- ✅ Multi-user registration and login system
- ✅ Secure password hashing with BCrypt
- ✅ Session management and SQL injection protection

### 💳 **Enhanced Banking Operations**
- ✅ **Multiple Account Types** (Savings, Current)
- ✅ **Deposits & Withdrawals** with real-time validation
- ✅ **Inter-account Transfers** with reference numbers
- ✅ **Complete Transaction History** with timestamps
- ✅ **Real-time Balance Updates**

### 📊 **Analytics & Insights**
- ✅ **Interactive Dashboards** with Plotly visualizations
- ✅ **Balance Distribution** charts and graphs
- ✅ **Transaction Trends** analysis over time
- ✅ **Monthly Spending** patterns and insights

### 🎨 **Beautiful UI/UX Design**
- ✅ **Modern Gradient Themes** with professional styling
- ✅ **Card-based Layouts** with shadows and animations
- ✅ **Responsive Design** for all screen sizes
- ✅ **Intuitive Navigation** with sidebar menu

---

## 🚀 **Quick Start - Web Application**

### **Prerequisites**
- Python 3.8+ installed
- Git for cloning the repository

### **Installation & Setup**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChintanL07/Bank-Management-System.git
   cd Bank-Management-System
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run bank_management_app.py
   ```

4. **Access the Application**
   - Open your browser and go to: `http://localhost:8501`
   - The application will automatically open in your default browser

### **🎮 Demo Login Credentials**
```
Username: john_doe     | Password: password123
Username: jane_smith   | Password: mypassword
Username: alice_johnson| Password: securepass
Username: bob_wilson   | Password: bobpass456
```

### **🎯 Alternative Launchers**
- **Windows PowerShell**: Double-click `start_app.ps1`
- **Windows Batch**: Double-click `start_app.bat`

---

## 🖥️ **Original Console Application Features**

The original C++ implementation provides basic banking operations:

1. **Open Account** - Create new bank accounts with unique numbers
2. **Deposit Money** - Add funds to existing accounts
3. **Withdraw Money** - Remove funds with balance validation
4. **Display Account** - View account details and balance

---

## 💻 **Console Application Setup**

### **Prerequisites**
- C++ compiler (g++, clang++, or Visual Studio)
- Any C++ IDE or text editor

### **Compilation & Execution**

**For C++ Version:**
```bash
g++ -o BankManagementSystem main.cpp
./BankManagementSystem
```

**For C Version:**
```bash
gcc -o bank bank.c
./bank
```

---

## 🏗️ **Project Architecture**

### **📁 File Structure**
```
Bank-Management-System/
├── 🌐 Web Application
│   ├── bank_management_app.py     # Main Streamlit app
│   ├── requirements.txt           # Python dependencies
│   ├── create_demo_data.py        # Demo data generator
│   ├── start_app.ps1             # PowerShell launcher
│   ├── start_app.bat             # Batch launcher
│   └── bank_system.db            # SQLite database
├── 📖 Documentation
│   ├── README_WebApp.md          # Detailed web app docs
│   ├── PROJECT_SHOWCASE.md       # Complete project overview
│   └── README.md                 # This file
└── 💻 Console Applications
    ├── main.cpp                  # C++ implementation
    ├── bank.c                    # C implementation
    └── accounts.dat              # Data file
```

### **🛠️ Technology Stack**

**Web Application:**
- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with SQLite database
- **Visualization**: Plotly for interactive charts
- **Security**: BCrypt for password hashing

**Console Application:**
- **Language**: C++ with STL containers
- **Storage**: File-based data persistence

---

## 📸 **Screenshots & Features**

### **🏠 Modern Dashboard**
- Real-time account metrics and balances
- Quick action buttons for common operations
- Recent transaction overview
- Beautiful gradient card designs

### **💳 Account Management**
- Multiple account types support
- Visual account cards with details
- Easy deposit/withdrawal interfaces
- Transaction history with search

### **📊 Analytics Dashboard**
- Interactive charts and graphs
- Balance distribution visualizations
- Transaction trend analysis
- Monthly spending insights

---

## 🔄 **Migration Guide: Console → Web**

| Console Feature | Web Enhancement |
|----------------|-----------------|
| Single user | → Multi-user with authentication |
| Text interface | → Beautiful web UI with charts |
| Basic operations | → Advanced banking features |
| File storage | → Professional database |
| No analytics | → Rich insights and visualizations |
| Desktop only | → Web-based, accessible anywhere |

---

## 🤝 **Contributing**

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Streamlit Team** - For the amazing web app framework
- **Plotly** - For beautiful interactive visualizations
- **SQLite** - For reliable database functionality
- **Python Community** - For excellent libraries and tools

---

## 📞 **Contact & Support**

- **GitHub**: [@ChintanL07](https://github.com/ChintanL07)
- **Email**: b22me036@iitj.ac.in
- **Project Link**: [Bank Management System](https://github.com/ChintanL07/Bank-Management-System)

---

<div align="center">

## 🏆 **Project Evolution**

**From Simple Console App → Professional Web Application**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**⭐ If you found this project helpful, please give it a star! ⭐**

</div>

- `main.cpp`: The main file containing the implementation of the Bank Management System.

## Usage

1. Run the executable file created after compilation.
2. Follow the on-screen instructions to perform different banking operations.
3. Choose from the menu options to open an account, deposit money, withdraw money, or display account details.
4. Exit the application by selecting the exit option from the menu.

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes.


## Contact

For any questions or inquiries, please contact:
- **Name:** Limbachiya Chintan Bharatbhai
- **Email:** chintanlimbachiya1515@gmail.com
- **LinkedIn:** [Chintan Limbachiya](https://www.linkedin.com/in/chintan-limbachiya/)

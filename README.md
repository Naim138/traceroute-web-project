# 🌐 Traceroute Web Application

A modern web-based traceroute tool built using Python Flask.

## ✨ Features

* 🖥️ **Web Interface**: Clean and user-friendly interface
* 🌍 **Geolocation**: Displays the location of each router
* ⏱️ **Real-time Results**: Live traceroute output
* 📊 **RTT Measurement**: Round-trip time calculation
* 🎨 **Beautiful UI**: Modern gradient design
* 📱 **Responsive**: Works on both mobile and desktop

## 📋 Requirements

* Python 3.7+
* Flask
* Requests
* Administrator/Root privileges

## 🚀 Installation

### Step 1: Download/Clone

```bash
# Navigate to your project folder
cd traceroute-web-project
```

### Step 2: Create Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

### Linux/Mac:

```bash
sudo python3 app.py
```

### Windows (Administrator PowerShell):

```powershell
python app.py
```

### Open in Browser:

```
http://localhost:5000
```

## 📖 Usage

1. **Open Browser**: `http://localhost:5000`
2. **Enter Destination**: hostname or IP address
3. **Click Start Traceroute**
4. **View Results**: Live traceroute output

## 📁 Project Structure

```
traceroute-web-project/
│
├── app.py                      # Flask server
├── traceroute_core.py          # Core logic
├── requirements.txt            # Dependencies
├── README.md                   # This file
│
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── script.js          # Frontend logic
│
├── templates/
│   ├── index.html             # Home page
│   └── about.html             # About page
│
└── results/                    # Saved results
```

## 🎯 Example Destinations

* `google.com`
* `facebook.com`
* `8.8.8.8` (Google DNS)
* `1.1.1.1` (Cloudflare DNS)
* `mit.edu`

## 🔧 Troubleshooting

### Problem: Permission Denied

**Solution**: Run as administrator/root

```bash
# Linux/Mac:
sudo python3 app.py

# Windows: Run PowerShell as Administrator
```

### Problem: Port 5000 Already in Use

**Solution**: Change port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Problem: Module Not Found

**Solution**: Install dependencies:

```bash
pip install flask requests matplotlib
```

## 📊 How It Works

### 1. TTL Manipulation

Set the TTL value in each packet (1, 2, 3...)

### 2. ICMP Packets

Send ICMP Echo Request packets

### 3. Router Responses

Routers send ICMP Time Exceeded messages

### 4. Path Discovery

This way, all routers on the path are discovered

## 🎨 Features Explained

### Web Interface

* Modern gradient design
* Responsive layout
* Real-time updates
* Error handling

### Geolocation

* Shows city and country details
* ISP information
* Uses IP-API.com

### RTT Measurement

* Sends 3 probe packets
* Calculates average, minimum, and maximum
* Displayed in milliseconds

## 🔐 Security Notes

* Requires raw socket access
* Administrator/Root privileges needed
* Apply security measures for production deployment

## 📝 Project Information

* **Course**: Computer Networking Lab
* **Topic**: Traceroute Implementation
* **Language**: Python 3
* **Framework**: Flask
* **Year**: 2024

## 🎓 Learning Outcomes

You will learn:

* ✅ Network protocols (ICMP, IP)
* ✅ Socket programming
* ✅ Web development (Flask)
* ✅ Frontend development (HTML/CSS/JS)
* ✅ TTL mechanism
* ✅ Packet analysis

## 📞 Support

If you face any issues:

1. Read the README
2. Check error messages
3. Verify dependencies
4. Ensure administrator/root privileges are available

## 📜 License

This project is created for educational purposes.

## 🙏 Acknowledgments

* *Computer Networking: A Top-Down Approach* (Kurose & Ross)
* Flask Documentation
* Python Socket Documentation

---

**Happy Tracing!** 🚀

Made with ❤️ for Computer Networking Lab

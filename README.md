# 🎉 Event Management System  

A simple **Streamlit-based web application** to manage Media Unit members and events.  
This app connects to a **Supabase database** for storing and retrieving data.

---

## 🚀 Features  
- Add, view, and manage members easily  
- Store and retrieve event information  
- Connects to Supabase for database operations  
- Clean and simple UI built with Streamlit  
- Secure API keys with `.env` or `secrets.toml`  

---

## 🛠️ Tech Stack  
- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask)  
- **Database:** Supabase (PostgreSQL)  

---

## 📸 Screenshot  

Here’s how the app looks:  

##### Screenshot 1
![Screenshot 1](assets/1.png)

##### Screenshot 2
![Screenshot 2](assets/1.png)

---

## ⚙️ Setup Instructions  

### 1. Clone the repository  

`git clone https://github.com/Subhaga2000/media-unit-management.git
cd your-media-unit-management`

### 2. Create and Activate Virtual Environment

`python -m venv .venv`
#### Windows
`.venv\Scripts\activate`
#### Mac/Linux
`source .venv/bin/activate`

### 3. Install Dependencies

`pip install -r requirements.txt`

### 4. Set Up Secrets

`[supabase]`
**url = "your-supabase-url"**
**key = "your-supabase-key"**


### 5. Run the Application

`streamlit run app.py`





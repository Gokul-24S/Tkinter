import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# User credentials (for demonstration)
users = {
    "gokul": {"password": "Tkinter@12", "email": "gokulsuriya966@psnacet.edu.in", "profile_pic": None},
    "suriya": {"password": "handsome23", "email": "actorsuriya23@gmail.com", "profile_pic": None}
}

# Store the generated OTP
otp_code = None

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to send OTP via email
def send_otp_email(recipient_email, otp):
    sender_email = "gokulsuriya966@gmail.com"
    sender_password = "twdv sqph osua dmdk"  # Use your actual password

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"OTP sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to verify OTP
def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == str(otp_code):
        messagebox.showinfo("Login Success", f"Welcome, {username_entry.get()}!")
        otp_window.destroy()  # Close OTP window
        show_main_screen()    # Show main screen after login
    else:
        messagebox.showerror("Invalid OTP", "The OTP entered is incorrect.")

# Function to resend OTP
def resend_otp():
    global otp_code
    otp_code = generate_otp()
    recipient_email = users[username_entry.get()]['email']
    send_otp_email(recipient_email, otp_code)
    messagebox.showinfo("OTP Resent", "A new OTP has been sent to your email.")

# Function to enable profile picture upload
def enable_profile_pic_upload():
    upload_button.config(state=tk.NORMAL)
    reset_pic_button.config(state=tk.NORMAL)

# Function to upload profile picture
def upload_profile_picture():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        users[username_entry.get()]['profile_pic'] = file_path
        show_profile_picture()

# Function to reset profile picture
def reset_profile_picture():
    users[username_entry.get()]['profile_pic'] = None
    profile_label.config(image='', text="No Profile Picture")

# Function to display profile picture
def show_profile_picture():
    user = username_entry.get()
    img_path = users[user].get("profile_pic")
    if img_path:
        img = Image.open(img_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        profile_label.config(image=img_tk, text="")
        profile_label.image = img_tk
    else:
        profile_label.config(image='', text="No Profile Picture")

# Function to validate password using regex
def validate_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(pattern, password) is not None

# Function to show password strength
def check_password_strength(event):
    password = password_entry.get()
    if len(password) < 8:
        strength_label.config(text="Weak", fg="red")
    elif validate_password(password):
        strength_label.config(text="Strong", fg="green")
    else:
        strength_label.config(text="Moderate", fg="orange")

# Function to handle login
def login():
    global otp_code

    username = username_entry.get()
    password = password_entry.get()

    if username in users:
        if validate_password(password):
            if users[username]['password'] == password:
                otp_code = generate_otp()
                recipient_email = users[username]['email']
                send_otp_email(recipient_email, otp_code)

                global otp_window, otp_entry
                otp_window = tk.Toplevel(root)
                otp_window.title("Enter OTP")
                otp_window.geometry("300x200")
                otp_window.config(bg="#D8BFD8")

                tk.Label(otp_window, text="Enter OTP sent to your email:", bg="#D8BFD8").pack(pady=10)
                otp_entry = tk.Entry(otp_window)
                otp_entry.pack(pady=10)

                tk.Button(otp_window, text="Verify OTP", command=verify_otp, bg="#4CAF50", fg="white").pack(pady=10)
                tk.Button(otp_window, text="Resend OTP", command=resend_otp, bg="#f0ad4e", fg="white").pack(pady=5)
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "Use a strong password 0-10,a-z,A-Z,@#,_.")
    else:
        messagebox.showerror("Login Failed", "Invalid username")

# Function to log out
def logout():
    main_screen.destroy()
    root.deiconify()

# Function to show main screen after login
def show_main_screen():
    global main_screen
    root.withdraw()
    main_screen = tk.Toplevel(root)
    main_screen.title("Main Screen")
    main_screen.geometry("400x400")
    tk.Label(main_screen, text=f"Welcome, {username_entry.get()}!",font=("Arial", 16)).pack(pady=20)

    # Profile Picture Section
    upload_button.config(state=tk.NORMAL)
    reset_pic_button.config(state=tk.NORMAL)

    upload_button.pack(pady=5)
    reset_pic_button.pack(pady=5)

    profile_label = tk.Label(main_screen, text="No Profile Picture", font=("Arial", 10))
    profile_label.pack(pady=10)

    tk.Button(main_screen, text="Logout", command=logout, bg="#f44336", fg="white").pack(pady=20)

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("300x400")
root.config(bg="#008B8B")

# Username label and entry
tk.Label(root, text="Username:", bg="#f0f0f0").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
tk.Label(root, text="Password:", bg="#f0f0f0").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)
password_entry.bind("<KeyRelease>", check_password_strength)

# Password strength label
strength_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f0f0")
strength_label.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login, bg="#4CAF50", fg="white")
login_button.pack(pady=20)

# Profile Picture Section
upload_button = tk.Button(root, text="Choose File", command=upload_profile_picture, state=tk.DISABLED, bg="#FFFFE0", fg="white")
upload_button.pack(pady=5)

reset_pic_button = tk.Button(root, text="Reset Picture", command=reset_profile_picture, state=tk.DISABLED, bg="#FFFFE0", fg="white")
reset_pic_button.pack(pady=5)

profile_label = tk.Label(root, text="No Profile Picture", font=("Arial", 10), bg="#FFFFE0")
profile_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()







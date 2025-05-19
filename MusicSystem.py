import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyodbc
import os

# Database connection setup
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-7RNSP14\SQLEXPRESS;'
    'DATABASE=musicsystemB43;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Initialize database by adding missing columns
def initialize_database():
    try:
        # Check if is_defaucdlt column exists in Playlists table
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Playlists' AND COLUMN_NAME = 'is_default'
            )
            BEGIN
                ALTER TABLE Playlists
                ADD is_default BIT DEFAULT 0;
            END
        """)
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

# Call initialize function
initialize_database()

# Function to create entry fields with labels
def create_labeled_entry(master, label_text):
    frame = tk.Frame(master)
    frame.pack(pady=2)
    label = tk.Label(frame, text=label_text, width=15, anchor='w')
    label.pack(side='left')
    entry = tk.Entry(frame)
    entry.pack(side='left')
    return entry

# Admin Panel with Tabs for Management
def open_admin_panel():
    admin_panel = tk.Toplevel()
    admin_panel.title("Admin Dashboard")
    admin_panel.geometry("1200x800")  # Increased size
    admin_panel.configure(bg='#f0f0f0')  # Light gray background

    # Add back button frame at the top
    back_frame = ttk.Frame(admin_panel)
    back_frame.pack(fill='x', padx=5, pady=5)
    
    def back_to_login():
        admin_panel.destroy()
        # Recreate the login window
        login_window = tk.Tk()
        login_window.title("Music Management System - Login")
        login_window.geometry("400x400")
        
        # Create main frame
        main_frame = tk.Frame(login_window)
        main_frame.pack(pady=40)
        
        # Title Label
        title_label = tk.Label(main_frame, text="Music Management System", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Login Type Selection
        login_type = tk.StringVar(value="user")
        tk.Radiobutton(main_frame, text="User Login", variable=login_type, value="user").pack()
        tk.Radiobutton(main_frame, text="Admin Login", variable=login_type, value="admin").pack()
        
        # Login Frame
        login_frame = tk.Frame(main_frame)
        login_frame.pack(pady=20)
        
        # Username and Password fields
        username_label = tk.Label(login_frame, text="Username:", width=10)
        username_label.grid(row=0, column=0, pady=5)
        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=0, column=1, pady=5)
        
        password_label = tk.Label(login_frame, text="Password:", width=10)
        password_label.grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        def login():
            uname = username_entry.get()
            pwd = password_entry.get()
            login_type_val = login_type.get()
            
            if login_type_val == "admin":
                if uname == "admin" and pwd == "123":
                    messagebox.showinfo("Login", "Welcome Admin!")
                    login_window.destroy()
                    open_admin_panel()
                else:
                    messagebox.showerror("Login Failed", "Invalid admin credentials!")
            else:  # user login
                cursor.execute("SELECT user_id, username FROM Users WHERE username = ? AND password = ? AND user_type = 'user'", uname, pwd)
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("Login", f"Welcome {uname}! You are logged in as a User.")
                    login_window.destroy()
                    launch_main_app(user[0])  # user[0] = user_id
                else:
                    messagebox.showerror("Login Failed", "Invalid user credentials!")
        
        # Login Button
        login_btn = tk.Button(main_frame, text="Login", command=login, width=20)
        login_btn.pack(pady=20)
        
        # Register Button (for new users)
        def open_register():
            register_window = tk.Toplevel(login_window)
            register_window.title("Register New User")
            register_window.geometry("300x250")
            
            # Register fields
            tk.Label(register_window, text="Username:").pack(pady=5)
            reg_username = tk.Entry(register_window)
            reg_username.pack(pady=5)
            
            tk.Label(register_window, text="Password:").pack(pady=5)
            reg_password = tk.Entry(register_window, show="*")
            reg_password.pack(pady=5)
            
            tk.Label(register_window, text="Email:").pack(pady=5)
            reg_email = tk.Entry(register_window)
            reg_email.pack(pady=5)
            
            def register_user():
                try:
                    cursor.execute("INSERT INTO Users (username, password, email, user_type) VALUES (?, ?, ?, 'user')",
                                 reg_username.get(), reg_password.get(), reg_email.get())
                    conn.commit()
                    messagebox.showinfo("Success", "User registered successfully!")
                    register_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Registration failed: {str(e)}")
            
            tk.Button(register_window, text="Register", command=register_user).pack(pady=20)
        
        register_btn = tk.Button(main_frame, text="Register New User", command=open_register)
        register_btn.pack(pady=10)
        
        login_window.mainloop()
    
    back_btn = ttk.Button(back_frame, text="⬅️ Back to Login", command=back_to_login)
    back_btn.pack(side='right', padx=5)

    # Create a style for the notebook
    style = ttk.Style()
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TNotebook.Tab', background='#e0e0e0', padding=[10, 5])
    style.map('TNotebook.Tab', background=[('selected', '#4CAF50')], foreground=[('selected', 'white')])
    
    # Create Excel-like table styles
    style.configure('Table.TFrame', 
                   background='white',
                   relief='solid',
                   borderwidth=1)

    style.configure('TableHeader.TLabel', 
                   background='#4472C4',  # Excel-like blue header
                   foreground='white',
                   font=('Arial', 10, 'bold'),
                   relief='solid',
                   borderwidth=1,
                   padding=5,
                   anchor='center')

    style.configure('TableCell.TLabel', 
                   background='white', 
                   font=('Arial', 10),
                   relief='solid',
                   borderwidth=1,
                   padding=5,
                   anchor='w')

    style.configure('TableCell.TFrame', 
                   relief='solid',
                   borderwidth=1)

    # Remove all hover effects
    style.map('TNotebook.Tab', background=[('selected', '#4CAF50')], foreground=[('selected', 'white')])
    style.map('TableHeader.TLabel', background=[])
    style.map('TableCell.TLabel', background=[])
    style.map('TableCell.TFrame', background=[])
    
    # Create a style for labels
    style.configure('TLabel',
                   background='#f0f0f0',
                   font=('Arial', 10))

    # Create a style for entries
    style.configure('TEntry',
                   padding=5)

    # Create a style for listboxes
    style.configure('TListbox',
                   background='white',
                   font=('Arial', 10))

    tabControl = ttk.Notebook(admin_panel)
    tabControl.pack(expand=1, fill='both', padx=10, pady=10)

    # Create tabs with different background colors
    user_tab = ttk.Frame(tabControl)
    song_tab = ttk.Frame(tabControl)
    artist_tab = ttk.Frame(tabControl)
    album_tab = ttk.Frame(tabControl)
    playlist_tab = ttk.Frame(tabControl)
    mood_tab = ttk.Frame(tabControl)
    query_tab = ttk.Frame(tabControl)  # New tab for SQL queries

    # Configure tab backgrounds
    for tab in [user_tab, song_tab, artist_tab, album_tab, playlist_tab, mood_tab, query_tab]:
        tab.configure(style='TFrame')

    tabControl.add(user_tab, text='👥 Manage Users')
    tabControl.add(song_tab, text='🎵 Manage Songs')
    tabControl.add(artist_tab, text='🎤 Manage Artists')
    tabControl.add(album_tab, text='💿 Manage Albums')
    tabControl.add(playlist_tab, text='📋 Manage Playlists')
    tabControl.add(mood_tab, text='😊 Manage Moods')
    tabControl.add(query_tab, text='🔍 Data Explorer')  # Renamed from SQL Queries to Data Explorer

    # ----- Manage Users -----
    def refresh_users():
        user_listbox.delete(0, tk.END)
        cursor.execute("SELECT user_id, username, email, user_type FROM Users")
        for row in cursor.fetchall():
            user_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    def add_user():
        try:
            cursor.execute("INSERT INTO Users (username, password, email, user_type) VALUES (?, ?, ?, ?)",
                        user_username.get(), user_password.get(), user_email.get(), 'user')
            conn.commit()
            refresh_users()
            messagebox.showinfo("Success", "User added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_user():
        selected = user_listbox.curselection()
        if selected:
            try:
                user_id = int(user_listbox.get(selected[0]).split(" | ")[0])
                cursor.execute("DELETE FROM Users WHERE user_id = ?", user_id)
                conn.commit()
                refresh_users()
                messagebox.showinfo("Success", "User deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create a frame for user management
    user_frame = ttk.Frame(user_tab)
    user_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create input fields with labels
    input_frame = ttk.Frame(user_frame)
    input_frame.pack(fill='x', pady=10)

    ttk.Label(input_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    user_username = ttk.Entry(input_frame)
    user_username.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    user_password = ttk.Entry(input_frame, show="*")
    user_password.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    user_email = ttk.Entry(input_frame)
    user_email.grid(row=2, column=1, padx=5, pady=5)

    # Create buttons
    button_frame = ttk.Frame(user_frame)
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Add User", command=add_user).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete Selected User", command=delete_user).pack(side='left', padx=5)

    # Create listbox with scrollbar
    list_frame = ttk.Frame(user_frame)
    list_frame.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    user_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20)
    user_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=user_listbox.yview)

    refresh_users()

    # ----- Manage Songs -----
    def refresh_songs():
        song_listbox.delete(0, tk.END)
        cursor.execute("""
            SELECT s.song_id, s.song_name, a.artist_name, al.album_name, s.release_year 
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            JOIN Albums al ON s.album_id = al.album_id
        """)
        for row in cursor.fetchall():
            song_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

    def add_song():
        try:
            cursor.execute("""
                INSERT INTO Songs (song_name, artist_id, album_id, release_year, file_path) 
                VALUES (?, ?, ?, ?, ?)
            """, song_name.get(), song_artist.get(), song_album.get(), 
                song_year.get(), song_path.get())
            conn.commit()
            refresh_songs()
            messagebox.showinfo("Success", "Song added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_song():
        selected = song_listbox.curselection()
        if selected:
            try:
                song_id = int(song_listbox.get(selected[0]).split(" | ")[0])
                cursor.execute("DELETE FROM Songs WHERE song_id = ?", song_id)
                conn.commit()
                refresh_songs()
                messagebox.showinfo("Success", "Song deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create a frame for song management
    song_frame = ttk.Frame(song_tab)
    song_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create input fields with labels
    input_frame = ttk.Frame(song_frame)
    input_frame.pack(fill='x', pady=10)

    ttk.Label(input_frame, text="Song Name:").grid(row=0, column=0, padx=5, pady=5)
    song_name = ttk.Entry(input_frame)
    song_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Artist ID:").grid(row=1, column=0, padx=5, pady=5)
    song_artist = ttk.Entry(input_frame)
    song_artist.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Album ID:").grid(row=2, column=0, padx=5, pady=5)
    song_album = ttk.Entry(input_frame)
    song_album.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Release Year:").grid(row=3, column=0, padx=5, pady=5)
    song_year = ttk.Entry(input_frame)
    song_year.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="File Path:").grid(row=4, column=0, padx=5, pady=5)
    song_path = ttk.Entry(input_frame)
    song_path.grid(row=4, column=1, padx=5, pady=5)

    # Create buttons
    button_frame = ttk.Frame(song_frame)
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Add Song", command=add_song).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete Selected Song", command=delete_song).pack(side='left', padx=5)

    # Create listbox with scrollbar
    list_frame = ttk.Frame(song_frame)
    list_frame.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    song_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20)
    song_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=song_listbox.yview)

    refresh_songs()

    # ----- Manage Artists -----
    def refresh_artists():
        artist_listbox.delete(0, tk.END)
        cursor.execute("SELECT artist_id, artist_name, genre FROM Artists")
        for row in cursor.fetchall():
            artist_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")

    def add_artist():
        try:
            cursor.execute("INSERT INTO Artists (artist_name, genre) VALUES (?, ?)",
                        artist_name.get(), artist_genre.get())
            conn.commit()
            refresh_artists()
            messagebox.showinfo("Success", "Artist added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_artist():
        selected = artist_listbox.curselection()
        if selected:
            try:
                artist_id = int(artist_listbox.get(selected[0]).split(" | ")[0])
                cursor.execute("DELETE FROM Artists WHERE artist_id = ?", artist_id)
                conn.commit()
                refresh_artists()
                messagebox.showinfo("Success", "Artist deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create a frame for artist management
    artist_frame = ttk.Frame(artist_tab)
    artist_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create input fields with labels
    input_frame = ttk.Frame(artist_frame)
    input_frame.pack(fill='x', pady=10)

    ttk.Label(input_frame, text="Artist Name:").grid(row=0, column=0, padx=5, pady=5)
    artist_name = ttk.Entry(input_frame)
    artist_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Genre:").grid(row=1, column=0, padx=5, pady=5)
    artist_genre = ttk.Entry(input_frame)
    artist_genre.grid(row=1, column=1, padx=5, pady=5)

    # Create buttons
    button_frame = ttk.Frame(artist_frame)
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Add Artist", command=add_artist).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete Selected Artist", command=delete_artist).pack(side='left', padx=5)

    # Create listbox with scrollbar
    list_frame = ttk.Frame(artist_frame)
    list_frame.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    artist_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20)
    artist_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=artist_listbox.yview)

    refresh_artists()

    # ----- Manage Albums -----
    def refresh_albums():
        album_listbox.delete(0, tk.END)
        cursor.execute("""
            SELECT a.album_id, a.album_name, ar.artist_name, a.release_year 
            FROM Albums a
            JOIN Artists ar ON a.artist_id = ar.artist_id
        """)
        for row in cursor.fetchall():
            album_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    def add_album():
        try:
            cursor.execute("INSERT INTO Albums (album_name, artist_id, release_year) VALUES (?, ?, ?)",
                        album_name.get(), album_artist.get(), album_year.get())
            conn.commit()
            refresh_albums()
            messagebox.showinfo("Success", "Album added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_album():
        selected = album_listbox.curselection()
        if selected:
            try:
                album_id = int(album_listbox.get(selected[0]).split(" | ")[0])
                cursor.execute("DELETE FROM Albums WHERE album_id = ?", album_id)
                conn.commit()
                refresh_albums()
                messagebox.showinfo("Success", "Album deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create a frame for album management
    album_frame = ttk.Frame(album_tab)
    album_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create input fields with labels
    input_frame = ttk.Frame(album_frame)
    input_frame.pack(fill='x', pady=10)

    ttk.Label(input_frame, text="Album Name:").grid(row=0, column=0, padx=5, pady=5)
    album_name = ttk.Entry(input_frame)
    album_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Artist ID:").grid(row=1, column=0, padx=5, pady=5)
    album_artist = ttk.Entry(input_frame)
    album_artist.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Release Year:").grid(row=2, column=0, padx=5, pady=5)
    album_year = ttk.Entry(input_frame)
    album_year.grid(row=2, column=1, padx=5, pady=5)

    # Create buttons
    button_frame = ttk.Frame(album_frame)
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Add Album", command=add_album).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete Selected Album", command=delete_album).pack(side='left', padx=5)

    # Create listbox with scrollbar
    list_frame = ttk.Frame(album_frame)
    list_frame.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    album_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20)
    album_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=album_listbox.yview)

    refresh_albums()

    # ----- Manage Playlists (Admin) -----
    def refresh_playlists():
        # Clear all widgets first
        for widget in playlist_tab.winfo_children():
            widget.destroy()
        
        # Add a message about the missing column
        info_frame = ttk.Frame(playlist_tab)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(info_frame, text="Playlist Management", 
                font=('Arial', 14, 'bold')).pack(side='left')
        
        # Add buttons at the top
        button_frame = ttk.Frame(playlist_tab)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Create Default Playlist", command=create_user_playlist).pack(side='left', padx=5)
        
        # Create a table-like display with headers
        headers_frame = ttk.Frame(playlist_tab, style='Table.TFrame')
        headers_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(headers_frame, text="ID", width=10, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
        ttk.Label(headers_frame, text="Playlist Name", width=30, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
        ttk.Label(headers_frame, text="User", width=20, style='TableHeader.TLabel').grid(row=0, column=2, sticky="nsew")
        ttk.Label(headers_frame, text="Type", width=15, style='TableHeader.TLabel').grid(row=0, column=3, sticky="nsew")
        ttk.Label(headers_frame, text="Actions", width=25, style='TableHeader.TLabel').grid(row=0, column=4, sticky="nsew")
        
        # Configure grid weights to eliminate hover effect
        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_columnconfigure(1, weight=3)
        headers_frame.grid_columnconfigure(2, weight=2)
        headers_frame.grid_columnconfigure(3, weight=1)
        headers_frame.grid_columnconfigure(4, weight=2)
        
        # Create a frame for playlist list with fixed height
        list_frame = ttk.Frame(playlist_tab)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create canvas with fixed width and height
        canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Make sure the frame takes the full width of the canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        try:
            # Get all playlists for admin view
            cursor.execute("""
                SELECT p.playlist_id, p.playlist_name, u.username, p.is_default
                FROM Playlists p
                JOIN Users u ON p.user_id = u.user_id
                ORDER BY p.is_default DESC, u.username, p.playlist_name
            """)
            playlists = cursor.fetchall()
            
            # Configure grid weights in scrollable frame to prevent hover effect
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=3)
            scrollable_frame.grid_columnconfigure(2, weight=2)
            scrollable_frame.grid_columnconfigure(3, weight=1)
            scrollable_frame.grid_columnconfigure(4, weight=2)
            
            # If no playlists found
            if not playlists:
                ttk.Label(scrollable_frame, text="No playlists found", font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
            else:
                # Display each playlist in a table-like format
                for i, (playlist_id, playlist_name, username, is_default) in enumerate(playlists):
                    row = i + 1  # Start from row 1 (row 0 is for headers)
                    
                    # Create cells with border to look like a table
                    ttk.Label(scrollable_frame, text=str(playlist_id), width=10, style='TableCell.TLabel').grid(row=row, column=0, sticky="nsew")
                    ttk.Label(scrollable_frame, text=playlist_name, width=30, style='TableCell.TLabel').grid(row=row, column=1, sticky="nsew")
                    ttk.Label(scrollable_frame, text=username, width=20, style='TableCell.TLabel').grid(row=row, column=2, sticky="nsew")
                    
                    # Show playlist type
                    playlist_type = "Default" if is_default else "User"
                    ttk.Label(scrollable_frame, text=playlist_type, width=15, style='TableCell.TLabel').grid(row=row, column=3, sticky="nsew")
                    
                    # Actions frame
                    actions_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    actions_frame.grid(row=row, column=4, sticky="nsew")
                    
                    # View button
                    view_btn = ttk.Button(actions_frame, text='View Songs', 
                                       command=lambda pid=playlist_id: view_playlist_songs(pid))
                    view_btn.pack(side='left', padx=3, pady=3)
                    
                    # Delete button - for all playlists
                    delete_btn = ttk.Button(actions_frame, text='Delete', 
                                         command=lambda pid=playlist_id: delete_playlist(pid))
                    delete_btn.pack(side='left', padx=3, pady=3)
                    
                    # Set row height for consistent display
                    scrollable_frame.grid_rowconfigure(row, minsize=40)
        except Exception as e:
            messagebox.showerror("Error Loading Playlists", str(e))
            ttk.Label(scrollable_frame, text=f"Error: {str(e)}", foreground="red", style='TableCell.TLabel').grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

    def create_user_playlist():
        playlist_name = simpledialog.askstring("New Default Playlist", "Enter default playlist name:")
        if playlist_name:
            try:
                # Get admin user ID
                cursor.execute("SELECT user_id FROM Users WHERE username = 'admin'")
                admin_id = cursor.fetchone()[0]
                
                # Create a playlist with admin as owner (default for all users)
                cursor.execute("INSERT INTO Playlists (user_id, playlist_name, is_default) VALUES (?, ?, 1)", 
                             admin_id, playlist_name)
                conn.commit()
                refresh_playlists()
                messagebox.showinfo("Success", f"Default playlist '{playlist_name}' created successfully. This playlist will be available to all users.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_playlist(playlist_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this playlist?"):
            try:
                # Check if it's a default playlist
                cursor.execute("SELECT is_default FROM Playlists WHERE playlist_id = ?", playlist_id)
                is_default = cursor.fetchone()[0]
                
                # First delete related entries in Playlist_Songs
                cursor.execute("DELETE FROM Playlist_Songs WHERE playlist_id = ?", playlist_id)
                # Then delete the playlist
                cursor.execute("DELETE FROM Playlists WHERE playlist_id = ?", playlist_id)
                conn.commit()
                
                if is_default:
                    messagebox.showinfo("Success", "Default playlist deleted successfully. This change affects all users.")
                else:
                    messagebox.showinfo("Success", "User playlist deleted successfully")
                
                refresh_playlists()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def add_songs_to_playlist(playlist_id):
        add_window = tk.Toplevel(admin_panel)
        add_window.title("Add Songs to Playlist")
        add_window.geometry("800x600")
        add_window.configure(bg='#f0f0f0')
        
        try:
            # Get songs not in the playlist
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                WHERE s.song_id NOT IN (
                    SELECT song_id FROM Playlist_Songs WHERE playlist_id = ?
                )
            """, playlist_id)
            
            available_songs = cursor.fetchall()
            
            # Create title
            ttk.Label(add_window, text="Add Songs to Playlist", 
                    font=('Arial', 14, 'bold')).pack(pady=10)
            
            # Create search box
            search_frame = ttk.Frame(add_window)
            search_frame.pack(fill='x', padx=20, pady=10)
            
            ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
            search_entry = ttk.Entry(search_frame, width=40)
            search_entry.pack(side='left', padx=5)
            
            # Create headers
            headers_frame = ttk.Frame(add_window, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=20, pady=5)
            
            ttk.Label(headers_frame, text="ID", width=8, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
            ttk.Label(headers_frame, text="Song", width=30, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
            ttk.Label(headers_frame, text="Artist", width=20, style='TableHeader.TLabel').grid(row=0, column=2, sticky="nsew")
            ttk.Label(headers_frame, text="Album", width=20, style='TableHeader.TLabel').grid(row=0, column=3, sticky="nsew")
            ttk.Label(headers_frame, text="Add", width=10, style='TableHeader.TLabel').grid(row=0, column=4, sticky="nsew")
            
            # Configure grid weights to eliminate hover effect
            headers_frame.grid_columnconfigure(0, weight=1)
            headers_frame.grid_columnconfigure(1, weight=3)
            headers_frame.grid_columnconfigure(2, weight=2)
            headers_frame.grid_columnconfigure(3, weight=2)
            headers_frame.grid_columnconfigure(4, weight=1)
            
            # Create scrollable frame
            canvas = tk.Canvas(add_window, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            # Make sure the frame takes the full width of the canvas
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=20, pady=5)
            scrollbar.pack(side="right", fill="y", pady=5)
            
            # Configure grid weights in scrollable frame to prevent hover effect
            scrollable_frame.grid_columnconfigure(0, weight=3)
            scrollable_frame.grid_columnconfigure(1, weight=2)
            scrollable_frame.grid_columnconfigure(2, weight=2)
            scrollable_frame.grid_columnconfigure(3, weight=2)
            scrollable_frame.grid_columnconfigure(4, weight=1)
            
            if not available_songs:
                ttk.Label(scrollable_frame, text="All songs are already in this playlist", 
                        font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            else:
                # Function to add song to playlist
                def add_song_to_db(playlist_id, song_id):
                    try:
                        cursor.execute("INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES (?, ?)", 
                                    playlist_id, song_id)
                        conn.commit()
                        messagebox.showinfo("Success", "Song added to playlist")
                        add_window.destroy()
                        if parent_window:
                            parent_window.destroy()
                            view_user_playlist(playlist_id)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                
                # Function to filter songs based on search
                def filter_songs(*args):
                    search_term = search_entry.get().lower()
                    
                    # Clear existing rows
                    for widget in scrollable_frame.winfo_children():
                        widget.destroy()
                    
                    # Filter and display songs
                    filtered_songs = [song for song in available_songs if 
                                    search_term in song[1].lower() or 
                                    search_term in song[2].lower() or 
                                    search_term in song[3].lower()]
                    
                    if not filtered_songs:
                        ttk.Label(scrollable_frame, text="No matching songs found", 
                                font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
                    else:
                        for i, (song_id, song_name, artist_name, album_name) in enumerate(filtered_songs):
                            ttk.Label(scrollable_frame, text=song_name, width=30, 
                                   style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                            ttk.Label(scrollable_frame, text=artist_name, width=20, 
                                   style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                            ttk.Label(scrollable_frame, text=album_name, width=20, 
                                   style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                            
                            add_btn_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                            add_btn_frame.grid(row=i, column=3, sticky="nsew")
                            
                            ttk.Button(add_btn_frame, text='➕ Add', 
                                    command=lambda sid=song_id: add_song_to_db(playlist_id, sid)).pack(padx=2, pady=2)
                            
                            # Set row height
                            scrollable_frame.grid_rowconfigure(i, minsize=40)
                
                # Bind search entry to filter function
                search_entry.bind("<KeyRelease>", filter_songs)
                
                # Initial display of all songs
                for i, (song_id, song_name, artist_name, album_name) in enumerate(available_songs):
                    ttk.Label(scrollable_frame, text=song_name, width=30, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    ttk.Label(scrollable_frame, text=artist_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                    ttk.Label(scrollable_frame, text=album_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                    
                    add_btn_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    add_btn_frame.grid(row=i, column=3, sticky="nsew")
                    
                    ttk.Button(add_btn_frame, text='➕ Add', 
                            command=lambda sid=song_id: add_song_to_db(playlist_id, sid)).pack(padx=2, pady=2)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def remove_from_playlist(playlist_id, song_id, window):
        try:
            cursor.execute("DELETE FROM Playlist_Songs WHERE playlist_id = ? AND song_id = ?", 
                        playlist_id, song_id)
            conn.commit()
            messagebox.showinfo("Success", "Song removed from playlist")
            
            if window:
                window.destroy()
                view_playlist_songs(playlist_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    # Call refresh_playlists to initialize the tab
    refresh_playlists()

    # ----- Manage Moods -----
    def refresh_moods():
        mood_listbox.delete(0, tk.END)
        cursor.execute("SELECT mood_id, mood_name FROM Moods")
        for row in cursor.fetchall():
            mood_listbox.insert(tk.END, f"{row[0]} | {row[1]}")

    def add_mood():
        try:
            cursor.execute("INSERT INTO Moods (mood_name) VALUES (?)",
                        mood_name.get())
            conn.commit()
            refresh_moods()
            messagebox.showinfo("Success", "Mood added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_mood():
        selected = mood_listbox.curselection()
        if selected:
            try:
                mood_id = int(mood_listbox.get(selected[0]).split(" | ")[0])
                cursor.execute("DELETE FROM Moods WHERE mood_id = ?", mood_id)
                conn.commit()
                refresh_moods()
                messagebox.showinfo("Success", "Mood deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create a frame for mood management
    mood_frame = ttk.Frame(mood_tab)
    mood_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create input fields with labels
    input_frame = ttk.Frame(mood_frame)
    input_frame.pack(fill='x', pady=10)

    ttk.Label(input_frame, text="Mood Name:").grid(row=0, column=0, padx=5, pady=5)
    mood_name = ttk.Entry(input_frame)
    mood_name.grid(row=0, column=1, padx=5, pady=5)

    # Create buttons
    button_frame = ttk.Frame(mood_frame)
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Add Mood", command=add_mood).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete Selected Mood", command=delete_mood).pack(side='left', padx=5)

    # Create listbox with scrollbar
    list_frame = ttk.Frame(mood_frame)
    list_frame.pack(fill='both', expand=True)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')

    mood_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20)
    mood_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=mood_listbox.yview)

    refresh_moods()

    # Add view_playlist_songs function for admin
    def view_playlist_songs(playlist_id):
        """Admin function to view playlist songs - with proper permissions for default playlists"""
        playlist_window = tk.Toplevel(admin_panel)
        playlist_window.title("Playlist Songs")
        playlist_window.geometry("900x600")
        playlist_window.configure(bg='#f0f0f0')
        
        try:
            # Get playlist name and check if it's a default playlist
            cursor.execute("SELECT playlist_name, is_default FROM Playlists WHERE playlist_id = ?", playlist_id)
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Playlist not found")
                return
            
            playlist_name, is_default = result
            
            # Create title frame
            title_frame = ttk.Frame(playlist_window)
            title_frame.pack(fill='x', padx=20, pady=10)
            
            playlist_type = "Default Playlist" if is_default else "User Playlist"
            ttk.Label(title_frame, text=f"{playlist_type}: {playlist_name}", 
                    font=('Arial', 14, 'bold')).pack(side='left')
            
            # Add button frame
            button_frame = ttk.Frame(playlist_window)
            button_frame.pack(fill='x', padx=20, pady=5)
            
            # Always allow add for default playlists or admin viewing any playlist
            if is_default:
                ttk.Button(button_frame, text='➕ Add Songs', 
                         command=lambda: add_songs_to_playlist(playlist_id)).pack(side='right')
            
            # Create a frame for the song list
            song_list_frame = ttk.Frame(playlist_window)
            song_list_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Create headers
            headers_frame = ttk.Frame(song_list_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', pady=5)
            
            ttk.Label(headers_frame, text="Song", width=30, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
            ttk.Label(headers_frame, text="Artist", width=20, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
            ttk.Label(headers_frame, text="Album", width=20, style='TableHeader.TLabel').grid(row=0, column=2, sticky="nsew")
            ttk.Label(headers_frame, text="Actions", width=20, style='TableHeader.TLabel').grid(row=0, column=3, sticky="nsew")
            
            # Configure grid weights
            headers_frame.grid_columnconfigure(0, weight=3)
            headers_frame.grid_columnconfigure(1, weight=2)
            headers_frame.grid_columnconfigure(2, weight=2)
            headers_frame.grid_columnconfigure(3, weight=2)
            
            # Create scrollable frame for songs
            canvas = tk.Canvas(song_list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(song_list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            scrollable_frame.grid_columnconfigure(0, weight=3)
            scrollable_frame.grid_columnconfigure(1, weight=2)
            scrollable_frame.grid_columnconfigure(2, weight=2)
            scrollable_frame.grid_columnconfigure(3, weight=2)
            
            # Get songs in playlist
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                JOIN Playlist_Songs ps ON s.song_id = ps.song_id
                WHERE ps.playlist_id = ?
            """, playlist_id)
            
            songs = cursor.fetchall()
            
            if not songs:
                ttk.Label(scrollable_frame, text="No songs in this playlist", 
                        font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            else:
                for i, (song_id, song_name, artist_name, album_name) in enumerate(songs):
                    ttk.Label(scrollable_frame, text=song_name, width=30, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    ttk.Label(scrollable_frame, text=artist_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                    ttk.Label(scrollable_frame, text=album_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                    
                    # Actions frame
                    actions_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    actions_frame.grid(row=i, column=3, sticky="nsew")
                    
                    ttk.Button(actions_frame, text='▶ Play', 
                             command=lambda sid=song_id: play_song(sid)).pack(side='left', padx=2, pady=2)
                    
                    # Always allow remove for default playlists or admin viewing any playlist
                    if is_default:
                        ttk.Button(actions_frame, text='❌ Remove', 
                                command=lambda pid=playlist_id, sid=song_id: remove_from_playlist(pid, sid, playlist_window)).pack(side='left', padx=2, pady=2)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ----- Data Explorer Tab -----
    def setup_data_explorer():
        # Clear previous contents
        for widget in query_tab.winfo_children():
            widget.destroy()
            
        # Create main layout with tabs for different query types
        explorer_notebook = ttk.Notebook(query_tab)
        explorer_notebook.pack(expand=1, fill='both', padx=10, pady=10)
        
        # Create tabs for different query types
        view_tab = ttk.Frame(explorer_notebook)
        join_tab = ttk.Frame(explorer_notebook)
        pattern_tab = ttk.Frame(explorer_notebook)
        order_tab = ttk.Frame(explorer_notebook)
        group_tab = ttk.Frame(explorer_notebook)
        
        explorer_notebook.add(view_tab, text='View Table')
        explorer_notebook.add(join_tab, text='Join Tables')
        explorer_notebook.add(pattern_tab, text='Pattern Matching')
        explorer_notebook.add(order_tab, text='Sort & Filter')
        explorer_notebook.add(group_tab, text='Group & Aggregate')
        
        # Setup individual tabs
        setup_view_tab(view_tab)
        setup_join_tab(join_tab)
        setup_pattern_tab(pattern_tab)
        setup_order_tab(order_tab)
        setup_group_tab(group_tab)
        
    # Tab 1: View Table
    def setup_view_tab(parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(frame, text="View Table Data", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Table selection
        select_frame = ttk.Frame(frame)
        select_frame.pack(fill='x', pady=10)
        
        ttk.Label(select_frame, text="Select Table:").pack(side='left', padx=5)
        
        # Table names
        tables = ["Users", "Artists", "Albums", "Songs", "Moods", "Playlists", "Playlist_Songs", "Favorites"]
        table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(select_frame, textvariable=table_var, values=tables, state="readonly", width=30)
        table_dropdown.pack(side='left', padx=5)
        table_dropdown.current(0)
        
        # View button
        ttk.Button(select_frame, text="View Data", 
                 command=lambda: view_table_data(table_var.get(), results_frame)).pack(side='left', padx=20)
        
        # Results area
        ttk.Label(frame, text="Table Contents:").pack(anchor='w', pady=5)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill='both', expand=True, pady=5)
        
    def view_table_data(table_name, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Get table schema to get column names
            cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
            column_names = [column[0] for column in cursor.description]
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                ttk.Label(results_frame, text=f"No data found in {table_name}", 
                       font=('Arial', 12)).pack(pady=20)
                return
                
            # Create a table-like display with headers
            headers_frame = ttk.Frame(results_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=10, pady=5)
            
            # Create headers
            for col, header in enumerate(column_names):
                ttk.Label(headers_frame, text=header, width=15, style='TableHeader.TLabel').grid(row=0, column=col, sticky="nsew")
                headers_frame.grid_columnconfigure(col, weight=1)
            
            # Create scrollable frame for results
            list_frame = ttk.Frame(results_frame)
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            for col in range(len(column_names)):
                scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Display results
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    cell_frame.grid(row=i, column=j, sticky="nsew")
                    
                    # Alternate row colors
                    if i % 2 == 0:
                        bg_color = 'white'
                    else:
                        bg_color = '#F2F2F2'
                    
                    ttk.Label(cell_frame, text=str(value), background=bg_color, 
                           style='TableCell.TLabel').pack(fill='both', expand=True)
                
                # Set row height
                scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            ttk.Label(results_frame, text=f"Error viewing table: {str(e)}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)
    
    # Tab 2: Join Tables
    def setup_join_tab(parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(frame, text="Join Tables", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Tables selection
        tables_frame = ttk.Frame(frame)
        tables_frame.pack(fill='x', pady=10)
        
        tables = ["Users", "Artists", "Albums", "Songs", "Moods", "Playlists", "Playlist_Songs", "Favorites"]
        
        # Table 1
        ttk.Label(tables_frame, text="First Table:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        table1_var = tk.StringVar()
        table1_dropdown = ttk.Combobox(tables_frame, textvariable=table1_var, values=tables, state="readonly", width=20)
        table1_dropdown.grid(row=0, column=1, padx=5, pady=5)
        table1_dropdown.current(0)
        
        # Table 2
        ttk.Label(tables_frame, text="Second Table:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        table2_var = tk.StringVar()
        table2_dropdown = ttk.Combobox(tables_frame, textvariable=table2_var, values=tables, state="readonly", width=20)
        table2_dropdown.grid(row=1, column=1, padx=5, pady=5)
        table2_dropdown.current(1)
        
        # Join Type
        ttk.Label(tables_frame, text="Join Type:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        join_types = ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"]
        join_var = tk.StringVar()
        join_dropdown = ttk.Combobox(tables_frame, textvariable=join_var, values=join_types, state="readonly", width=20)
        join_dropdown.grid(row=2, column=1, padx=5, pady=5)
        join_dropdown.current(0)
        
        # Join On (ID fields)
        ttk.Label(tables_frame, text="Join On:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        join_on_frame = ttk.Frame(tables_frame)
        join_on_frame.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        join_on_var = tk.StringVar(value="automatic")
        ttk.Radiobutton(join_on_frame, text="Automatic (ID fields)", variable=join_on_var, value="automatic").pack(anchor='w')
        ttk.Radiobutton(join_on_frame, text="Manual (select columns)", variable=join_on_var, value="manual").pack(anchor='w')
        
        # Execute button
        ttk.Button(tables_frame, text="View Joined Data", 
                 command=lambda: join_tables(table1_var.get(), table2_var.get(), join_var.get(), 
                                           join_on_var.get(), results_frame)).grid(row=4, column=0, columnspan=2, pady=15)
        
        # Results area
        ttk.Label(frame, text="Join Results:").pack(anchor='w', pady=5)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill='both', expand=True, pady=5)
        
    def join_tables(table1, table2, join_type, join_method, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Determine join condition automatically
            join_on = ""
            if join_method == "automatic":
                # Common join patterns
                join_patterns = {
                    ("Users", "Playlists"): "Users.user_id = Playlists.user_id",
                    ("Playlists", "Users"): "Playlists.user_id = Users.user_id",
                    ("Songs", "Artists"): "Songs.artist_id = Artists.artist_id",
                    ("Artists", "Songs"): "Artists.artist_id = Songs.artist_id",
                    ("Songs", "Albums"): "Songs.album_id = Albums.album_id",
                    ("Albums", "Songs"): "Albums.album_id = Songs.album_id",
                    ("Albums", "Artists"): "Albums.artist_id = Artists.artist_id",
                    ("Artists", "Albums"): "Artists.artist_id = Albums.artist_id",
                    ("Songs", "Playlist_Songs"): "Songs.song_id = Playlist_Songs.song_id",
                    ("Playlist_Songs", "Songs"): "Playlist_Songs.song_id = Songs.song_id",
                    ("Playlists", "Playlist_Songs"): "Playlists.playlist_id = Playlist_Songs.playlist_id",
                    ("Playlist_Songs", "Playlists"): "Playlist_Songs.playlist_id = Playlists.playlist_id",
                    ("Users", "Favorites"): "Users.user_id = Favorites.user_id",
                    ("Favorites", "Users"): "Favorites.user_id = Users.user_id",
                    ("Songs", "Favorites"): "Songs.song_id = Favorites.song_id",
                    ("Favorites", "Songs"): "Favorites.song_id = Songs.song_id"
                }
                
                if (table1, table2) in join_patterns:
                    join_on = join_patterns[(table1, table2)]
                else:
                    # Try common ID patterns
                    join_on = f"{table1}.{table1[:-1].lower()}_id = {table2}.{table1[:-1].lower()}_id"
                
            # SQL Join query
            query = f"""
                SELECT * 
                FROM {table1} 
                {join_type} {table2} 
                ON {join_on}
            """
            
            # Execute join query
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            
            if not rows:
                ttk.Label(results_frame, text=f"No results found for the join", 
                       font=('Arial', 12)).pack(pady=20)
                return
                
            # Create a table-like display with headers
            headers_frame = ttk.Frame(results_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=10, pady=5)
            
            # Create headers
            for col, header in enumerate(column_names):
                ttk.Label(headers_frame, text=header, width=15, style='TableHeader.TLabel').grid(row=0, column=col, sticky="nsew")
                headers_frame.grid_columnconfigure(col, weight=1)
            
            # Create scrollable frame for results
            list_frame = ttk.Frame(results_frame)
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            for col in range(len(column_names)):
                scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Display results
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    cell_frame.grid(row=i, column=j, sticky="nsew")
                    
                    # Alternate row colors
                    if i % 2 == 0:
                        bg_color = 'white'
                    else:
                        bg_color = '#F2F2F2'
                    
                    ttk.Label(cell_frame, text=str(value), background=bg_color, 
                           style='TableCell.TLabel').pack(fill='both', expand=True)
                
                # Set row height
                scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            ttk.Label(results_frame, text=f"Error executing join: {str(e)}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)
    
    # Tab 3: Pattern Matching
    def setup_pattern_tab(parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(frame, text="Pattern Matching Search", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Search configuration
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', pady=10)
        
        # Table selection
        tables = ["Users", "Artists", "Albums", "Songs", "Moods", "Playlists"]
        
        ttk.Label(search_frame, text="Search In:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(search_frame, textvariable=table_var, values=tables, state="readonly", width=20)
        table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        table_dropdown.current(0)
        
        # Column selection (will be populated based on table selection)
        ttk.Label(search_frame, text="Column:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        column_var = tk.StringVar()
        column_dropdown = ttk.Combobox(search_frame, textvariable=column_var, width=20)
        column_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Update columns when table changes
        def update_columns(*args):
            try:
                cursor.execute(f"SELECT * FROM {table_var.get()} WHERE 1=0")
                columns = [col[0] for col in cursor.description]
                column_dropdown['values'] = columns
                if columns:
                    column_dropdown.current(0)
            except Exception as e:
                column_dropdown['values'] = []
                
        table_var.trace('w', update_columns)
        # Initialize columns
        update_columns()
        
        # Pattern matching type
        ttk.Label(search_frame, text="Match Type:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        pattern_types = [
            "Starts with...", 
            "Contains...", 
            "Ends with...", 
            "Exactly matches..."
        ]
        pattern_var = tk.StringVar()
        pattern_dropdown = ttk.Combobox(search_frame, textvariable=pattern_var, values=pattern_types, state="readonly", width=20)
        pattern_dropdown.grid(row=2, column=1, padx=5, pady=5)
        pattern_dropdown.current(0)
        
        # Search text
        ttk.Label(search_frame, text="Search Text:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        search_text = ttk.Entry(search_frame, width=30)
        search_text.grid(row=3, column=1, padx=5, pady=5)
        
        # Search button
        ttk.Button(search_frame, text="Search", 
                 command=lambda: pattern_search(table_var.get(), column_var.get(), pattern_var.get(), 
                                              search_text.get(), results_frame)).grid(row=4, column=0, columnspan=2, pady=15)
        
        # Results area
        ttk.Label(frame, text="Search Results:").pack(anchor='w', pady=5)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill='both', expand=True, pady=5)
        
    def pattern_search(table, column, pattern_type, search_text, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Build pattern for LIKE clause
            pattern = ""
            if pattern_type == "Starts with...":
                pattern = f"{search_text}%"
            elif pattern_type == "Contains...":
                pattern = f"%{search_text}%"
            elif pattern_type == "Ends with...":
                pattern = f"%{search_text}"
            elif pattern_type == "Exactly matches...":
                pattern = search_text
            
            # Execute search query
            query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
            cursor.execute(query, [pattern])
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            
            if not rows:
                ttk.Label(results_frame, text=f"No matches found", 
                       font=('Arial', 12)).pack(pady=20)
                return
                
            # Create a table-like display with headers
            headers_frame = ttk.Frame(results_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=10, pady=5)
            
            # Create headers
            for col, header in enumerate(column_names):
                ttk.Label(headers_frame, text=header, width=15, style='TableHeader.TLabel').grid(row=0, column=col, sticky="nsew")
                headers_frame.grid_columnconfigure(col, weight=1)
            
            # Create scrollable frame for results
            list_frame = ttk.Frame(results_frame)
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            for col in range(len(column_names)):
                scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Display results
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    cell_frame.grid(row=i, column=j, sticky="nsew")
                    
                    # Alternate row colors
                    if i % 2 == 0:
                        bg_color = 'white'
                    else:
                        bg_color = '#F2F2F2'
                    
                    ttk.Label(cell_frame, text=str(value), background=bg_color, 
                           style='TableCell.TLabel').pack(fill='both', expand=True)
                
                # Set row height
                scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            ttk.Label(results_frame, text=f"Error executing search: {str(e)}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)
    
    # Tab 4: Sort & Filter (Order By)
    def setup_order_tab(parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(frame, text="Sort & Filter Data", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Configuration
        config_frame = ttk.Frame(frame)
        config_frame.pack(fill='x', pady=10)
        
        # Table selection
        tables = ["Users", "Artists", "Albums", "Songs", "Moods", "Playlists"]
        
        ttk.Label(config_frame, text="Table:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(config_frame, textvariable=table_var, values=tables, state="readonly", width=20)
        table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        table_dropdown.current(0)
        
        # Column selection (will be populated based on table selection)
        ttk.Label(config_frame, text="Sort By:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        sort_column_var = tk.StringVar()
        sort_column_dropdown = ttk.Combobox(config_frame, textvariable=sort_column_var, width=20)
        sort_column_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Sort order
        ttk.Label(config_frame, text="Order:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        sort_orders = ["Ascending (A-Z, 1-9)", "Descending (Z-A, 9-1)"]
        sort_order_var = tk.StringVar()
        sort_order_dropdown = ttk.Combobox(config_frame, textvariable=sort_order_var, values=sort_orders, state="readonly", width=20)
        sort_order_dropdown.grid(row=2, column=1, padx=5, pady=5)
        sort_order_dropdown.current(0)
        
        # Filter option
        ttk.Label(config_frame, text="Filter By:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        filter_column_var = tk.StringVar()
        filter_column_dropdown = ttk.Combobox(config_frame, textvariable=filter_column_var, width=20)
        filter_column_dropdown.grid(row=3, column=1, padx=5, pady=5)
        
        # Filter condition
        filter_conditions = ["equals", "greater than", "less than", "contains"]
        filter_condition_var = tk.StringVar()
        filter_condition_dropdown = ttk.Combobox(config_frame, textvariable=filter_condition_var, 
                                              values=filter_conditions, state="readonly", width=15)
        filter_condition_dropdown.grid(row=3, column=2, padx=5, pady=5)
        filter_condition_dropdown.current(0)
        
        # Filter value
        filter_value = ttk.Entry(config_frame, width=15)
        filter_value.grid(row=3, column=3, padx=5, pady=5)
        
        # Update columns when table changes
        def update_columns(*args):
            try:
                cursor.execute(f"SELECT * FROM {table_var.get()} WHERE 1=0")
                columns = [col[0] for col in cursor.description]
                sort_column_dropdown['values'] = columns
                filter_column_dropdown['values'] = columns
                if columns:
                    sort_column_dropdown.current(0)
                    filter_column_dropdown.current(0)
            except Exception as e:
                sort_column_dropdown['values'] = []
                filter_column_dropdown['values'] = []
                
        table_var.trace('w', update_columns)
        # Initialize columns
        update_columns()
        
        # Execute button
        ttk.Button(config_frame, text="View Sorted & Filtered Data", 
                 command=lambda: execute_sort_filter(
                     table_var.get(), 
                     sort_column_var.get(), 
                     sort_order_var.get(), 
                     filter_column_var.get(), 
                     filter_condition_var.get(), 
                     filter_value.get(), 
                     results_frame)).grid(row=4, column=0, columnspan=4, pady=15)
        
        # Results area
        ttk.Label(frame, text="Results:").pack(anchor='w', pady=5)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill='both', expand=True, pady=5)
    
    def execute_sort_filter(table, sort_column, sort_order, filter_column, filter_condition, filter_value, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Build SQL query
            query = f"SELECT * FROM {table}"
            params = []
            
            # Add filter if provided
            if filter_column and filter_condition and filter_value:
                if filter_condition == "equals":
                    query += f" WHERE {filter_column} = ?"
                    params.append(filter_value)
                elif filter_condition == "greater than":
                    query += f" WHERE {filter_column} > ?"
                    params.append(filter_value)
                elif filter_condition == "less than":
                    query += f" WHERE {filter_column} < ?"
                    params.append(filter_value)
                elif filter_condition == "contains":
                    query += f" WHERE {filter_column} LIKE ?"
                    params.append(f"%{filter_value}%")
            
            # Add sort
            if sort_column:
                order_direction = "DESC" if sort_order.startswith("Descending") else "ASC"
                query += f" ORDER BY {sort_column} {order_direction}"
                
            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            
            if not rows:
                ttk.Label(results_frame, text=f"No data found", 
                       font=('Arial', 12)).pack(pady=20)
                return
                
            # Create a table-like display with headers
            headers_frame = ttk.Frame(results_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=10, pady=5)
            
            # Create headers
            for col, header in enumerate(column_names):
                ttk.Label(headers_frame, text=header, width=15, style='TableHeader.TLabel').grid(row=0, column=col, sticky="nsew")
                headers_frame.grid_columnconfigure(col, weight=1)
            
            # Create scrollable frame for results
            list_frame = ttk.Frame(results_frame)
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            for col in range(len(column_names)):
                scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Display results
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    cell_frame.grid(row=i, column=j, sticky="nsew")
                    
                    # Alternate row colors
                    if i % 2 == 0:
                        bg_color = 'white'
                    else:
                        bg_color = '#F2F2F2'
                    
                    ttk.Label(cell_frame, text=str(value), background=bg_color, 
                           style='TableCell.TLabel').pack(fill='both', expand=True)
                
                # Set row height
                scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            ttk.Label(results_frame, text=f"Error: {str(e)}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)

    # Tab 5: Group & Aggregate
    def setup_group_tab(parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(frame, text="Group & Aggregate Data", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Configuration
        config_frame = ttk.Frame(frame)
        config_frame.pack(fill='x', pady=10)
        
        # Table selection
        tables = ["Songs", "Albums", "Artists", "Playlists", "Playlist_Songs", "Favorites"]
        
        ttk.Label(config_frame, text="Table:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(config_frame, textvariable=table_var, values=tables, state="readonly", width=20)
        table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        table_dropdown.current(0)
        
        # Group By column selection
        ttk.Label(config_frame, text="Group By:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        group_column_var = tk.StringVar()
        group_column_dropdown = ttk.Combobox(config_frame, textvariable=group_column_var, width=20)
        group_column_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Aggregate function
        ttk.Label(config_frame, text="Aggregate:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        agg_frame = ttk.Frame(config_frame)
        agg_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Aggregate function
        agg_functions = ["COUNT", "MAX", "MIN", "SUM", "AVG"]
        agg_func_var = tk.StringVar()
        agg_func_dropdown = ttk.Combobox(agg_frame, textvariable=agg_func_var, values=agg_functions, state="readonly", width=10)
        agg_func_dropdown.pack(side='left', padx=5)
        agg_func_dropdown.current(0)
        
        # Aggregate column
        agg_column_var = tk.StringVar()
        agg_column_dropdown = ttk.Combobox(agg_frame, textvariable=agg_column_var, width=15)
        agg_column_dropdown.pack(side='left', padx=5)
        
        # Having condition
        ttk.Label(config_frame, text="Having:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        having_frame = ttk.Frame(config_frame)
        having_frame.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        having_conditions = ["greater than", "less than", "equals"]
        having_condition_var = tk.StringVar()
        having_condition_dropdown = ttk.Combobox(having_frame, textvariable=having_condition_var, 
                                               values=having_conditions, state="readonly", width=10)
        having_condition_dropdown.pack(side='left', padx=5)
        having_condition_dropdown.current(0)
        
        # Having value
        having_value = ttk.Entry(having_frame, width=10)
        having_value.pack(side='left', padx=5)
        
        # Use having condition checkbox
        use_having_var = tk.BooleanVar()
        ttk.Checkbutton(having_frame, text="Apply Having", variable=use_having_var).pack(side='left', padx=5)
        
        # Update columns when table changes
        def update_columns(*args):
            try:
                cursor.execute(f"SELECT * FROM {table_var.get()} WHERE 1=0")
                columns = [col[0] for col in cursor.description]
                group_column_dropdown['values'] = columns
                agg_column_dropdown['values'] = columns
                if columns:
                    group_column_dropdown.current(0)
                    agg_column_dropdown.current(0)
            except Exception as e:
                group_column_dropdown['values'] = []
                agg_column_dropdown['values'] = []
                
        table_var.trace('w', update_columns)
        # Initialize columns
        update_columns()
        
        # Execute button
        ttk.Button(config_frame, text="View Grouped Data", 
                 command=lambda: execute_group_aggregate(
                     table_var.get(), 
                     group_column_var.get(), 
                     agg_func_var.get(), 
                     agg_column_var.get(), 
                     use_having_var.get(),
                     having_condition_var.get(), 
                     having_value.get(), 
                     results_frame)).grid(row=4, column=0, columnspan=2, pady=15)
        
        # Results area
        ttk.Label(frame, text="Results:").pack(anchor='w', pady=5)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill='both', expand=True, pady=5)
    
    def execute_group_aggregate(table, group_column, agg_func, agg_column, use_having, having_condition, having_value, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Build SQL query
            agg_expr = f"{agg_func}({agg_column})" if agg_func != "COUNT" else f"COUNT(*)"
            query = f"SELECT {group_column}, {agg_expr} AS aggregation_result FROM {table} GROUP BY {group_column}"
            params = []
            
            # Add having clause if needed
            if use_having and having_condition and having_value:
                if having_condition == "greater than":
                    query += f" HAVING {agg_expr} > ?"
                    params.append(having_value)
                elif having_condition == "less than":
                    query += f" HAVING {agg_expr} < ?"
                    params.append(having_value)
                elif having_condition == "equals":
                    query += f" HAVING {agg_expr} = ?"
                    params.append(having_value)
            
            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            
            if not rows:
                ttk.Label(results_frame, text=f"No data found", 
                       font=('Arial', 12)).pack(pady=20)
                return
                
            # Create a table-like display with headers
            headers_frame = ttk.Frame(results_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=10, pady=5)
            
            # Create headers
            for col, header in enumerate(column_names):
                ttk.Label(headers_frame, text=header, width=20, style='TableHeader.TLabel').grid(row=0, column=col, sticky="nsew")
                headers_frame.grid_columnconfigure(col, weight=1)
            
            # Create scrollable frame for results
            list_frame = ttk.Frame(results_frame)
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            for col in range(len(column_names)):
                scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Display results
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    cell_frame.grid(row=i, column=j, sticky="nsew")
                    
                    # Alternate row colors
                    if i % 2 == 0:
                        bg_color = 'white'
                    else:
                        bg_color = '#F2F2F2'
                    
                    ttk.Label(cell_frame, text=str(value), background=bg_color, 
                           style='TableCell.TLabel').pack(fill='both', expand=True)
                
                # Set row height
                scrollable_frame.grid_rowconfigure(i, minsize=40)
                
        except Exception as e:
            ttk.Label(results_frame, text=f"Error: {str(e)}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)

    # Call the setup function
    setup_data_explorer()

def launch_main_app(user_id):
    root = tk.Tk()
    root.title("\U0001F3B5 Music Management System")
    root.geometry("1000x600")

    # Add back button frame at the top
    back_frame = ttk.Frame(root)
    back_frame.pack(fill='x', padx=5, pady=5)
    
    def back_to_login():
        root.destroy()
        # Recreate the login window
        login_window = tk.Tk()
        login_window.title("Music Management System - Login")
        login_window.geometry("400x400")
        
        # Create main frame
        main_frame = tk.Frame(login_window)
        main_frame.pack(pady=40)
        
        # Title Label
        title_label = tk.Label(main_frame, text="Music Management System", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Login Type Selection
        login_type = tk.StringVar(value="user")
        tk.Radiobutton(main_frame, text="User Login", variable=login_type, value="user").pack()
        tk.Radiobutton(main_frame, text="Admin Login", variable=login_type, value="admin").pack()
        
        # Login Frame
        login_frame = tk.Frame(main_frame)
        login_frame.pack(pady=20)
        
        # Username and Password fields
        username_label = tk.Label(login_frame, text="Username:", width=10)
        username_label.grid(row=0, column=0, pady=5)
        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=0, column=1, pady=5)
        
        password_label = tk.Label(login_frame, text="Password:", width=10)
        password_label.grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        def login():
            uname = username_entry.get()
            pwd = password_entry.get()
            login_type_val = login_type.get()
            
            if login_type_val == "admin":
                if uname == "admin" and pwd == "123":
                    messagebox.showinfo("Login", "Welcome Admin!")
                    login_window.destroy()
                    open_admin_panel()
                else:
                    messagebox.showerror("Login Failed", "Invalid admin credentials!")
            else:  # user login
                cursor.execute("SELECT user_id, username FROM Users WHERE username = ? AND password = ? AND user_type = 'user'", uname, pwd)
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("Login", f"Welcome {uname}! You are logged in as a User.")
                    login_window.destroy()
                    launch_main_app(user[0])  # user[0] = user_id
                else:
                    messagebox.showerror("Login Failed", "Invalid user credentials!")
        
        # Login Button
        login_btn = tk.Button(main_frame, text="Login", command=login, width=20)
        login_btn.pack(pady=20)
        
        # Register Button (for new users)
        def open_register():
            register_window = tk.Toplevel(login_window)
            register_window.title("Register New User")
            register_window.geometry("300x250")
            
            # Register fields
            tk.Label(register_window, text="Username:").pack(pady=5)
            reg_username = tk.Entry(register_window)
            reg_username.pack(pady=5)
            
            tk.Label(register_window, text="Password:").pack(pady=5)
            reg_password = tk.Entry(register_window, show="*")
            reg_password.pack(pady=5)
            
            tk.Label(register_window, text="Email:").pack(pady=5)
            reg_email = tk.Entry(register_window)
            reg_email.pack(pady=5)
            
            def register_user():
                try:
                    cursor.execute("INSERT INTO Users (username, password, email, user_type) VALUES (?, ?, ?, 'user')",
                                 reg_username.get(), reg_password.get(), reg_email.get())
                    conn.commit()
                    messagebox.showinfo("Success", "User registered successfully!")
                    register_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Registration failed: {str(e)}")
            
            tk.Button(register_window, text="Register", command=register_user).pack(pady=20)
        
        register_btn = tk.Button(main_frame, text="Register New User", command=open_register)
        register_btn.pack(pady=10)
        
        login_window.mainloop()
    
    back_btn = ttk.Button(back_frame, text="⬅️ Back to Login", command=back_to_login)
    back_btn.pack(side='right', padx=5)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    home_tab = ttk.Frame(notebook)
    search_tab = ttk.Frame(notebook)
    playlist_tab = ttk.Frame(notebook)
    favorites_tab = ttk.Frame(notebook)
    sort_tab = ttk.Frame(notebook)  # New tab for sort and filter
    pattern_tab = ttk.Frame(notebook)  # New tab for pattern matching

    notebook.add(home_tab, text='\U0001F3E0 Home')
    notebook.add(search_tab, text='\U0001F50D Search')
    notebook.add(playlist_tab, text='\U0001F4C2 Playlists')
    notebook.add(favorites_tab, text='\U0001F496 Favorites')
    notebook.add(sort_tab, text='\U0001F4CA Sort & Filter')  # New tab for sort and filter
    notebook.add(pattern_tab, text='\U0001F50E Pattern Search')  # New tab for pattern matching

    def play_song(song_id):
        try:
            cursor.execute("SELECT file_path FROM Songs WHERE song_id = ?", song_id)
            row = cursor.fetchone()
            if row and row[0]:
                os.startfile(row[0])
            else:
                messagebox.showinfo("Info", "No file path available for this song")
        except Exception as e:
            messagebox.showerror("Play Error", str(e))

    def add_to_favorites(song_id):
        try:
            cursor.execute("INSERT INTO Favorites (user_id, song_id) VALUES (?, ?)", user_id, song_id)
            conn.commit()
            messagebox.showinfo("Success", "Added to Favorites")
            refresh_favorites()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def play_mood(mood_name):
        for widget in home_tab.winfo_children():
            widget.destroy()

        mood_label = ttk.Label(home_tab, text=f"\U0001F3A7 Songs for Mood: {mood_name}", font=('Arial', 14, 'bold'))
        mood_label.pack(pady=10)

        back_btn = ttk.Button(home_tab, text="\U0001F519 Back to All Songs", command=load_songs)
        back_btn.pack(pady=5)

        try:
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                JOIN Song_Moods sm ON s.song_id = sm.song_id
                JOIN Moods m ON sm.mood_id = m.mood_id
                WHERE m.mood_name = ?
            """, mood_name)
            songs = cursor.fetchall()

            if not songs:
                ttk.Label(home_tab, text="No songs found for this mood.").pack()
                return

            for song_id, song_name, artist_name, album_name in songs:
                frame = ttk.Frame(home_tab)
                frame.pack(fill='x', padx=5, pady=2)

                label = ttk.Label(frame, text=f"{song_name} - {artist_name} ({album_name})")
                label.pack(side='left', padx=10)

                play_btn = ttk.Button(frame, text='▶ Play Now', command=lambda sid=song_id: play_song(sid))
                play_btn.pack(side='right', padx=5)

                fav_btn = ttk.Button(frame, text='❤ Favorite', command=lambda sid=song_id: add_to_favorites(sid))
                fav_btn.pack(side='right', padx=5)

        except Exception as e:
            messagebox.showerror("Mood Error", str(e))

    def load_songs():
        for widget in home_tab.winfo_children():
            widget.destroy()

        moods_frame = ttk.Frame(home_tab)
        moods_frame.pack(pady=10)
        
        try:
            cursor.execute("SELECT mood_name FROM Moods")
            mood_names = [row[0] for row in cursor.fetchall()]
            for mood in mood_names:
                ttk.Button(moods_frame, text=f"\U0001F3A7 {mood}", 
                          command=lambda m=mood: play_mood(m)).pack(side='left', padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load moods: {str(e)}")

        try:
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
            """)
            songs = cursor.fetchall()
            for song_id, song_name, artist_name, album_name in songs:
                frame = ttk.Frame(home_tab)
                frame.pack(fill='x', padx=5, pady=2)

                label = ttk.Label(frame, text=f"{song_name} - {artist_name} ({album_name})")
                label.pack(side='left', padx=10)

                play_btn = ttk.Button(frame, text='▶ Play Now', command=lambda sid=song_id: play_song(sid))
                play_btn.pack(side='right', padx=5)

                fav_btn = ttk.Button(frame, text='❤ Favorite', command=lambda sid=song_id: add_to_favorites(sid))
                fav_btn.pack(side='right', padx=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_music():
        term = search_entry.get()
        for widget in search_results.winfo_children():
            widget.destroy()
        try:
            cursor.execute("""
                SELECT 'Song' AS Type, s.song_name, a.artist_name, al.album_name, s.song_id
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                WHERE s.song_name LIKE ? OR a.artist_name LIKE ? OR al.album_name LIKE ?
            """, f'%{term}%', f'%{term}%', f'%{term}%')
            results = cursor.fetchall()
            for type_, song_name, artist_name, album_name, song_id in results:
                frame = ttk.Frame(search_results)
                frame.pack(fill='x', padx=5, pady=2)
                
                label = ttk.Label(frame, text=f"{type_}: {song_name} - {artist_name} ({album_name})")
                label.pack(side='left', padx=10)
                
                play_btn = ttk.Button(frame, text='▶ Play Now', command=lambda sid=song_id: play_song(sid))
                play_btn.pack(side='right', padx=5)
                
                fav_btn = ttk.Button(frame, text='❤ Favorite', command=lambda sid=song_id: add_to_favorites(sid))
                fav_btn.pack(side='right', padx=5)
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    # Search Tab
    search_entry = ttk.Entry(search_tab, width=60)
    search_entry.pack(pady=10)
    search_button = ttk.Button(search_tab, text="Search", command=search_music)
    search_button.pack()
    search_results = ttk.Frame(search_tab)
    search_results.pack(fill='both', expand=True)

    # Favorites Tab
    def refresh_favorites():
        for widget in favorites_tab.winfo_children():
            widget.destroy()
            
        try:
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                JOIN Favorites f ON s.song_id = f.song_id
                WHERE f.user_id = ?
            """, user_id)
            songs = cursor.fetchall()
            
            for song_id, song_name, artist_name, album_name in songs:
                frame = ttk.Frame(favorites_tab)
                frame.pack(fill='x', padx=5, pady=2)
                
                label = ttk.Label(frame, text=f"{song_name} - {artist_name} ({album_name})")
                label.pack(side='left', padx=10)
                
                play_btn = ttk.Button(frame, text='▶ Play Now', command=lambda sid=song_id: play_song(sid))
                play_btn.pack(side='right', padx=5)
                
                remove_btn = ttk.Button(frame, text='Remove', 
                                      command=lambda sid=song_id: remove_from_favorites(sid))
                remove_btn.pack(side='right', padx=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_from_favorites(song_id):
        try:
            cursor.execute("DELETE FROM Favorites WHERE user_id = ? AND song_id = ?", 
                         user_id, song_id)
            conn.commit()
            refresh_favorites()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    refresh_favorites()

    # Playlist Tab - User Interface
    def refresh_user_playlists():
        for widget in playlist_tab.winfo_children():
            widget.destroy()
        
        # Title and create button frame
        title_frame = ttk.Frame(playlist_tab)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(title_frame, text="My Playlists", font=('Arial', 14, 'bold')).pack(side='left')
        ttk.Button(title_frame, text="➕ Create New Playlist", command=create_user_playlist).pack(side='right')
        
        # Create notebook for playlist types
        playlist_notebook = ttk.Notebook(playlist_tab)
        playlist_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs for personal and default playlists
        personal_tab = ttk.Frame(playlist_notebook)
        default_tab = ttk.Frame(playlist_notebook)
        
        playlist_notebook.add(personal_tab, text='My Playlists')
        playlist_notebook.add(default_tab, text='Default Playlists')
        
        # Load personal playlists
        try:
            cursor.execute("""
                SELECT playlist_id, playlist_name
                FROM Playlists
                WHERE user_id = ? AND is_default = 0
                ORDER BY playlist_name
            """, user_id)
            
            personal_playlists = cursor.fetchall()
            
            if not personal_playlists:
                ttk.Label(personal_tab, text="You haven't created any playlists yet.", font=('Arial', 12)).pack(pady=20)
            else:
                # Create a table-like display with headers
                headers_frame = ttk.Frame(personal_tab, style='Table.TFrame')
                headers_frame.pack(fill='x', padx=10, pady=5)
                
                ttk.Label(headers_frame, text="Playlist Name", width=30, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
                ttk.Label(headers_frame, text="Actions", width=30, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
                
                # Configure grid weights
                headers_frame.grid_columnconfigure(0, weight=3)
                headers_frame.grid_columnconfigure(1, weight=2)
                
                # Create scrollable frame for playlist list
                list_frame = ttk.Frame(personal_tab)
                list_frame.pack(fill='both', expand=True, padx=10, pady=5)
                
                canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
                scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )
                
                canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                
                def on_canvas_configure(event):
                    canvas.itemconfig(canvas_window, width=event.width)
                
                canvas.bind("<Configure>", on_canvas_configure)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Configure grid weights
                scrollable_frame.grid_columnconfigure(0, weight=3)
                scrollable_frame.grid_columnconfigure(1, weight=2)
                
                # Display each personal playlist
                for i, (playlist_id, playlist_name) in enumerate(personal_playlists):
                    ttk.Label(scrollable_frame, text=playlist_name, width=30, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    
                    # Actions frame
                    actions_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    actions_frame.grid(row=i, column=1, sticky="nsew")
                    
                    ttk.Button(actions_frame, text='View Songs', 
                             command=lambda pid=playlist_id: view_user_playlist(pid)).pack(side='left', padx=3, pady=3)
                    ttk.Button(actions_frame, text='Delete', 
                             command=lambda pid=playlist_id, pname=playlist_name: delete_user_playlist(pid, pname)).pack(side='left', padx=3, pady=3)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load personal playlists: {str(e)}")
        
        # Load default playlists
        try:
            cursor.execute("""
                SELECT playlist_id, playlist_name
                FROM Playlists
                WHERE is_default = 1
                ORDER BY playlist_name
            """)
            default_playlists = cursor.fetchall()
            
            if not default_playlists:
                ttk.Label(default_tab, text="No default playlists available.", font=('Arial', 12)).pack(pady=20)
            else:
                # Create a table-like display with headers
                headers_frame = ttk.Frame(default_tab, style='Table.TFrame')
                headers_frame.pack(fill='x', padx=10, pady=5)
                
                ttk.Label(headers_frame, text="Playlist Name", width=40, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
                ttk.Label(headers_frame, text="Actions", width=20, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
                
                # Configure grid weights
                headers_frame.grid_columnconfigure(0, weight=4)
                headers_frame.grid_columnconfigure(1, weight=1)
                
                # Create scrollable frame for playlist list
                list_frame = ttk.Frame(default_tab)
                list_frame.pack(fill='both', expand=True, padx=10, pady=5)
                
                canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
                scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )
                
                canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                
                def on_canvas_configure(event):
                    canvas.itemconfig(canvas_window, width=event.width)
                
                canvas.bind("<Configure>", on_canvas_configure)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Configure grid weights
                scrollable_frame.grid_columnconfigure(0, weight=4)
                scrollable_frame.grid_columnconfigure(1, weight=1)
                
                # Display each default playlist
                for i, (playlist_id, playlist_name) in enumerate(default_playlists):
                    ttk.Label(scrollable_frame, text=playlist_name, width=40, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    
                    # Actions frame
                    actions_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    actions_frame.grid(row=i, column=1, sticky="nsew")
                    
                    ttk.Button(actions_frame, text='View Songs', 
                             command=lambda pid=playlist_id: view_user_playlist(pid, is_default=True)).pack(side='left', padx=5, pady=3)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load default playlists: {str(e)}")

    def create_user_playlist():
        playlist_name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if playlist_name:
            try:
                cursor.execute("INSERT INTO Playlists (user_id, playlist_name, is_default) VALUES (?, ?, 0)", 
                             user_id, playlist_name)
                conn.commit()
                refresh_user_playlists()
                messagebox.showinfo("Success", "Playlist created successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_user_playlist(playlist_id, playlist_name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete playlist '{playlist_name}'?"):
            try:
                # First delete related entries in Playlist_Songs
                cursor.execute("DELETE FROM Playlist_Songs WHERE playlist_id = ?", playlist_id)
                # Then delete the playlist
                cursor.execute("DELETE FROM Playlists WHERE playlist_id = ? AND user_id = ?", playlist_id, user_id)
                conn.commit()
                refresh_user_playlists()
                messagebox.showinfo("Success", "Playlist deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def view_user_playlist(playlist_id, is_default=False):
        playlist_window = tk.Toplevel(root)
        playlist_window.title("Playlist Songs")
        playlist_window.geometry("900x600")
        playlist_window.configure(bg='#f0f0f0')
        
        try:
            # Get playlist name
            cursor.execute("SELECT playlist_name FROM Playlists WHERE playlist_id = ?", playlist_id)
            playlist_name = cursor.fetchone()[0]
            
            # Create title frame
            title_frame = ttk.Frame(playlist_window)
            title_frame.pack(fill='x', padx=20, pady=10)
            
            playlist_type = "Default Playlist" if is_default else "My Playlist"
            ttk.Label(title_frame, text=f"{playlist_type}: {playlist_name}", 
                    font=('Arial', 14, 'bold')).pack(side='left')
            
            # Add button frame
            button_frame = ttk.Frame(playlist_window)
            button_frame.pack(fill='x', padx=20, pady=5)
            
            # Only allow add/remove for personal playlists
            if not is_default:
                ttk.Button(button_frame, text='➕ Add Songs', 
                         command=lambda: add_song_to_user_playlist(playlist_id, playlist_window)).pack(side='right')
            
            # Create a frame for the song list
            song_list_frame = ttk.Frame(playlist_window)
            song_list_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Create headers
            headers_frame = ttk.Frame(song_list_frame, style='Table.TFrame')
            headers_frame.pack(fill='x', pady=5)
            
            ttk.Label(headers_frame, text="Song", width=30, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
            ttk.Label(headers_frame, text="Artist", width=20, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
            ttk.Label(headers_frame, text="Album", width=20, style='TableHeader.TLabel').grid(row=0, column=2, sticky="nsew")
            ttk.Label(headers_frame, text="Actions", width=20, style='TableHeader.TLabel').grid(row=0, column=3, sticky="nsew")
            
            # Configure grid weights
            headers_frame.grid_columnconfigure(0, weight=3)
            headers_frame.grid_columnconfigure(1, weight=2)
            headers_frame.grid_columnconfigure(2, weight=2)
            headers_frame.grid_columnconfigure(3, weight=2)
            
            # Create scrollable frame for songs
            canvas = tk.Canvas(song_list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(song_list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Configure grid weights
            scrollable_frame.grid_columnconfigure(0, weight=3)
            scrollable_frame.grid_columnconfigure(1, weight=2)
            scrollable_frame.grid_columnconfigure(2, weight=2)
            scrollable_frame.grid_columnconfigure(3, weight=2)
            
            # Get songs in playlist
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                JOIN Playlist_Songs ps ON s.song_id = ps.song_id
                WHERE ps.playlist_id = ?
            """, playlist_id)
            
            songs = cursor.fetchall()
            
            if not songs:
                ttk.Label(scrollable_frame, text="No songs in this playlist", 
                        font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            else:
                for i, (song_id, song_name, artist_name, album_name) in enumerate(songs):
                    ttk.Label(scrollable_frame, text=song_name, width=30, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    ttk.Label(scrollable_frame, text=artist_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                    ttk.Label(scrollable_frame, text=album_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                    
                    # Actions frame
                    actions_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    actions_frame.grid(row=i, column=3, sticky="nsew")
                    
                    ttk.Button(actions_frame, text='▶ Play', 
                             command=lambda sid=song_id: play_song(sid)).pack(side='left', padx=2, pady=2)
                    
                    # Only allow remove for personal playlists
                    if not is_default:
                        ttk.Button(actions_frame, text='❌ Remove', 
                                 command=lambda pid=playlist_id, sid=song_id: remove_song_from_user_playlist(pid, sid, playlist_window)).pack(side='left', padx=2, pady=2)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
                    
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_song_to_user_playlist(playlist_id, parent_window):
        add_window = tk.Toplevel(root)
        add_window.title("Add Songs to Playlist")
        add_window.geometry("800x600")
        add_window.configure(bg='#f0f0f0')
        
        try:
            # Get songs not in the playlist
            cursor.execute("""
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                WHERE s.song_id NOT IN (
                    SELECT song_id FROM Playlist_Songs WHERE playlist_id = ?
                )
            """, playlist_id)
            
            available_songs = cursor.fetchall()
            
            # Create title
            ttk.Label(add_window, text="Add Songs to Playlist", 
                    font=('Arial', 14, 'bold')).pack(pady=10)
            
            # Create search box
            search_frame = ttk.Frame(add_window)
            search_frame.pack(fill='x', padx=20, pady=10)
            
            ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
            search_entry = ttk.Entry(search_frame, width=40)
            search_entry.pack(side='left', padx=5)
            
            # Create headers
            headers_frame = ttk.Frame(add_window, style='Table.TFrame')
            headers_frame.pack(fill='x', padx=20, pady=5)
            
            ttk.Label(headers_frame, text="Song", width=30, style='TableHeader.TLabel').grid(row=0, column=0, sticky="nsew")
            ttk.Label(headers_frame, text="Artist", width=20, style='TableHeader.TLabel').grid(row=0, column=1, sticky="nsew")
            ttk.Label(headers_frame, text="Album", width=20, style='TableHeader.TLabel').grid(row=0, column=2, sticky="nsew")
            ttk.Label(headers_frame, text="Add", width=10, style='TableHeader.TLabel').grid(row=0, column=3, sticky="nsew")
            
            # Configure grid weights
            headers_frame.grid_columnconfigure(0, weight=3)
            headers_frame.grid_columnconfigure(1, weight=2)
            headers_frame.grid_columnconfigure(2, weight=2)
            headers_frame.grid_columnconfigure(3, weight=1)
            
            # Create scrollable frame
            canvas = tk.Canvas(add_window, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            # Make sure the frame takes the full width of the canvas
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=20, pady=5)
            scrollbar.pack(side="right", fill="y", pady=5)
            
            # Configure grid weights in scrollable frame to prevent hover effect
            scrollable_frame.grid_columnconfigure(0, weight=3)
            scrollable_frame.grid_columnconfigure(1, weight=2)
            scrollable_frame.grid_columnconfigure(2, weight=2)
            scrollable_frame.grid_columnconfigure(3, weight=1)
            
            if not available_songs:
                ttk.Label(scrollable_frame, text="All songs are already in this playlist", 
                        font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            else:
                # Function to add song to playlist
                def add_song_to_db(playlist_id, song_id):
                    try:
                        cursor.execute("INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES (?, ?)", 
                                    playlist_id, song_id)
                        conn.commit()
                        messagebox.showinfo("Success", "Song added to playlist")
                        add_window.destroy()
                        if parent_window:
                            parent_window.destroy()
                            view_user_playlist(playlist_id)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                
                # Function to filter songs based on search
                def filter_songs(*args):
                    search_term = search_entry.get().lower()
                    
                    # Clear existing rows
                    for widget in scrollable_frame.winfo_children():
                        widget.destroy()
                    
                    # Filter and display songs
                    filtered_songs = [song for song in available_songs if 
                                    search_term in song[1].lower() or 
                                    search_term in song[2].lower() or 
                                    search_term in song[3].lower()]
                    
                    if not filtered_songs:
                        ttk.Label(scrollable_frame, text="No matching songs found", 
                                font=('Arial', 12), style='TableCell.TLabel').grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
                    else:
                        for i, (song_id, song_name, artist_name, album_name) in enumerate(filtered_songs):
                            ttk.Label(scrollable_frame, text=song_name, width=30, 
                                   style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                            ttk.Label(scrollable_frame, text=artist_name, width=20, 
                                   style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                            ttk.Label(scrollable_frame, text=album_name, width=20, 
                                   style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                            
                            add_btn_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                            add_btn_frame.grid(row=i, column=3, sticky="nsew")
                            
                            ttk.Button(add_btn_frame, text='➕ Add', 
                                    command=lambda sid=song_id: add_song_to_db(playlist_id, sid)).pack(padx=2, pady=2)
                            
                            # Set row height
                            scrollable_frame.grid_rowconfigure(i, minsize=40)
                
                # Bind search entry to filter function
                search_entry.bind("<KeyRelease>", filter_songs)
                
                # Initial display of all songs
                for i, (song_id, song_name, artist_name, album_name) in enumerate(available_songs):
                    ttk.Label(scrollable_frame, text=song_name, width=30, 
                           style='TableCell.TLabel').grid(row=i, column=0, sticky="nsew")
                    ttk.Label(scrollable_frame, text=artist_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=1, sticky="nsew")
                    ttk.Label(scrollable_frame, text=album_name, width=20, 
                           style='TableCell.TLabel').grid(row=i, column=2, sticky="nsew")
                    
                    add_btn_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                    add_btn_frame.grid(row=i, column=3, sticky="nsew")
                    
                    ttk.Button(add_btn_frame, text='➕ Add', 
                            command=lambda sid=song_id: add_song_to_db(playlist_id, sid)).pack(padx=2, pady=2)
                    
                    # Set row height
                    scrollable_frame.grid_rowconfigure(i, minsize=40)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def remove_song_from_user_playlist(playlist_id, song_id, window):
        try:
            cursor.execute("DELETE FROM Playlist_Songs WHERE playlist_id = ? AND song_id = ?", 
                        playlist_id, song_id)
            conn.commit()
            messagebox.showinfo("Success", "Song removed from playlist")
            
            if window:
                window.destroy()
                view_user_playlist(playlist_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Initialize playlist tab
    refresh_user_playlists()

    # Load home tab
    load_songs()

    # Sort & Filter Tab for User
    def setup_user_sort_tab():
        # Title
        ttk.Label(sort_tab, text="Sort & Filter Music", font=('Arial', 14, 'bold')).pack(pady=10, anchor='w')
        
        # Configuration
        config_frame = ttk.Frame(sort_tab)
        config_frame.pack(fill='x', pady=10, padx=20)
        
        # Table selection - for user, only show Songs table
        ttk.Label(config_frame, text="View:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        table_var = tk.StringVar(value="Songs")
        tables = ["Songs"]  # Only show songs for users
        table_dropdown = ttk.Combobox(config_frame, textvariable=table_var, values=tables, state="readonly", width=20)
        table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        table_dropdown.current(0)
        
        # Column selection for sorting
        ttk.Label(config_frame, text="Sort By:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        sort_column_var = tk.StringVar()
        sort_columns = ["song_name", "artist_id", "album_id", "release_year"]
        sort_column_dropdown = ttk.Combobox(config_frame, textvariable=sort_column_var, values=sort_columns, state="readonly", width=20)
        sort_column_dropdown.grid(row=1, column=1, padx=5, pady=5)
        sort_column_dropdown.current(0)
        
        # Sort order
        ttk.Label(config_frame, text="Order:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        sort_orders = ["Ascending (A-Z, 1-9)", "Descending (Z-A, 9-1)"]
        sort_order_var = tk.StringVar()
        sort_order_dropdown = ttk.Combobox(config_frame, textvariable=sort_order_var, values=sort_orders, state="readonly", width=20)
        sort_order_dropdown.grid(row=2, column=1, padx=5, pady=5)
        sort_order_dropdown.current(0)
        
        # Filter option
        ttk.Label(config_frame, text="Filter By:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        filter_columns = ["song_name", "release_year"]
        filter_column_var = tk.StringVar()
        filter_column_dropdown = ttk.Combobox(config_frame, textvariable=filter_column_var, values=filter_columns, state="readonly", width=20)
        filter_column_dropdown.grid(row=3, column=1, padx=5, pady=5)
        filter_column_dropdown.current(0)
        
        # Filter condition
        filter_conditions = ["equals", "greater than", "less than", "contains"]
        filter_condition_var = tk.StringVar()
        filter_condition_dropdown = ttk.Combobox(config_frame, textvariable=filter_condition_var, 
                                              values=filter_conditions, state="readonly", width=15)
        filter_condition_dropdown.grid(row=3, column=2, padx=5, pady=5)
        filter_condition_dropdown.current(0)
        
        # Filter value
        filter_value = ttk.Entry(config_frame, width=15)
        filter_value.grid(row=3, column=3, padx=5, pady=5)
        
        # Execute button
        ttk.Button(config_frame, text="View Results", 
                 command=lambda: user_sort_filter(
                     sort_column_var.get(), 
                     sort_order_var.get(), 
                     filter_column_var.get(), 
                     filter_condition_var.get(), 
                     filter_value.get(), 
                     results_frame)).grid(row=4, column=0, columnspan=4, pady=15)
        
        # Results area
        results_frame = ttk.Frame(sort_tab)
        results_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Style configuration for Excel-like appearance
        style = ttk.Style()
        style.configure('Table.TFrame', 
                       background='white',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('TableHeader.TLabel', 
                       background='#4472C4',  # Excel-like blue header
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       relief='solid',
                       borderwidth=1,
                       padding=5,
                       anchor='center')
        
        style.configure('TableCell.TLabel', 
                       background='white', 
                       font=('Arial', 10),
                       relief='solid',
                       borderwidth=1,
                       padding=5,
                       anchor='w')
    
    def user_sort_filter(sort_column, sort_order, filter_column, filter_condition, filter_value, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Input validation
            if filter_column == "release_year" and filter_value and not filter_value.isdigit():
                raise ValueError("Release year must be a number")
                
            # Join with artists and albums to get names instead of IDs for better user experience
            query = """
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name, s.release_year 
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
            """
            params = []
            
            # Add filter if provided
            if filter_column and filter_condition and filter_value:
                if filter_column == "song_name":
                    if filter_condition == "equals":
                        query += " WHERE s.song_name = ?"
                        params.append(filter_value)
                    elif filter_condition == "contains":
                        query += " WHERE s.song_name LIKE ?"
                        params.append(f"%{filter_value}%")
                elif filter_column == "release_year":
                    if filter_condition == "equals":
                        query += " WHERE s.release_year = ?"
                        params.append(int(filter_value))
                    elif filter_condition == "greater than":
                        query += " WHERE s.release_year > ?"
                        params.append(int(filter_value))
                    elif filter_condition == "less than":
                        query += " WHERE s.release_year < ?"
                        params.append(int(filter_value))
            
            # Add sort
            if sort_column:
                sort_col_prefix = "s." if sort_column in ["song_name", "release_year"] else "a." if sort_column == "artist_id" else "al."
                sort_col_name = sort_column
                if sort_column == "artist_id":
                    sort_col_name = "artist_name"
                elif sort_column == "album_id":
                    sort_col_name = "album_name"
                    
                order_direction = "DESC" if sort_order.startswith("Descending") else "ASC"
                query += f" ORDER BY {sort_col_prefix}{sort_col_name} {order_direction}"
                
            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if not rows:
                ttk.Label(results_frame, text="No songs found", 
                       font=('Arial', 12)).pack(pady=20)
                return
            
            # Define column widths - improved proportions
            col_widths = {
                "Song ID": 8,
                "Song Name": 25,
                "Artist": 20,
                "Album": 20,
                "Release Year": 10,
                "Actions": 15
            }
            
            # Create a container frame with fixed width
            table_container = ttk.Frame(results_frame)
            table_container.pack(fill='both', expand=True, pady=5)
            
            # Create headers frame with fixed width
            headers_frame = ttk.Frame(table_container, style='Table.TFrame')
            headers_frame.pack(fill='x', pady=5)
            
            # Configure columns in the headers frame
            total_width = sum(col_widths.values())
            for i, (header, width) in enumerate(col_widths.items()):
                headers_frame.columnconfigure(i, weight=width, minsize=width*8)  # Use proportional weights
                cell = ttk.Label(headers_frame, text=header, style='TableHeader.TLabel')
                cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            
            # Create a scrollable frame for results
            list_frame = ttk.Frame(table_container)
            list_frame.pack(fill='both', expand=True, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            # Configure the same column weights in the scrollable frame
            for i, width in enumerate(col_widths.values()):
                scrollable_frame.columnconfigure(i, weight=width, minsize=width*8)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Display songs with action buttons
            for i, row in enumerate(rows):
                song_id, song_name, artist_name, album_name, release_year = row
                
                # Alternate row colors
                bg_color = '#F2F2F2' if i % 2 == 0 else 'white'
                
                # Create cells for each column with proper alignment
                # Song ID
                cell = ttk.Label(scrollable_frame, text=str(song_id), background=bg_color, 
                              style='TableCell.TLabel', anchor='center')
                cell.grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
                
                # Song Name
                cell = ttk.Label(scrollable_frame, text=song_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=1, sticky="nsew", padx=1, pady=1)
                
                # Artist
                cell = ttk.Label(scrollable_frame, text=artist_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=2, sticky="nsew", padx=1, pady=1)
                
                # Album
                cell = ttk.Label(scrollable_frame, text=album_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=3, sticky="nsew", padx=1, pady=1)
                
                # Release Year
                cell = ttk.Label(scrollable_frame, text=str(release_year), background=bg_color, 
                              style='TableCell.TLabel', anchor='center')
                cell.grid(row=i, column=4, sticky="nsew", padx=1, pady=1)
                
                # Actions
                action_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                action_frame.grid(row=i, column=5, sticky="nsew", padx=1, pady=1)
                action_frame.configure(padding=2)
                
                ttk.Button(action_frame, text='▶ Play', 
                         command=lambda sid=song_id: play_song(sid), width=5).pack(side='left', padx=1, pady=1)
                ttk.Button(action_frame, text='❤', 
                         command=lambda sid=song_id: add_to_favorites(sid), width=3).pack(side='left', padx=1, pady=1)
                
                # Set row height
                scrollable_frame.rowconfigure(i, minsize=40)
                
        except Exception as e:
            error_message = str(e)
            ttk.Label(results_frame, text=f"Error: {error_message}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)
    
    # Pattern Matching Tab for User
    def setup_user_pattern_tab():
        # Title
        title_frame = ttk.Frame(pattern_tab)
        title_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(title_frame, text="Search Songs by Pattern", font=('Arial', 14, 'bold')).pack(side='left')
        ttk.Button(title_frame, text="Help", command=show_wildcard_help).pack(side='right')
        
        # Search configuration
        search_frame = ttk.Frame(pattern_tab)
        search_frame.pack(fill='x', pady=10, padx=20)
        
        # Column selection
        ttk.Label(search_frame, text="Search In:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        column_var = tk.StringVar(value="Song Name")  # Set default value
        columns = ["Song Name", "Artist Name", "Album Name"]
        column_dropdown = ttk.Combobox(search_frame, textvariable=column_var, values=columns, state="readonly", width=20)
        column_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Pattern matching type
        ttk.Label(search_frame, text="Match Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        pattern_types = [
            "Starts with...", 
            "Contains...", 
            "Ends with...", 
            "Exactly matches...",
            "Custom pattern..." # Added for advanced pattern matching
        ]
        pattern_var = tk.StringVar(value="Contains...")  # Set default value
        pattern_dropdown = ttk.Combobox(search_frame, textvariable=pattern_var, values=pattern_types, state="readonly", width=20)
        pattern_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Search text
        ttk.Label(search_frame, text="Search Text:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        search_text = ttk.Entry(search_frame, width=30)
        search_text.grid(row=2, column=1, padx=5, pady=5)
        
        # Case sensitive option
        case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(search_frame, text="Case Sensitive", variable=case_sensitive_var).grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Results area
        results_frame = ttk.Frame(pattern_tab)
        results_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Search and clear buttons
        ttk.Button(button_frame, text="Search", 
                 command=lambda: user_pattern_search(
                     column_var.get(), 
                     pattern_var.get(), 
                     search_text.get(),
                     case_sensitive_var.get(),
                     results_frame)).pack(side='left', padx=10)
                 
        ttk.Button(button_frame, text="Clear", 
                 command=lambda: clear_pattern_search(
                     column_var,
                     pattern_var,
                     search_text,
                     case_sensitive_var,
                     results_frame)).pack(side='left', padx=10)

    def show_wildcard_help():
        help_text = """
Wildcard Pattern Matching Help:

% - Matches any string of zero or more characters
_ - Matches any single character
[] - Matches any single character within the specified range
[^] - Matches any single character not within the specified range

Examples:
- 'A%' - Matches any string starting with 'A'
- '%ing' - Matches any string ending with 'ing'
- '_at' - Matches any 3-character string ending with 'at'
- '[A-C]%' - Matches any string starting with A, B, or C
- '[^A-C]%' - Matches any string not starting with A, B, or C
    """
        messagebox.showinfo("Wildcard Pattern Matching Help", help_text)

    def clear_pattern_search(column_var, pattern_var, search_text, case_sensitive_var, results_frame):
        column_var.set("Song Name")
        pattern_var.set("Contains...")
        search_text.delete(0, tk.END)
        case_sensitive_var.set(False)
        
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        # Show message
        ttk.Label(results_frame, text="Enter a search pattern and click Search", 
               font=('Arial', 12)).pack(pady=20)

    def user_pattern_search(column, pattern_type, search_text, case_sensitive, results_frame):
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Input validation for empty search
            if not search_text.strip():
                raise ValueError("Please enter a search term")
                
            # Map friendly column name to actual column name
            column_map = {
                "Song Name": "s.song_name",
                "Artist Name": "a.artist_name",
                "Album Name": "al.album_name"
            }
            
            if column not in column_map:
                raise ValueError(f"Invalid column selection: {column}")
            
            search_column = column_map[column]
            
            # Build pattern for LIKE clause
            if pattern_type == "Starts with...":
                pattern = f"{search_text}%"
            elif pattern_type == "Contains...":
                pattern = f"%{search_text}%"
            elif pattern_type == "Ends with...":
                pattern = f"%{search_text}"
            elif pattern_type == "Exactly matches...":
                pattern = search_text
            elif pattern_type == "Custom pattern...":
                pattern = search_text  # Use the exact pattern provided by user
            else:
                raise ValueError(f"Invalid pattern type: {pattern_type}")
            
            # Execute search query with joins to get all relevant information
            query = """
                SELECT s.song_id, s.song_name, a.artist_name, al.album_name, s.release_year 
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                JOIN Albums al ON s.album_id = al.album_id
                WHERE """
            
            # Handle case sensitivity
            if case_sensitive:
                query += search_column + " LIKE ?"
                params = [pattern]
            else:
                query += f"LOWER({search_column}) LIKE LOWER(?)"
                params = [pattern]
            
            print(f"DEBUG: Running query: {query} with pattern: {pattern}, case_sensitive: {case_sensitive}")
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if not rows:
                ttk.Label(results_frame, text=f"No matches found for '{search_text}'", 
                       font=('Arial', 12)).pack(pady=20)
                return
            
            # Show search summary
            summary_text = f"Found {len(rows)} matches for '{search_text}'"
            if pattern_type != "Custom pattern...":
                summary_text += f" ({pattern_type.lower().rstrip('...')})"
            if case_sensitive:
                summary_text += " (case sensitive)"
                
            ttk.Label(results_frame, text=summary_text, 
                   font=('Arial', 11, 'italic')).pack(anchor='w', pady=(0, 10))
            
            # Define column widths - improved proportions
            col_widths = {
                "Song ID": 8,
                "Song Name": 25,
                "Artist": 20,
                "Album": 20,
                "Release Year": 10,
                "Actions": 15
            }
            
            # Create a container frame with fixed width
            table_container = ttk.Frame(results_frame)
            table_container.pack(fill='both', expand=True, pady=5)
            
            # Create headers frame with fixed width
            headers_frame = ttk.Frame(table_container, style='Table.TFrame')
            headers_frame.pack(fill='x', pady=5)
            
            # Configure columns in the headers frame
            total_width = sum(col_widths.values())
            for i, (header, width) in enumerate(col_widths.items()):
                headers_frame.columnconfigure(i, weight=width, minsize=width*8)  # Use proportional weights
                cell = ttk.Label(headers_frame, text=header, style='TableHeader.TLabel')
                cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            
            # Create a scrollable frame for results
            list_frame = ttk.Frame(table_container)
            list_frame.pack(fill='both', expand=True, pady=5)
            
            canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Table.TFrame')
            
            # Configure the same column weights in the scrollable frame
            for i, width in enumerate(col_widths.values()):
                scrollable_frame.columnconfigure(i, weight=width, minsize=width*8)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Display songs with action buttons
            for i, row in enumerate(rows):
                song_id, song_name, artist_name, album_name, release_year = row
                
                # Alternate row colors
                bg_color = '#F2F2F2' if i % 2 == 0 else 'white'
                
                # Create cells for each column with proper alignment
                # Song ID
                cell = ttk.Label(scrollable_frame, text=str(song_id), background=bg_color, 
                              style='TableCell.TLabel', anchor='center')
                cell.grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
                
                # Song Name
                cell = ttk.Label(scrollable_frame, text=song_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=1, sticky="nsew", padx=1, pady=1)
                
                # Artist
                cell = ttk.Label(scrollable_frame, text=artist_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=2, sticky="nsew", padx=1, pady=1)
                
                # Album
                cell = ttk.Label(scrollable_frame, text=album_name, background=bg_color, 
                              style='TableCell.TLabel', anchor='w')
                cell.grid(row=i, column=3, sticky="nsew", padx=1, pady=1)
                
                # Release Year
                cell = ttk.Label(scrollable_frame, text=str(release_year), background=bg_color, 
                              style='TableCell.TLabel', anchor='center')
                cell.grid(row=i, column=4, sticky="nsew", padx=1, pady=1)
                
                # Actions
                action_frame = ttk.Frame(scrollable_frame, style='TableCell.TFrame')
                action_frame.grid(row=i, column=5, sticky="nsew", padx=1, pady=1)
                action_frame.configure(padding=2)
                
                # Use lambda with default args to capture the current song_id value
                play_btn = ttk.Button(action_frame, text='▶ Play', width=5)
                play_btn.configure(command=lambda sid=song_id: play_song(sid))
                play_btn.pack(side='left', padx=1, pady=1)
                
                fav_btn = ttk.Button(action_frame, text='❤', width=3)
                fav_btn.configure(command=lambda sid=song_id: add_to_favorites(sid))
                fav_btn.pack(side='left', padx=1, pady=1)
                
                # Set row height
                scrollable_frame.rowconfigure(i, minsize=40)
                
        except Exception as e:
            error_message = str(e)
            print(f"DEBUG: Pattern search error: {error_message}")  # Debug info
            ttk.Label(results_frame, text=f"Error: {error_message}", 
                   foreground="red", font=('Arial', 12)).pack(pady=20)
    
    # Setup the sort/filter and pattern matching tabs
    setup_user_sort_tab()
    setup_user_pattern_tab()

    root.mainloop()

# ---- Main Login UI ----
root = tk.Tk()
root.title("Music Management System - Login")
root.geometry("400x400")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(pady=40)

# Title Label
title_label = tk.Label(main_frame, text="Music Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Login Type Selection
login_type = tk.StringVar(value="user")
tk.Radiobutton(main_frame, text="User Login", variable=login_type, value="user").pack()
tk.Radiobutton(main_frame, text="Admin Login", variable=login_type, value="admin").pack()

# Login Frame
login_frame = tk.Frame(main_frame)
login_frame.pack(pady=20)

# Username and Password fields
username_label = tk.Label(login_frame, text="Username:", width=10)
username_label.grid(row=0, column=0, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, pady=5)

password_label = tk.Label(login_frame, text="Password:", width=10)
password_label.grid(row=1, column=0, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, pady=5)

def login():
    uname = username_entry.get()
    pwd = password_entry.get()
    login_type_val = login_type.get()

    if login_type_val == "admin":
        if uname == "admin" and pwd == "123":
            messagebox.showinfo("Login", "Welcome Admin!")
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials!")
    else:  # user login
        cursor.execute("SELECT user_id, username FROM Users WHERE username = ? AND password = ? AND user_type = 'user'", uname, pwd)
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Login", f"Welcome {uname}! You are logged in as a User.")
            launch_main_app(user[0])  # user[0] = user_id
        else:
            messagebox.showerror("Login Failed", "Invalid user credentials!")

# Login Button
login_btn = tk.Button(main_frame, text="Login", command=login, width=20)
login_btn.pack(pady=20)

# Register Button (for new users)
def open_register():
    register_window = tk.Toplevel(root)
    register_window.title("Register New User")
    register_window.geometry("300x250")

    # Register fields
    tk.Label(register_window, text="Username:").pack(pady=5)
    reg_username = tk.Entry(register_window)
    reg_username.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    reg_password = tk.Entry(register_window, show="*")
    reg_password.pack(pady=5)

    tk.Label(register_window, text="Email:").pack(pady=5)
    reg_email = tk.Entry(register_window)
    reg_email.pack(pady=5)

    def register_user():
        try:
            cursor.execute("INSERT INTO Users (username, password, email, user_type) VALUES (?, ?, ?, 'user')",
                         reg_username.get(), reg_password.get(), reg_email.get())
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            register_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    tk.Button(register_window, text="Register", command=register_user).pack(pady=20)

register_btn = tk.Button(main_frame, text="Register New User", command=open_register)
register_btn.pack(pady=10)

root.mainloop()
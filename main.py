import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide"
)

# File path for saving/loading library data
FILE_PATH = "library.json"

# Function to load library from file
def load_library():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        except Exception as e:
            st.error(f"Error loading library: {e}")
    return []

# Function to save library to file
def save_library(library):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(library, file)
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

# Initialize session state if not already initialized
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# Initialize success message flags if not already in session state
if 'show_add_success' not in st.session_state:
    st.session_state.show_add_success = False
    st.session_state.add_success_message = ""

if 'show_remove_success' not in st.session_state:
    st.session_state.show_remove_success = False
    st.session_state.remove_success_message = ""

if 'show_save_success' not in st.session_state:
    st.session_state.show_save_success = False

# Function to set add success message
def set_add_success(title, author):
    st.session_state.show_add_success = True
    st.session_state.add_success_message = f"'{title}' by {author} added successfully!"

# Function to set remove success message
def set_remove_success(title):
    st.session_state.show_remove_success = True
    st.session_state.remove_success_message = f"'{title}' has been removed from your library!"

# Function to set save success
def set_save_success():
    st.session_state.show_save_success = True

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 1rem;
    }
    .book-card {
        background-color: #F3F3F3;
        color: #000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    .success-msg {
        color: #059669;
        font-weight: bold;
    }
    .warning-msg {
        color: #D97706;
        font-weight: bold;
    }
    .stAlert {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.markdown('<p class="main-header">📚 Library Manager</p>', unsafe_allow_html=True)
page = st.sidebar.radio("Select Operation", 
                        ["Home", "Add Book", "View Library", "Search Books", 
                         "Remove Book", "Statistics"])

st.sidebar.markdown("---")
# Display current library size
st.sidebar.markdown(f"**Library Size:** {len(st.session_state.library)} books")

# Add auto-save button
if st.sidebar.button("Save Library"):
    if save_library(st.session_state.library):
        set_save_success()
        st.sidebar.success("Library saved successfully!")
    else:
        st.sidebar.error("Failed to save library!")

# Display last saved time if file exists
if os.path.exists(FILE_PATH):
    last_modified = os.path.getmtime(FILE_PATH)
    last_modified_time = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f"**Last saved:** {last_modified_time}")

# Home page
if page == "Home":
    st.markdown('<p class="main-header">Welcome to Your Personal Library Manager!</p>', unsafe_allow_html=True)
    
    # Display success message if a book was just added
    if st.session_state.show_add_success:
        st.success(st.session_state.add_success_message)
        st.session_state.show_add_success = False
    
    # Display success message if a book was just removed
    if st.session_state.show_remove_success:
        st.success(st.session_state.remove_success_message)
        st.session_state.show_remove_success = False
    
    # Display success message if library was just saved
    if st.session_state.show_save_success:
        st.success("Library saved successfully!")
        st.session_state.show_save_success = False
    
    st.markdown("""
    This application helps you manage your personal book collection.
    
    ### Features:
    - **Add Books**: Keep track of your entire collection
    - **View Library**: See all your books in one place
    - **Search Books**: Find books by title or author
    - **Remove Books**: Remove books you no longer own
    - **Statistics**: Get insights about your reading habits
    
    ### Getting Started
    Use the sidebar to navigate through different features.
    """)
    
    # Display a sample of books from the library
    if st.session_state.library:
        st.markdown('<p class="section-header">Recently Added Books</p>', unsafe_allow_html=True)
        recent_books = st.session_state.library[-3:] if len(st.session_state.library) > 3 else st.session_state.library
        recent_books.reverse()  # Show newest first
        
        for book in recent_books:
            read_status = "✅ Read" if book["read"] else "📖 Unread"
            st.markdown(f"""
            <div class="book-card">
                <h3>{book['title']}</h3>
                <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
            </div>
            """, unsafe_allow_html=True)

# Add Book page
elif page == "Add Book":
    st.markdown('<p class="section-header">Add a New Book</p>', unsafe_allow_html=True)
    
    # Reset success flags when navigating to this page
    st.session_state.show_add_success = False
    
    with st.form("add_book_form"):
        title = st.text_input("Book Title", key="title")
        author = st.text_input("Author", key="author")
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                             value=2020, step=1, key="year")
        genre = st.text_input("Genre", key="genre")
        read = st.radio("Have you read this book?", ["Yes", "No"], key="read")
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if not title or not author:
                st.error("Title and author are required fields!")
            else:
                # Create and add book to library
                book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read == "Yes"
                }
                
                st.session_state.library.append(book)
                # Auto-save after adding
                save_library(st.session_state.library)
                
                # Set success message and redirect to home
                set_add_success(title, author)
                # Navigate to home to see the success message
                st.rerun()
    
    # Show recently added books on this page as well
    if st.session_state.library:
        st.markdown('<p class="section-header">Recently Added Books</p>', unsafe_allow_html=True)
        recent_books = st.session_state.library[-3:] if len(st.session_state.library) > 3 else st.session_state.library
        recent_books.reverse()  # Show newest first
        
        for book in recent_books:
            read_status = "✅ Read" if book["read"] else "📖 Unread"
            st.markdown(f"""
            <div class="book-card">
                <h3>{book['title']}</h3>
                <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
            </div>
            """, unsafe_allow_html=True)

# View Library page
elif page == "View Library":
    st.markdown('<p class="section-header">Your Book Collection</p>', unsafe_allow_html=True)
    
    # Reset success flags when navigating to this page
    if st.session_state.show_add_success:
        st.success(st.session_state.add_success_message)
        st.session_state.show_add_success = False
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Add an "Edit Mode" toggle
        edit_mode = st.checkbox("Enable Edit Mode")
        
        # Convert library data to DataFrame for display
        df = pd.DataFrame(st.session_state.library)
        
        # Add sorting options
        sort_by = st.selectbox("Sort by:", ["Title", "Author", "Year", "Genre"])
        sort_order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)
        
        # Convert sort column name to lowercase for DataFrame column access
        sort_col = sort_by.lower()
        ascending = sort_order == "Ascending"
        
        # Filter options
        show_filter = st.checkbox("Show filters")
        if show_filter:
            col1, col2 = st.columns(2)
            
            with col1:
                # Only show filter options for existing genres
                all_genres = sorted(list(set(book["genre"] for book in st.session_state.library if book["genre"])))
                if all_genres:
                    selected_genres = st.multiselect("Filter by genre:", all_genres)
            
            with col2:
                read_filter = st.radio("Filter by read status:", ["All", "Read", "Unread"])
        
            # Apply filters
            filtered_df = df.copy()
            if selected_genres:
                filtered_df = filtered_df[filtered_df["genre"].isin(selected_genres)]
            
            if read_filter != "All":
                filtered_df = filtered_df[filtered_df["read"] == (read_filter == "Read")]
        else:
            filtered_df = df.copy()
        
        # Sort the DataFrame
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=ascending)
        
        # Convert boolean to yes/no for display
        filtered_df["read"] = filtered_df["read"].map({True: "Yes", False: "No"})
        
        # Rename columns for display
        filtered_df.columns = [col.capitalize() for col in filtered_df.columns]
        
        # Display the table
        st.dataframe(filtered_df, use_container_width=True)
        
        # Show count of displayed books
        st.markdown(f"**Displaying {len(filtered_df)} of {len(df)} books**")
        
        # If edit mode is enabled, add quick actions
        if edit_mode:
            st.markdown("### Quick Actions")
            
            # Mark as read/unread function
            st.markdown("#### Mark Book as Read/Unread")
            
            # Get list of books
            book_options = [f"{book['title']} by {book['author']} ({book['year']})" 
                          for book in st.session_state.library]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_book = st.selectbox("Select a book:", book_options, key="read_status_book")
            
            with col2:
                # Get current read status
                if selected_book:
                    index = book_options.index(selected_book)
                    current_status = st.session_state.library[index]["read"]
                    new_status = not current_status
                    button_label = f"Mark as {'Unread' if current_status else 'Read'}"
                    
                    if st.button(button_label):
                        st.session_state.library[index]["read"] = new_status
                        save_library(st.session_state.library)
                        st.success(f"'{st.session_state.library[index]['title']}' marked as {'Read' if new_status else 'Unread'}")
                        st.rerun()

# Search Books page
elif page == "Search Books":
    st.markdown('<p class="section-header">Search Your Library</p>', unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to search!")
    else:
        # Create tabs for different search types
        search_tabs = st.tabs(["Basic Search", "Advanced Search"])
        
        with search_tabs[0]:  # Basic Search
            search_type = st.radio("Search by:", ["Title", "Author"], horizontal=True)
            search_term = st.text_input(f"Enter {search_type.lower()} to search:")
            
            if search_term:
                # Perform search based on search type
                if search_type == "Title":
                    results = [book for book in st.session_state.library 
                              if search_term.lower() in book["title"].lower()]
                else:  # Author
                    results = [book for book in st.session_state.library 
                              if search_term.lower() in book["author"].lower()]
                
                # Display results
                if results:
                    st.success(f"Found {len(results)} matching books!")
                    
                    for i, book in enumerate(results, 1):
                        read_status = "✅ Read" if book["read"] else "📖 Unread"
                        st.markdown(f"""
                        <div class="book-card">
                            <h3>{book['title']}</h3>
                            <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No books found with {search_type.lower()} containing '{search_term}'.")
        
        with search_tabs[1]:  # Advanced Search
            st.markdown("### Advanced Search Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                adv_title = st.text_input("Title contains:")
                adv_author = st.text_input("Author contains:")
            
            with col2:
                # Get unique genres
                all_genres = sorted(list(set(book["genre"] for book in st.session_state.library if book["genre"])))
                adv_genre = st.selectbox("Genre:", ["Any"] + all_genres)
                
                adv_read = st.radio("Read status:", ["Any", "Read", "Unread"])
            
            # Year range slider
            if st.session_state.library:
                min_year = min(book["year"] for book in st.session_state.library)
                max_year = max(book["year"] for book in st.session_state.library)
                year_range = st.slider("Publication year range:", 
                                      min_value=min_year, max_value=max_year, 
                                      value=(min_year, max_year))
            
            # Perform advanced search when button is clicked
            if st.button("Search", key="adv_search_btn"):
                results = st.session_state.library.copy()
                
                # Apply title filter
                if adv_title:
                    results = [book for book in results if adv_title.lower() in book["title"].lower()]
                
                # Apply author filter
                if adv_author:
                    results = [book for book in results if adv_author.lower() in book["author"].lower()]
                
                # Apply genre filter
                if adv_genre != "Any":
                    results = [book for book in results if book["genre"] == adv_genre]
                
                # Apply read status filter
                if adv_read != "Any":
                    results = [book for book in results if book["read"] == (adv_read == "Read")]
                
                # Apply year range filter
                results = [book for book in results if year_range[0] <= book["year"] <= year_range[1]]
                
                # Display results
                if results:
                    st.success(f"Found {len(results)} matching books!")
                    
                    for i, book in enumerate(results, 1):
                        read_status = "✅ Read" if book["read"] else "📖 Unread"
                        st.markdown(f"""
                        <div class="book-card">
                            <h3>{book['title']}</h3>
                            <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No books found matching your search criteria.")

# Remove Book page
elif page == "Remove Book":
    st.markdown('<p class="section-header">Remove Books</p>', unsafe_allow_html=True)
    
    # Reset success message flags
    st.session_state.show_remove_success = False
    
    if not st.session_state.library:
        st.info("Your library is empty. There are no books to remove.")
    else:
        # Create tabs for different removal methods
        remove_tabs = st.tabs(["Remove by Selection", "Bulk Remove"])
        
        with remove_tabs[0]:  # Remove by Selection
            # Create a list of book titles with authors for the selection dropdown
            book_options = [f"{book['title']} by {book['author']} ({book['year']})" 
                          for book in st.session_state.library]
            
            selected_book = st.selectbox("Select a book to remove:", book_options)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Show book details
                if selected_book:
                    index = book_options.index(selected_book)
                    book = st.session_state.library[index]
                    read_status = "Read" if book["read"] else "Unread"
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Remove Book", key="remove_single"):
                    # Find the index of the selected book
                    index = book_options.index(selected_book)
                    
                    # Get book details before removing
                    removed_book = st.session_state.library[index]
                    
                    # Remove the book from the library
                    st.session_state.library.pop(index)
                    
                    # Auto-save after removing
                    save_library(st.session_state.library)
                    
                    # Set success message and redirect to home
                    set_remove_success(removed_book['title'])
                    st.rerun()
        
        with remove_tabs[1]:  # Bulk Remove
            st.markdown("### Bulk Remove Options")
            
            # Options for bulk removal
            bulk_option = st.radio("Remove books by:", 
                                ["Read Status", "Genre", "Publication Year"])
            
            if bulk_option == "Read Status":
                status_to_remove = st.radio("Remove books that are:", ["Read", "Unread"])
                books_to_remove = [book for book in st.session_state.library 
                                  if book["read"] == (status_to_remove == "Read")]
            
            elif bulk_option == "Genre":
                # Get unique genres
                all_genres = sorted(list(set(book["genre"] for book in st.session_state.library if book["genre"])))
                if all_genres:
                    genre_to_remove = st.selectbox("Select genre to remove:", all_genres)
                    books_to_remove = [book for book in st.session_state.library 
                                      if book["genre"] == genre_to_remove]
                else:
                    st.warning("No genres found in your library.")
                    books_to_remove = []
            
            elif bulk_option == "Publication Year":
                # Year range slider
                if st.session_state.library:
                    min_year = min(book["year"] for book in st.session_state.library)
                    max_year = max(book["year"] for book in st.session_state.library)
                    year_range = st.slider("Remove books published between:", 
                                          min_value=min_year, max_value=max_year, 
                                          value=(min_year, min_year + 9))
                    
                    books_to_remove = [book for book in st.session_state.library 
                                      if year_range[0] <= book["year"] <= year_range[1]]
            
            # Display books that will be removed
            if books_to_remove:
                st.markdown(f"### {len(books_to_remove)} Books Selected for Removal:")
                
                for book in books_to_remove:
                    read_status = "Read" if book["read"] else "Unread"
                    st.markdown(f"- {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
                
                # Confirmation
                if st.button("Confirm Bulk Remove", key="bulk_remove"):
                    # Save book count before removal
                    removed_count = len(books_to_remove)
                    
                    # Filter out the books to remove
                    st.session_state.library = [book for book in st.session_state.library 
                                              if book not in books_to_remove]
                    
                    # Auto-save after removing
                    save_library(st.session_state.library)
                    
                    st.success(f"Successfully removed {removed_count} books from your library!")
                    st.rerun()
            else:
                st.info("No books match the selected criteria for removal.")

# Statistics page
elif page == "Statistics":
    st.markdown('<p class="section-header">Library Statistics</p>', unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to see statistics!")
    else:
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book["read"])
        unread_books = total_books - read_books
        
        if total_books > 0:
            percent_read = (read_books / total_books) * 100
        else:
            percent_read = 0
        
        # Create tabs for different statistics views
        stat_tabs = st.tabs(["Overview", "By Genre", "By Year", "Authors"])
        
        with stat_tabs[0]:  # Overview
            # Display basic statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Books", total_books)
            
            with col2:
                st.metric("Books Read", read_books)
            
            with col3:
                st.metric("Books Unread", unread_books)
            
            # Progress bar for read percentage
            st.markdown(f"**Percentage Read: {percent_read:.1f}%**")
            st.progress(percent_read / 100)
            
            # Display recent activity if library has books
            if total_books > 0:
                # Get the most recently added books (assuming they're added at the end)
                recent_books = st.session_state.library[-3:] if len(st.session_state.library) > 3 else st.session_state.library
                recent_books.reverse()  # Show newest first
                
                st.markdown("### Recent Activity")
                for book in recent_books:
                    read_status = "✅ Read" if book["read"] else "📖 Unread"
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p>by <b>{book['author']}</b> ({book['year']}) - {book['genre']} - {read_status}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with stat_tabs[1]:  # By Genre
            # Create genre statistics
            st.markdown("### Breakdown by Genre")
            
            genres = {}
            read_by_genre = {}
            
            for book in st.session_state.library:
                genre = book["genre"] if book["genre"] else "Uncategorized"
                
                # Count by genre
                if genre in genres:
                    genres[genre] += 1
                    if book["read"]:
                        read_by_genre[genre] += 1
                else:
                    genres[genre] = 1
                    read_by_genre[genre] = 1 if book["read"] else 0
            
            # Convert to DataFrame for visualization
            genre_df = pd.DataFrame({
                "Genre": list(genres.keys()),
                "Count": list(genres.values()),
                "Read": list(read_by_genre.values())
            })
            
            # Calculate percentage read for each genre
            genre_df["Unread"] = genre_df["Count"] - genre_df["Read"]
            genre_df["Percent_Read"] = (genre_df["Read"] / genre_df["Count"] * 100).round(1)
            
            # Sort by count
            genre_df = genre_df.sort_values("Count", ascending=False)
            
            # Display genre breakdown chart
            st.bar_chart(genre_df.set_index("Genre")[["Read", "Unread"]])
            
            # Display detailed genre table
            st.markdown("### Genre Details")
            genre_display = genre_df[["Genre", "Count", "Read", "Percent_Read"]]
            genre_display.columns = ["Genre", "Total Books", "Books Read", "% Read"]
            st.table(genre_display)
        
        with stat_tabs[2]:  # By Year
            # Publication year distribution
            st.markdown("### Books by Publication Decade")
            
            # Create decade groups
            decades = {}
            read_by_decade = {}
            
            for book in st.session_state.library:
                decade = (book["year"] // 10) * 10
                decade_label = f"{decade}s"
                
                # Count by decade
                if decade_label in decades:
                    decades[decade_label] += 1
                    if book["read"]:
                        read_by_decade[decade_label] += 1
                else:
                    decades[decade_label] = 1
                    read_by_decade[decade_label] = 1 if book["read"] else 0
            
            # Sort decades chronologically
            sorted_decades = sorted(decades.items(), key=lambda x: int(x[0][:-1]))
            sorted_read_by_decade = {decade: read_by_decade.get(decade, 0) for decade, _ in sorted_decades}
            
            decade_df = pd.DataFrame({
                "Decade": [item[0] for item in sorted_decades],
                "Count": [item[1] for item in sorted_decades],
                "Read": list(sorted_read_by_decade.values())
            })
            
            # Calculate unread and percentage
            decade_df["Unread"] = decade_df["Count"] - decade_df["Read"]
            
            # Display decade breakdown chart
            st.bar_chart(decade_df.set_index("Decade")[["Read", "Unread"]])
            
            # Display oldest and newest books
            if total_books > 0:
                oldest_book = min(st.session_state.library, key=lambda x: x["year"])
                newest_book = max(st.session_state.library, key=lambda x: x["year"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Oldest Book")
                    read_status = "✅ Read" if oldest_book["read"] else "📖 Unread"
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{oldest_book['title']}</h3>
                        <p>by <b>{oldest_book['author']}</b> ({oldest_book['year']}) - {oldest_book['genre']} - {read_status}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### Newest Book")
                    read_status = "✅ Read" if newest_book["read"] else "📖 Unread"
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{newest_book['title']}</h3>
                        <p>by <b>{newest_book['author']}</b> ({newest_book['year']}) - {newest_book['genre']} - {read_status}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with stat_tabs[3]:  # Authors
            # Author statistics
            st.markdown("### Author Statistics")
            
            authors = {}
            books_by_author = {}
            
            for book in st.session_state.library:
                author = book["author"]
                if author in authors:
                    authors[author] += 1
                    books_by_author[author].append(book)
                else:
                    authors[author] = 1
                    books_by_author[author] = [book]
            
            # Get top authors
            top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
            
            # Create a DataFrame for visualization
            if top_authors:
                author_df = pd.DataFrame(top_authors[:10], columns=["Author", "Count"])
                
                # Display author bar chart
                st.bar_chart(author_df.set_index("Author"))
                
                # Display most read authors
                st.markdown("### Top 5 Authors in Your Library")
                for author, count in top_authors[:5]:
                    # Calculate percentage read for this author
                    author_books = books_by_author[author]
                    read_count = sum(1 for book in author_books if book["read"])
                    percent_read = (read_count / count) * 100 if count > 0 else 0
                    
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{author}</h3>
                            <p><b>{count} books</b> ({read_count} read)</p>
                        </div>
                        """, unsafe_allow_html=True)
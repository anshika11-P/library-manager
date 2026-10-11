import json
import os

class Book:
    def __init__(self, book_id, title, author, total_copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.issued_copies = 0

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "issued_copies": self.issued_copies
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["book_id"], data["title"], data["author"], data["total_copies"])
        book.issued_copies = data.get("issued_copies", 0)
        return book


class Library:
    def __init__(self, filename="library_inventory.json"):
        self.filename = filename
        self.books = {}  # HashMap style lookup using book_id as key
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for item in data:
                        book = Book.from_dict(item)
                        self.books[book.book_id] = book
            except Exception as e:
                print(f"Error loading library data: {e}")

    def save_data(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump([book.to_dict() for book in self.books.values()], file, indent=4)
        except Exception as e:
            print(f"Error saving library data: {e}")

    def add_book(self, book_id, title, author, total_copies):
        if book_id in self.books:
            print("\n❌ Book ID already exists! Updating total copies instead.")
            self.books[book_id].total_copies += total_copies
        else:
            new_book = Book(book_id, title, author, total_copies)
            self.books[book_id] = new_book
            print("\n✅ Book added successfully to the library!")
        self.save_data()

    def search_books(self, query):
        query = query.lower()
        results = [
            b for b in self.books.values() 
            if query in b.title.lower() or query in b.author.lower() or query in b.book_id.lower()
        ]
        
        if not results:
            print("\n⚠️ No matching books found.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<10} | {'Title':<22} | {'Author':<18} | {'Total':<6} | {'Issued':<6}")
        print("=" * 70)
        for b in results:
            print(f"{b.book_id:<10} | {b.title:<22} | {b.author:<18} | {b.total_copies:<6} | {b.issued_copies:<6}")
        print("=" * 70)

    def issue_book(self, book_id):
        if book_id not in self.books:
            print("\n❌ Book ID not found in library.")
            return

        book = self.books[book_id]
        if book.issued_copies < book.total_copies:
            book.issued_copies += 1
            self.save_data()
            print(f"\n✅ Book '{book.title}' issued successfully!")
        else:
            print(f"\n❌ Sorry, all copies of '{book.title}' are currently issued out.")

    def return_book(self, book_id):
        if book_id not in self.books:
            print("\n❌ Book ID not found in library.")
            return

        book = self.books[book_id]
        if book.issued_copies > 0:
            book.issued_copies -= 1
            self.save_data()
            print(f"\n✅ Book '{book.title}' returned successfully!")
        else:
            print(f"\n❌ Error: No copies of this book were marked as issued.")

    def generate_report(self):
        total_unique_books = len(self.books)
        total_books_count = sum(b.total_copies for b in self.books.values())
        total_issued_count = sum(b.issued_copies for b in self.books.values())

        print("\n" + "=" * 30)
        print("📊 LIBRARY INVENTORY REPORT")
        print("=" * 30)
        print(f"Total Unique Titles : {total_unique_books}")
        print(f"Total Physical Books: {total_books_count}")
        print(f"Total Issued Books  : {total_issued_count}")
        print(f"Available in Stock  : {total_books_count - total_issued_count}")
        print("=" * 30)


def main():
    library = Library()

    while True:
        print("\n--- LIBRARY BOOK INVENTORY MANAGER ---")
        print("1. Add Book")
        print("2. Search Book (Title / Author / ID)")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Inventory & Reports")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()

        if choice == '1':
            bid = input("Enter Book ID: ").strip()
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()
            try:
                copies = int(input("Enter Total Copies: ").strip())
                if bid and title and author:
                    library.add_book(bid, title, author, copies)
                else:
                    print("❌ Fields cannot be empty.")
            except ValueError:
                print("❌ Please enter a valid number for copies.")

        elif choice == '2':
            query = input("Enter search query (Title, Author, or ID): ").strip()
            library.search_books(query)

        elif choice == '3':
            bid = input("Enter Book ID to issue: ").strip()
            library.issue_book(bid)

        elif choice == '4':
            bid = input("Enter Book ID to return: ").strip()
            library.return_book(bid)

        elif choice == '5':
            library.generate_report()

        elif choice == '6':
            print("Exiting Library Manager. Goodbye!")
            break
        else:
            print("❌ Invalid option! Please try again.")

if __name__ == "__main__":
    main()
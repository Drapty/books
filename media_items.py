from operator import add
import sqlite3
import sys
import time
from turtle import title
from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QTextEdit, QLabel, QComboBox
)

from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem

from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import pyqtSignal

import database






def add_item(title, type, genre, rating, review, date_added):
    database.cursor.execute(
    "INSERT INTO media (title,type,genre,rating,review,date_added) VALUES (?,?,?, ?,?,?)",
                   (title, type, genre, rating, review, date_added)
    )
    

def view_items():
    database.cursor.execute("SELECT * FROM media")
    
    for item in database.cursor:
        print(item)

def delete_item(title):
    database.cursor.execute(
        "DELETE FROM media WHERE title=(?)",
        (title,)
    )



def filter_items_by_type(type):
    database.cursor.execute(
        "SELECT * FROM media WHERE type=(?)",
        (type,)
    )

def filter_items_by_genre(genre):
    database.cursor.execute(
        "SELECT * FROM media WHERE genre=(?)",
        (genre,)
    )

def filter_items_by_rating(rating):
    database.cursor.execute(
        "SELECT * FROM media WHERE rating=(?)",
        (rating,)
    )

def sort_items_ascending():
    database.cursor.execute(
        "SELECT * FROM media ORDER BY title ASC"
    )

class Mainmenu(QWidget):
    pass

class add_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Item")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")

        self.type_input = QComboBox()
        self.type_input.addItems(["Book", "Movie"])

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Genre")

        self.rating_input = QLineEdit()
        self.rating_input.setPlaceholderText("Rating")

        self.review_input = QTextEdit()
        self.review_input.setPlaceholderText("Review")

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item_to_db)

        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.type_input)
        self.layout.addWidget(self.genre_input)
        self.layout.addWidget(self.rating_input)
        self.layout.addWidget(self.review_input)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        



    def add_item_to_db(self):
        title = self.title_input.text()
        type = self.type_input.currentText()
        genre = self.genre_input.text()
        rating = self.rating_input.text()
        review = self.review_input.toPlainText()
        date_added = time.strftime("%Y-%m-%d")

        add_item(title, type, genre, rating, review, date_added)
        print(view_items())

        self.hide()
        ### add item succesfully
        self.main_.show()

class Managebook(QWidget):

    emit_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Books")
        self.resize(800, 500)

        main_layout=QVBoxLayout()

        ##top layout
        top_layout = QHBoxLayout()

        ##top_layout.addWidget(QListWidget())

        self.description=QLabel("Manage your media library: Add, delete, or update items.\n")

        self.description.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.description.setFixedSize(100, 50)

        top_layout.addWidget(self.description)
        self.description.setWordWrap(True)

        self.list_widget = QListWidget()

        

        self.add_button = QPushButton("Add")
        top_layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        switch_tab = pyqtSignal(int)
        self.add_button.clicked.connect(self.emit_signal)

        self.delete_button = QPushButton("Delete")

        top_layout.addWidget(self.delete_button, alignment=Qt.AlignTop)

        self.update_button = QPushButton("Update")
        top_layout.addWidget(self.update_button, alignment=Qt.AlignRight)

        top_layout.addWidget(self.list_widget)

        


        ##bottom layolayout

        bottom_layout = QHBoxLayout()

        self.label = QLineEdit("Book/Movie Title:")
        bottom_layout.addWidget(self.label)

        self.search_button = QPushButton("Search")
        bottom_layout.addWidget(self.search_button)
        ##self.search_button.clicked.connect()

        ## assemble

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        database.cursor.execute("SELECT * FROM media")

        rows=database.cursor.fetchall()
        for row in rows:
            self.list_widget.addItem(str(row[0])+" - "+str(row[1])+" - "+str(row[2])+" - "+str(row[3])+" - "+str(row[4])+" - "+str(row[5]))

    



class LibraryUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Library")
        self.resize(800, 500)

        main_layout=QVBoxLayout()


        ##top layout
        top_layout = QHBoxLayout()

        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books by name...")

        self.category_filter = QComboBox()
        self.category_filter.addItems(["Book", "Movie"])

        self.search_button = QPushButton("Search")

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(self.category_filter)
        top_layout.addWidget(self.search_button)

        ###middle layout
        middle_layout= QHBoxLayout()

        self.results_list=QListWidget()
        self.detaildisplay=QTextEdit()
        self.detaildisplay.setReadOnly(True)
        self.image_label=QLabel()
        self.image_label.setAlignment(Qt.AlignLeft )

        middle_layout.addWidget(self.results_list,2)
        middle_layout.addWidget(self.detaildisplay,3)
        middle_layout.addWidget(self.image_label,5)

        ##Assemble

        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)

        self.setLayout(main_layout)

        ## assemble interaction

        self.search_button.clicked.connect(self.search_books)
        

    
    def search_books(self):
        rows=''
        self.detaildisplay.clear()
        self.results_list.clear()
        self.image_label.clear()

        if not self.search_input.text():
            msg = QMessageBox()
            msg.setWindowTitle("Empty imput")
            msg.setText("Please enter a search term.")
            msg.exec_()
            return
        else:
            query=self.search_input.text()

        
        
        row=database.cursor.fetchone()
        time.sleep(0.4)  # Simulate delay for fetching data
        database.cursor.execute(
            "SELECT title FROM media WHERE title LIKE ? AND type=(?)",(query,self.category_filter.currentText())
        )

        
        rows=database.cursor.fetchall()

        if row is None:
            msg = QMessageBox()
            msg.setWindowTitle("No results")
            msg.setText("No media items found matching your search.")
            msg.exec_()
            return

        for row in rows:
            self.results_list.addItem(row[0])
            self.results_list.clicked.connect(lambda: self.show_details(row[0]))  # connect click event to show details 


        results=database.cursor.fetchall()
        ###database.conn.close()

        
        



    def show_details(self,item):
       ## title = item.data(Qt.UserRole)
        
        titlu=item
        
        database.cursor.execute("SELECT title, type FROM media WHERE title=?", (titlu,),)

        if titlu:
            path=f"images/{titlu}.jpg"
            row=database.cursor.fetchall()
            self.detaildisplay.setText(f"{row[0]}")
            self.detaildisplay.append(f"{row[0]}")
            self.detaildisplay.show()
            print(f"{row}")
            pixmap=QPixmap(path)

            scaled = pixmap.scaled(
            200, 200,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)

            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setMinimumSize(250, 250)
            self.image_label.setStyleSheet("""
            background-color: #1e1e1e;
            border: 1px solid #444;
            """)

            scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
            self.image_label.setScaledContents(True)
        

def main():
    
    add_item("The Great Gatsby", "Book", "Classic", "5 stars", "A timeless masterpiece.", "2024-06-01")
    add_item("Inception", "Movie", "Sci-Fi", "4.5 stars", "A mind-bending thriller.", "2024-06-02")
    add_item("Inception", "Movie", "Classic", "5 stars", "A powerful social commentary.", "2024-06-03")

    print(view_items())

    app=QApplication(sys.argv)

    window=LibraryUi()
    add = add_widget()

    ##star-up
    main_=Managebook()

    emit_signal = pyqtSignal()
    
    def handle_switch():
        main_.hide()
        add.show()

    main_.emit_signal.connect(handle_switch)

    main_.show()
    add.hide()
    ##window.show()

    
        


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
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

from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtCore import pyqtSignal

import database

def add_item(title, type, genre, rating, review, date_added):




    database.cursor.execute(
    "INSERT INTO media (title,type,genre,rating,review,date_added) VALUES (?,?,?, ?,?,?)",
                   (title, type, genre, rating, review, date_added)
    )

    
def update_item_to_database(title, type, genre, rating, review):
    database.cursor.execute(
        "UPDATE media SET type=(?), genre=(?), rating=(?), review=(?) WHERE title=(?)",
        (type, genre, rating, review, title)
    )

    
def view_items():
    database.cursor.execute("SELECT * FROM media")
    rows = database.cursor.fetchall()
    return rows

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

class update_widget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_=main_window
       
        self.setWindowTitle("Update Item")
        self.resize(400, 300)

        
        self.layout=QVBoxLayout()

        self.title_input=QLineEdit()
        
        self.type_input=QComboBox()

        self.type_input.addItems(["Book", "Movie"])

        self.genre_input=QLineEdit()
        
        self.rating_input=QLineEdit()
        
        self.review_input=QTextEdit()

        self.update_button=QPushButton("Update")

        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.type_input)  
        self.layout.addWidget(self.genre_input)
        self.layout.addWidget(self.rating_input)
        self.layout.addWidget(self.review_input)
        self.layout.addWidget(self.update_button)

        

        self.setLayout(self.layout)

        id=0
        titlu_=""
        tip=""
        gen=""
        rata=""
        rev=""



        def update_item_to_database(self,title, type, genre, rating, review):
            print("trololoolo")
            if title is not None:
                title_in = title
                print(title_in)
                database.cursor.execute(
                "UPDATE media SET title=(?),type=(?), genre=(?), rating=(?), review=(?) WHERE title=(?)",
                (title,type, genre, rating, review, title_in)
                )
    
                database.conn.commit()
                print(database.cursor.rowcount)
                ###self.hide()
                ###load_data(self.main_)
    
                ###self.main_.show()
            else:
                print("No item selected")
                return

        def update_true(id):
            if title is not None:
                title_in=titlu_

                self.id=id
                print(title_in)
                
                database.cursor.execute(
                "UPDATE media SET title=(?),type=(?), genre=(?), rating=(?), review=(?) WHERE id=(?)",
                (self.title_input.text(), self.type_input.currentText(), self.genre_input.text(), self.rating_input.text(), self.review_input.toPlainText(), self.id)
                )
                database.conn.commit()
                
                self.hide()
                load_data(self.main_)
                self.main_.show()



        self.update_button.clicked.connect(
                                           lambda: update_true(self.id)
                                                                   
                                            
                                                                )
        
class add_widget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_ = main_window

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
        if self.title_input.text() and self.genre_input.text() and self.type_input.currentText() and self.rating_input.text() and self.review_input.toPlainText():
            title = self.title_input.text()
            type = self.type_input.currentText()
            genre = self.genre_input.text()
            rating = self.rating_input.text()
            review = self.review_input.toPlainText()
            date_added = time.strftime("%Y-%m-%d")
            

            add_item(title, type, genre, rating, review, date_added)

            database.cursor.fetchall()
            self.hide()
    
            load_data(self.main_)
            self.main_.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Incomplete input")
            msg.setText("Please fill in all fields before adding an item.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon("images/blue-circle-icon-info-png-clipart.jpg"))
            msg.exec_()
        
def delete_item_from_db(list_widget):
    items_=list_widget.selectedItems()

    if not items_:  
        msg = QMessageBox()
        msg.setWindowTitle("No selection")
        msg.setText("Please select an item to delete.")
        msg.setIcon(QMessageBox.Warning)
        pixmap = QPixmap("images/warning.png")
        msg.setWindowIcon(QIcon("images/blue-circle-icon-info-png-clipart.jpg"))
        msg.exec_()
        return
    else:
        for item in items_:
            print(item.text())
            database.cursor.execute("DELETE FROM media WHERE title=(?)", (item.text().split(" - ")[1],)) 

        load_data(list_widget.parent())  # refresh the list after deletion

def update_item_from_db(self,update_widget_,item):
    
    if item is None:
        msg = QMessageBox()
        msg.setWindowTitle("No selection")
        msg.setText("Please select an item to update.")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon("images/blue-circle-icon-info-png-clipart.jpg"))
        msg.exec_()
        return 
    else:
        if len(item) > 1:
            msg = QMessageBox()
            msg.setWindowTitle("Multiple selection")
            msg.setText("Please select only one item to update.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon("images/blue-circle-icon-info-png-clipart.jpg"))
            msg.exec_()
            return
        else:            
            text=item[0].text()

            if item:
            
                update_widget_.title_input.setText(text.split(" - ")[1])
                if text.split(" - ")[2]=="Book":
                    update_widget_.type_input.setCurrentText("Book")
                else:
                    update_widget_.type_input.setCurrentText("Movie")

                update_widget_.genre_input.setText(text.split(" - ")[3])
                update_widget_.rating_input.setText(text.split(" - ")[4])
                update_widget_.review_input.setText(text.split(" - ")[5])

                update_widget_.repaint()
                 
                
                update_widget_.show()
                print("lolololol")

                update_widget_.titlu_=text.split(" - ")[1]
                update_widget_.id=text.split(" - ")[0]
                print(update_widget_.id)
                print(update_widget_.titlu_)

                update_widget_.tip=update_widget_.type_input
                update_widget_.gen=update_widget_.genre_input
                update_widget_.rata=update_widget_.rating_input
                update_widget_.rev=update_widget_.review_input

                

             # Clear selection after loading data into update form

                self.list_widget.clearSelection()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("No selection")
                msg.setText("Please select an item to update.")
                msg.setIcon(QMessageBox.Warning)
                
                msg.setWindowIcon(QIcon("images/blue-circle-icon-info-png-clipart.jpg"))
                msg.exec_()

class Managebook(QWidget):

    emit_signal = pyqtSignal()

    emit_signal_update = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Books")
        self.resize(800, 500)

        main_layout=QVBoxLayout()

        ##top layout
        top_layout = QHBoxLayout()

        self.description=QLabel("Manage your media library: Add, delete, or update items.\n")

        self.description.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.description.setFixedSize(100, 50)

        top_layout.addWidget(self.description)
        self.description.setWordWrap(True)

        self.list_widget = QListWidget()
        
        self.reload_button = QPushButton("Reload")
        top_layout.addWidget(self.reload_button, alignment=Qt.AlignTop)
        self.reload_button.clicked.connect(lambda: load_data(self))

        self.add_button = QPushButton("Add")
        top_layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        switch_tab = pyqtSignal(int)
        self.add_button.clicked.connect(self.emit_signal)

        self.delete_button = QPushButton("Delete")

        top_layout.addWidget(self.delete_button, alignment=Qt.AlignTop)

        self.delete_button.clicked.connect(lambda: delete_item_from_db(self.list_widget))

        self.update_button = QPushButton("Update")
        top_layout.addWidget(self.update_button, alignment=Qt.AlignRight)
        self.update_button.clicked.connect(self.emit_signal_update)


        top_layout.addWidget(self.list_widget)

        ##bottom layolayout

        bottom_layout = QHBoxLayout()

        self.label = QLineEdit("Book/Movie Title:")
        bottom_layout.addWidget(self.label)

        self.search_button = QPushButton("Search")
        bottom_layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.search_books)

        ## assemble

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        database.cursor.execute("SELECT * FROM media")

        rows=database.cursor.fetchall()
        for row in rows:
            self.list_widget.addItem(str(row[0])+" - "+str(row[1])+" - "+str(row[2])+" - "+str(row[3])+" - "+str(row[4])+" - "+str(row[5]))
    
    def search_books(self):
        query=self.label.text().split(":")[1].strip()  # Extract the search term after the colon and remove extra spaces
        self.list_widget.clear()
        
        print(query)
        database.cursor.execute("SELECT * FROM media WHERE title LIKE ?", (f"%{query}%",))
        rows=database.cursor.fetchall()

        for row in rows:
            self.list_widget.clear()
            self.list_widget.addItem(str(row[0])+" - "+str(row[1])+" - "+str(row[2])+" - "+str(row[3])+" - "+str(row[4])+" - "+str(row[5]))

        
    def some_button_clicked(self):
        self.emit_signal.emit()

    
def load_data(self):
    self.list_widget.clear()

    database.cursor.execute("SELECT * FROM media")
    rows = database.cursor.fetchall()

    for row in rows:
        self.list_widget.addItem(
            f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}"
        )

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
        else:
            self.results_list.clear()
            for row in rows:
                self.results_list.addItem(row[0])
                self.results_list.clicked.connect(lambda: self.show_details(row[0]))  # connect click event to show details function

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
    
    ###add_item("The Great Gatsby", "Book", "Classic", "5 stars", "A timeless masterpiece.", "2024-06-01")
    ###add_item("Inception", "Movie", "Sci-Fi", "4.5 stars", "A mind-bending thriller.", "2024-06-02")
    ###add_item("Inception", "Movie", "Classic", "5 stars", "A powerful social commentary.", "2024-06-03")

    print(view_items())

    app=QApplication(sys.argv)
    
    main_=Managebook()

    add = add_widget(main_)

    update = update_widget(main_)
    
    def handle_switch_add():
        main_.hide()
        add.show()

    def handle_switch_update():
        item=list(main_.list_widget.selectedItems())
        if item:
            update_item_from_db(main_,update,item)

    main_.emit_signal.connect(handle_switch_add)

    main_.emit_signal_update.connect(handle_switch_update)

    main_.show()
    add.hide()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
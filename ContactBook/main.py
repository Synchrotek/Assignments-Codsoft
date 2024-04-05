import sys, random, string
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.uic import loadUi
import mysql.connector


class ContactBook(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ContactBook.ui", self)
        self.setWindowTitle("Contact Book")
        self.Handel_Buttons()

        # Initial Setup
        self.tabWidget.setCurrentIndex(0)
        reg_ex = QRegExp("[0-9]{1,10}")
        input_validator = QRegExpValidator(reg_ex, self.number_input)
        self.number_input.setValidator(input_validator)

    def Handel_Buttons(self):
        # Change tabs
        self.tab1_btn.clicked.connect(self.open_tab1)
        self.tab2_btn.clicked.connect(self.open_tab2)

        self.cadd_btn.clicked.connect(self.add_contact)
        self.showAll_contact_btn.clicked.connect(self.showAll_contact)

        self.csearch_btn.clicked.connect(self.search_contact)
        self.clear_Inpt_btn.clicked.connect(self.clearText_inTab2)
        self.cupdate_btn.clicked.connect(self.update_contact)
        self.cdelete_btn.clicked.connect(self.delete_contact)

    # ````````````````````````````````````````
    # ---------------------
    def open_tab1(self):
        self.tabWidget.setCurrentIndex(0)

    # ---------------------

    def open_tab2(self):
        self.tabWidget.setCurrentIndex(1)

    # ---------------------
    def add_contact(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cname = self.name_input.text()
        cnumber = self.number_input.text()
        cemail = self.email_input.text()
        cadress = self.address_input.toPlainText()

        if cname == "" or cnumber == "":
            QMessageBox.warning(self, "", "Invalid Number or Name")
            return

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO contact_book (cname,cnumber,cemail,cadress)
            VALUES (%s , %s , %s , %s)
        """,
            (
                cname,
                cnumber,
                cemail,
                cadress,
            ),
        )
        self.db.commit()

        self.statusBar().showMessage("New Contact Added")

        self.number_input.setText("")
        self.name_input.setText("")
        self.email_input.setText("")
        self.address_input.setText("")

        self.showAll_contact()

        self.db.close()

    # ---------------------
    def showAll_contact(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()
        cursor.execute("SELECT cnumber, cname, cemail FROM contact_book")
        data = cursor.fetchall()

        self.contact_showAll.setRowCount(0)
        self.contact_showAll.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.contact_showAll.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.contact_showAll.rowCount()
            self.contact_showAll.insertRow(row_position)

        self.db.close()

    # ---------------------
    def search_contact(self):
        cname = self.name_update_field.toPlainText()
        cnumber = self.number_update_field.toPlainText()

        if cname == "" and cnumber == "":
            QMessageBox.warning(self, "", "Invalid Number or Name")
            return

        search_value = cname if (cname != "") else cnumber
        search_query = "cname" if (search_value == cname) else "cnumber"

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT * FROM contact_book WHERE {search_query} = %s", [(search_value)]
        )
        data = cursor.fetchone()

        if data:
            self.name_update_field.setPlainText(data[0])
            self.number_update_field.setPlainText(data[1])
            self.email_update_field.setPlainText(data[2])
            self.address_update_field.setPlainText(data[3])
        else:
            QMessageBox.warning(
                self,
                "No contact found",
                """Given Contact-Info is \nNot present in Contact Book \nTry Adding it to Contact Book
                """,
            )

        self.db.close()

    # ---------------------
    def clearText_inTab2(self):
        self.name_update_field.setPlainText("")
        self.number_update_field.setPlainText("")
        self.email_update_field.setPlainText("")
        self.address_update_field.setPlainText("")

    # ---------------------
    def delete_contact(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        cname = self.name_update_field.toPlainText()
        cnumber = self.number_update_field.toPlainText()
        if cname == "" or cnumber == "":
            QMessageBox.warning(
                self, "", "Please Search the contact\n Before Deleting it"
            )
            return

        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM contact_book WHERE cnumber = %s", [(cnumber)])
        data = cursor.fetchone()
        if not data:
            QMessageBox.warning(self, "", "Given Number is not present in Contact Book")
            return

        warning = QMessageBox.warning(
            self,
            "Delete",
            (
                ("Contact details related to\n")
                + (f"given Number : {cnumber}\n")
                + ("will be deleted\n")
                + ("Do you Want to Proceed")
            ),
            QMessageBox.Yes | QMessageBox.No,
        )
        if warning == QMessageBox.No:
            return

        cursor.execute("DELETE FROM contact_book WHERE cnumber = %s", [(cnumber)])
        self.db.commit()
        self.statusBar().showMessage("Contact Deleted")

        self.clearText_inTab2()

        self.db.close()

    # ---------------------
    def update_contact(self):
        cname = self.name_update_field.toPlainText()
        cnumber = self.number_update_field.toPlainText()
        cemail = self.email_update_field.toPlainText()
        cadress = self.address_update_field.toPlainText()
        if cname == "" or cnumber == "":
            QMessageBox.warning(
                self, "", "Please Search the contact\n Before Updating it"
            )
            return

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )

        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM contact_book WHERE cnumber = %s", [(cnumber)])
        data = cursor.fetchone()
        if not data:
            QMessageBox.warning(self, "", "Given Number is not present in Contact Book")
            return

        warning = QMessageBox.warning(
            self,
            "Update",
            (
                ("The on-screen content of\n")
                + ("Name, Email Id and Address\n")
                + ("Will be updated and binded\n")
                + (f"with given Number : {cnumber}\n")
                + ("So make sure You modifed details Correctly\n")
                + ("  Do you Want to Proceed")
            ),
            QMessageBox.Yes | QMessageBox.No,
        )
        if warning == QMessageBox.No:
            return

        cursor.execute(
            """
            UPDATE contact_book SET
            cname = %s, cemail=%s, cadress=%s
            WHERE cnumber=%s
        """,
            (
                cname,
                cemail,
                cadress,
                cnumber,
            ),
        )
        self.db.commit()
        self.statusBar().showMessage("Contact Updated")

        self.db.close()

    # ---------------------
    # ````````````````````````````````````````


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ContactBook()
    main_window.show()
    sys.exit(app.exec_())

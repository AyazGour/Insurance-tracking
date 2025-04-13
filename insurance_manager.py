import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTableWidget, QTableWidgetItem, QMessageBox,
                           QFrame, QHeaderView, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database Setup
Base = declarative_base()
engine = create_engine('sqlite:///insurance.db', echo=True)
Session = sessionmaker(bind=engine)

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100))
    email = Column(String(100))
    policies = relationship("Policy", back_populates="client")

class Policy(Base):
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    policy_type = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    policy_number = Column(String(50))
    investment_amount = Column(Float, nullable=False)
    start_date = Column(String(20))
    end_date = Column(String(20))
    
    client = relationship("Client", back_populates="policies")

# Create tables
Base.metadata.create_all(engine)

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)

class StyledButton(QPushButton):
    def __init__(self, text, primary=True):
        super().__init__(text)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px;
                    background-color: #f5f5f5;
                    color: #333;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #bdbdbd;
                }
            """)

class SectionFrame(QFrame):
    def __init__(self, title=""):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
        """)
        self.layout = QVBoxLayout(self)
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #1976D2;
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
            """)
            self.layout.addWidget(title_label)

class InsuranceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insurance Policy Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("Insurance Policy Manager")
        header_label.setStyleSheet("""
            QLabel {
                color: #1976D2;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Search section
        search_frame = SectionFrame("Search Client")
        search_layout = QHBoxLayout()
        self.search_input = StyledLineEdit("Enter client name to search")
        search_button = StyledButton("Search")
        search_button.clicked.connect(self.search_client)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_frame.layout.addLayout(search_layout)
        layout.addWidget(search_frame)
        
        # Client and Policy section
        input_container = QHBoxLayout()
        
        # Add client section
        client_frame = SectionFrame("Add New Client")
        self.name_input = StyledLineEdit("Client Name")
        self.contact_input = StyledLineEdit("Contact Number")
        self.email_input = StyledLineEdit("Email Address")
        add_client_button = StyledButton("Add Client")
        add_client_button.clicked.connect(self.add_client)
        
        client_frame.layout.addWidget(self.name_input)
        client_frame.layout.addWidget(self.contact_input)
        client_frame.layout.addWidget(self.email_input)
        client_frame.layout.addWidget(add_client_button)
        input_container.addWidget(client_frame)
        
        # Add policy section
        policy_frame = SectionFrame("Add New Policy")
        self.policy_type_input = StyledLineEdit("Policy Type")
        self.company_input = StyledLineEdit("Insurance Company")
        self.policy_number_input = StyledLineEdit("Policy Number")
        self.amount_input = StyledLineEdit("Investment Amount")
        add_policy_button = StyledButton("Add Policy")
        add_policy_button.clicked.connect(self.add_policy)
        
        policy_frame.layout.addWidget(self.policy_type_input)
        policy_frame.layout.addWidget(self.company_input)
        policy_frame.layout.addWidget(self.policy_number_input)
        policy_frame.layout.addWidget(self.amount_input)
        policy_frame.layout.addWidget(add_policy_button)
        input_container.addWidget(policy_frame)
        
        layout.addLayout(input_container)
        
        # Results table
        table_frame = SectionFrame("Policy Records")
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Client Name", "Policy Type", "Company", 
            "Policy Number", "Investment Amount", "Contact", "Email"
        ])
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        table_frame.layout.addWidget(self.table)
        layout.addWidget(table_frame)
        
        self.current_client_id = None
        
    def search_client(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Warning", "Please enter a search term")
            return
            
        session = Session()
        try:
            clients = session.query(Client).filter(
                Client.name.ilike(f"%{search_term}%")
            ).all()
            
            self.table.setRowCount(0)
            for client in clients:
                for policy in client.policies:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    
                    self.table.setItem(row_position, 0, QTableWidgetItem(client.name))
                    self.table.setItem(row_position, 1, QTableWidgetItem(policy.policy_type))
                    self.table.setItem(row_position, 2, QTableWidgetItem(policy.company))
                    self.table.setItem(row_position, 3, QTableWidgetItem(policy.policy_number))
                    self.table.setItem(row_position, 4, QTableWidgetItem(f"${policy.investment_amount:,.2f}"))
                    self.table.setItem(row_position, 5, QTableWidgetItem(client.contact))
                    self.table.setItem(row_position, 6, QTableWidgetItem(client.email))
            
            if self.table.rowCount() == 0:
                QMessageBox.information(self, "Info", "No results found")
                
        finally:
            session.close()
    
    def add_client(self):
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter client name")
            return
            
        session = Session()
        try:
            new_client = Client(name=name, contact=contact, email=email)
            session.add(new_client)
            session.commit()
            self.current_client_id = new_client.id
            QMessageBox.information(self, "Success", "Client added successfully")
            
            # Clear inputs
            self.name_input.clear()
            self.contact_input.clear()
            self.email_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding client: {str(e)}")
            session.rollback()
        finally:
            session.close()
    
    def add_policy(self):
        if not self.current_client_id:
            QMessageBox.warning(self, "Warning", "Please add or search for a client first")
            return
            
        policy_type = self.policy_type_input.text().strip()
        company = self.company_input.text().strip()
        policy_number = self.policy_number_input.text().strip()
        
        try:
            amount = float(self.amount_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid investment amount")
            return
            
        if not all([policy_type, company, policy_number]):
            QMessageBox.warning(self, "Warning", "Please fill all policy fields")
            return
            
        session = Session()
        try:
            new_policy = Policy(
                client_id=self.current_client_id,
                policy_type=policy_type,
                company=company,
                policy_number=policy_number,
                investment_amount=amount
            )
            session.add(new_policy)
            session.commit()
            QMessageBox.information(self, "Success", "Policy added successfully")
            
            # Clear inputs
            self.policy_type_input.clear()
            self.company_input.clear()
            self.policy_number_input.clear()
            self.amount_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding policy: {str(e)}")
            session.rollback()
        finally:
            session.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Segoe UI", 10))
    
    window = InsuranceManager()
    window.show()
    sys.exit(app.exec()) 
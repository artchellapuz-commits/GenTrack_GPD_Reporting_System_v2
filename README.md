# GenTrack GPD Reporting System v2

A comprehensive web-based reporting system for Generation Plant Data (GPD) management, featuring real-time data tracking, Excel report generation, and secure e-signature functionality.

## 🌟 Features

### Core Functionality
- **Plant Status Reporting (PSR)** - Generate detailed plant status reports
- **Real-time Data Tracking** - Monitor generation data across multiple plants
- **Excel Report Generation** - Export reports in Excel format with custom formatting
- **Report Preview** - Preview reports before generation
- **Historical Data Management** - Import and manage historical plant data
- **Monthly Targets** - Set and track monthly generation targets

### E-Signature System
- **Digital Signatures** - Draw and save digital signatures
- **Authorization Workflow** - Request and approve signature authorizations
- **Persistent Signatures** - Signatures saved to database and reusable
- **2FA Security** - Two-factor authentication for signature operations
- **Audit Trail** - Complete logging of all signature activities
- **Email Notifications** - Automated email notifications for signature requests

### User Management
- **Role-Based Access Control** - Admin, Manager, and User roles
- **User Authentication** - Secure login with JWT tokens
- **Password Reset** - Self-service password reset workflow
- **Audit Logging** - Track all user actions and system events

### Data Management
- **Excel Import** - Import plant data from Excel files
- **Multi-Plant Support** - Manage data for multiple power plants
- **Unit-Level Tracking** - Track individual unit performance
- **Automated Reports** - Schedule automatic report generation

## 🏗️ Technology Stack

### Backend
- **Framework:** Django 4.2.7 + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **File Processing:** openpyxl, pandas
- **Email:** SMTP (Gmail)
- **Security:** Custom e-signature encryption

### Frontend
- **Framework:** Vue.js 3
- **UI Library:** Element Plus
- **HTTP Client:** Axios
- **Routing:** Vue Router
- **State Management:** Vuex (if applicable)

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/artchellapuz-commits/GenTrack_GPD_Reporting_System_v2.git
cd GenTrack_GPD_Reporting_System_v2
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env file with your configuration
# Update database credentials, email settings, etc.

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run serve
```

### 4. Access the Application

- **Frontend:** http://localhost:8080 or http://localhost:8081
- **Backend API:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

## ⚙️ Configuration

### Database Configuration

Edit `backend/.env`:

```env
DB_NAME=your_database_name
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Email Configuration

For Gmail SMTP, you need to:
1. Enable 2FA on your Gmail account
2. Generate an App Password
3. Update `backend/.env`:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Initial Data Setup

```bash
# Create plants and units
python manage.py shell
>>> from reports.models import Plant, Unit
>>> # Create plants as needed
```

## 📚 API Documentation

### Authentication

```bash
# Login
POST /api/auth/login/
{
  "username": "your_username",
  "password": "your_password"
}

# Get current user
GET /api/auth/profile/
Authorization: Bearer <token>
```

### Reports

```bash
# Generate report preview
POST /api/generation-reports/preview-report/
{
  "plant_codes": ["AGUS1", "AGUS2"],
  "start_date": "2026-05-07",
  "end_date": "2026-05-07",
  "report_type": "psr"
}

# Generate Excel report
POST /api/generation-reports/generate_report/
{
  "plant_codes": ["AGUS1", "AGUS2"],
  "start_date": "2026-05-07",
  "end_date": "2026-05-07",
  "report_type": "psr"
}
```

### E-Signatures

```bash
# Request signature authorization
POST /api/signatory-authorizations/request/
{
  "signatory_name": "O.M. LAVA",
  "role": "Prepared by:",
  "email": "user@example.com",
  "justification": "Need signature for PSR reports"
}

# Save drawn signature to report
POST /api/report-signatures/save-drawn-signature/
{
  "signatory_name": "O.M. LAVA",
  "signatory_role": "Prepared by:",
  "report_date": "2026-05-07",
  "report_type": "PSR",
  "signature": "data:image/png;base64,..."
}
```

## 🗂️ Project Structure

```
GenTrack_GPD_Reporting_System_v2/
├── backend/
│   ├── npc_reporting/          # Django project settings
│   ├── reports/                # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serializers
│   │   ├── services/          # Business logic
│   │   └── migrations/        # Database migrations
│   ├── media/                 # Uploaded files
│   │   ├── signatures/        # Report signatures
│   │   ├── admin_signatures/  # Reusable admin signatures
│   │   └── documents/         # Uploaded documents
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page views
│   │   ├── services/          # API services
│   │   ├── utils/             # Utility functions
│   │   └── router/            # Vue Router config
│   ├── public/
│   └── package.json
├── .gitignore
└── README.md
```

## 🔐 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt password hashing
- **CSRF Protection** - Custom CSRF exemption for API
- **2FA for Signatures** - Two-factor authentication for e-signatures
- **Audit Logging** - Complete audit trail of all actions
- **Role-Based Access** - Granular permission system
- **Signature Encryption** - Encrypted signature storage

## 📊 Database Models

### Key Models

- **Plant** - Power plant information
- **Unit** - Individual generation units
- **GenerationReport** - Daily generation data
- **ESignature** - Digital signature records
- **ReportSignature** - Signatures applied to reports
- **SignatoryAuthorization** - Signature authorization records
- **AuditLog** - System audit trail

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm run test
```

## 📝 Documentation

Additional documentation available in the repository:

- `SIGNATURE_SAVE_AND_NOTIFICATION.md` - E-signature system documentation
- `PERSISTENT_SIGNATURE_PREVIEW_SYSTEM.md` - Signature preview system
- `FRONTEND_SIGNATURE_INTEGRATION_GUIDE.md` - Frontend integration guide
- `EMAIL_CONFIGURATION_GUIDE.md` - Email setup guide
- `API_DOCUMENTATION.md` - Complete API reference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 👥 Authors

- **Development Team** - Initial work and ongoing development

## 🙏 Acknowledgments

- National Power Corporation (NPC)
- Generation Plant Division (GPD)
- Mindanao Generation Team

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

## 🔄 Version History

### v2.0.0 (Current)
- Complete system rewrite with Vue.js frontend
- Enhanced e-signature system with 2FA
- Persistent signature preview
- Improved report generation
- Email notification system
- Comprehensive audit logging

### v1.0.0
- Initial release
- Basic reporting functionality
- User management

## 🚧 Known Issues

- Frontend signature integration pending (see `FRONTEND_SIGNATURE_INTEGRATION_GUIDE.md`)
- Excel report signature images need dynamic loading implementation

## 🗺️ Roadmap

- [ ] Complete frontend signature integration
- [ ] Dynamic signature loading in Excel reports
- [ ] Mobile responsive design improvements
- [ ] Real-time data synchronization
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ for the National Power Corporation**

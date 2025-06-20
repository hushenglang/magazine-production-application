# Magazine Production Application

An AI-powered online magazine production application that automates content collection, processing, and magazine layout generation.

## 🚀 Overview

This application helps users create professional-looking magazines by:
- **Content Collection**: Automated web scraping and content aggregation
- **AI Processing**: Content summarization, title generation, and insights using Google Gemini
- **Magazine Generation**: Automated layout and design with customizable templates
- **User Management**: Role-based access control for editors and administrators

## 🏗️ Architecture

The application follows a **monolithic architecture** with separate frontend and backend services:

```
magazine-production-application/
├── docs/                           # Documentation
│   ├── PRD_Magazine_Production_Application.md
│   └── Technical_Architecture_Overview.md
├── magazine-production-service/    # Backend API (FastAPI + Python)
└── magazine-production-ui/         # Frontend (React + TypeScript) [Coming Soon]
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: MySQL 8.4 with SQLAlchemy
- **Authentication**: JWT with role-based access control
- **AI Integration**: Google Gemini 2.5 Flash API
- **Content Processing**: Trafilatura for web scraping

### Frontend (Planned)
- **Framework**: React 19 with TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **State Management**: Zustand

## 📋 Features

### ✅ Completed
- [x] **Authentication System**
  - User login/logout
  - JWT token management
  - Role-based access control (Admin/Editor)
  - Password management

- [x] **Backend Architecture**
  - FastAPI application structure
  - Database models and migrations
  - API documentation (OpenAPI/Swagger)
  - Environment configuration
  - Logging system

### 🚧 In Progress
- [ ] **Content Management**
  - Web content scraping
  - AI-powered content processing
  - Content library management

- [ ] **Magazine Generation**
  - Layout template system
  - Automated magazine creation
  - Export functionality

- [ ] **Frontend Application**
  - React UI components
  - User dashboard
  - Magazine builder interface

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MySQL 8.4+
- Node.js 18+ (for frontend)

### Backend Setup

1. **Navigate to backend service**:
   ```bash
   cd magazine-production-service
   ```

2. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Setup database**:
   ```sql
   CREATE DATABASE magazine_production;
   ```

5. **Create admin user**:
   ```bash
   python app/scripts/create_admin.py
   ```

6. **Run the application**:
   ```bash
   python -m app.main
   ```

The API will be available at: http://localhost:8000

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Documentation

- **[Product Requirements Document](docs/PRD_Magazine_Production_Application.md)**: Detailed feature specifications and requirements
- **[Technical Architecture](docs/Technical_Architecture_Overview.md)**: System design, database schema, and deployment architecture
- **[Backend API Guide](magazine-production-service/README.md)**: Backend service documentation

## 🔧 Development

### Project Structure
```
magazine-production-application/
├── .gitignore                      # Git ignore patterns
├── README.md                       # This file
├── docs/                          # Project documentation
├── magazine-production-service/   # Backend FastAPI service
│   ├── app/                      # Application code
│   │   ├── api/                  # API routes
│   │   ├── core/                 # Core configuration
│   │   ├── models/               # Database models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   └── utils/                # Utilities
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
└── magazine-production-ui/        # Frontend React application [Planned]
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🚀 Deployment

### Development
```bash
# Backend
cd magazine-production-service
python -m app.main

# Frontend (when available)
cd magazine-production-ui
npm run dev
```

### Production
- Backend: Deploy with Docker or direct Python deployment
- Frontend: Build and deploy to CDN/static hosting
- Database: MySQL 8.4+ with proper security configuration

## 📊 Current Status

**Version**: 1.0.0 (MVP Development)

**Completed Modules**:
- ✅ Authentication & User Management
- ✅ Backend API Structure
- ✅ Database Design
- ✅ Documentation

**Next Milestones**:
- 🚧 Content Scraping & AI Processing
- 🚧 Frontend React Application
- 🚧 Magazine Generation Engine

## 📞 Support

For questions, issues, or contributions:
- **Repository**: [GitHub Repository](https://github.com/hushenglang/magazine-production-application)
- **Issues**: Use GitHub Issues for bug reports and feature requests

## 📄 License

This project is developed for educational and portfolio purposes.

---

**Built with** ❤️ **using FastAPI, React, and AI technologies** 
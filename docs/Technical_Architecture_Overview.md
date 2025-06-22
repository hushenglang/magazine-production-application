# Technical Architecture Overview
# Online Magazine Production Application

## Document Information
- **Version**: 1.0
- **Date**: 2025-01-15
- **Author**: hushenglang
- **Status**: Draft
- **Related Document**: PRD_Magazine_Production_Application.md

## 1. Architecture Overview

### 1.1 Architecture Style
The application follows a **monolithic architecture** pattern, providing simplicity in development, deployment, and maintenance. All components are packaged and deployed as a single unit, which is suitable for the current scope and team size.

### 1.2 High-Level Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    Internet                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                AliCloud ECS Instance                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Docker Environment                     │  │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐ │  │
│  │  │   Application   │  │        MySQL Database      │ │  │
│  │  │   Container     │  │         Container           │ │  │
│  │  │                 │  │                             │ │  │
│  │  │  ┌───────────┐  │  │  ┌─────────────────────────┐│ │  │
│  │  │  │ Frontend  │  │  │  │     Content Data        ││ │  │
│  │  │  │(React+TW) │  │  │  │     User Data           ││ │  │
│  │  │  └───────────┘  │  │  │     Magazine Data       ││ │  │
│  │  │  ┌───────────┐  │  │  │     Media Metadata      ││ │  │
│  │  │  │ Backend   │  │  │  └─────────────────────────┘│ │  │
│  │  │  │(Python)   │  │  └─────────────────────────────┘ │  │
│  │  │  └───────────┘  │                                  │  │
│  │  └─────────────────┘                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              External Services                               │
│  ┌─────────────────┐  ┌─────────────────────────────────┐   │
│  │  Google Gemini  │  │        File Storage             │   │
│  │   2.5 Flash     │  │     (Local/Object Storage)      │   │
│  │      API        │  │                                 │   │
│  └─────────────────┘  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 2. Technology Stack

### 2.1 Frontend Technology
- **Framework**: React 19 with TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite or Create React App
- **HTTP Client**: Axios for API communication
- **State Management**: React Context API or Zustand
- **Routing**: React Router

### 2.2 Backend Technology
- **Runtime**: Python 3.12
- **Framework**: FastAPI
- **Language**: Python
- **Package Manager**: UV (ultraviolet) for fast dependency management
- **API Style**: RESTful APIs
- **Authentication**: JWT with session management
- **Validation**: Pydantic for request/response validation

### 2.3 Database
- **Primary Database**: MySQL 8.4
- **ORM**: SQLAlchemy with Alembic for migrations
- **Connection Pooling**: SQLAlchemy connection pooling
- **Database Driver**: aiomysql for async operations

### 2.4 External Integrations
- **LLM Service**: Google Gemini 2.5 Flash API(via OpenRouter), OpenAI Agents SDK
- **Web Scraping**: Trafilatura library
- **Image Processing**: Pillow (PIL) for image optimization

## 3. System Components

### 3.1 Frontend Components

#### 3.1.1 User Interface Modules
```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── content/
│   │   ├── ContentCollectionForm.tsx
│   │   ├── ContentLibrary.tsx
│   │   ├── ContentEditor.tsx
│   │   └── ContentPreview.tsx
│   ├── magazine/
│   │   ├── MagazineBuilder.tsx
│   │   ├── LayoutTemplates.tsx
│   │   └── PublishingPanel.tsx
│   └── common/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Loading.tsx
├── hooks/
├── services/
├── types/
└── utils/
```

#### 3.1.2 Key Features
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Preview**: Live magazine preview functionality
- **Drag & Drop**: Content arrangement with react-beautiful-dnd
- **Rich Text Editor**: Quill.js integration

### 3.2 Backend Components

#### 3.2.1 Core Services

##### Authentication Service
- **Purpose**: Authentication and authorization dependency injection
- **Features**:
  - JWT token validation and user extraction
  - Role-based access control enforcement
  - Current user context management
  - Security middleware integration

##### Content Management Service
- **Purpose**: Content management and storage
- **Features**:
  - Content storage and retrieval
  - Content metadata management

##### Content Scraping Service
- **Library**: Trafilatura for content extraction
- **Features**: 
  - URL validation and sanitization
  - Image URL extraction
  - Error handling for failed requests
  - Content cleaning and formatting

##### Content Processing Service
- **Purpose**: AI-powered content processing
- **Functions**:
  - Title generation
  - Summary creation
  - Key insights extraction
  - Content categorization

##### Image Processing Service
- **Library**: Pillow (PIL)
- **Features**:
  - Image download from URLs
  - Format conversion (WebP optimization)
  - Resizing for web display
  - Thumbnail generation
  - Storage management

## 4. Database Design

### 4.1 Core Tables

#### 4.1.1 Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    role ENUM('editor', 'admin') DEFAULT 'editor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 4.1.2 Content Types Table
```sql
CREATE TABLE content_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.3 Content Table
```sql
CREATE TABLE content (
    id INT PRIMARY KEY AUTO_INCREMENT,
    source_url VARCHAR(2048),
    raw_content LONGTEXT,  
    title VARCHAR(500),
    generated_title VARCHAR(500),
    summary TEXT,
    insights TEXT,
    content_type_id INT,
    status ENUM('pending', 'processing', 'completed') DEFAULT 'pending',
    language ENUM('en', 'zh') DEFAULT 'en',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (content_type_id) REFERENCES content_types(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 4.1.4 Images Table
```sql
CREATE TABLE images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content_id INT,
    original_url VARCHAR(2048),
    stored_path VARCHAR(1024),
    filename VARCHAR(255),
    file_size INT,
    width INT,
    height INT,
    alt_text VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE
);
```

#### 4.1.5 Magazines Table
```sql
CREATE TABLE magazines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    layout_config JSON,
    status ENUM('draft', 'review', 'published') DEFAULT 'draft',
    published_at TIMESTAMP NULL,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 4.1.6 Magazine Content Mapping
```sql
CREATE TABLE magazine_content (
    id INT PRIMARY KEY AUTO_INCREMENT,
    magazine_id INT,
    content_id INT,
    position_order INT,
    section_type VARCHAR(100),
    layout_settings JSON,
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES content(id)
);
```
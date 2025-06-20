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
- **API Style**: RESTful APIs
- **Authentication**: JWT with session management
- **Validation**: Pydantic for request/response validation
- **Async Support**: AsyncIO for concurrent operations

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

#### 3.2.1 API Structure
```
app/
├── api/
│   └── routers/
│       ├── auth.py
│       ├── content.py
│       ├── magazine.py
│       └── upload.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/
│   ├── user.py
│   ├── content.py
│   ├── magazine.py
│   └── content_type.py
├── schemas/
│   ├── user.py
│   ├── content.py
│   ├── magazine.py
│   └── auth.py
├── services/
│   ├── auth_service.py
│   ├── content_scraping_service.py
│   ├── gemini_service.py
│   ├── image_processing_service.py
│   └── magazine_service.py
├── utils/
│   ├── logger.py
│   └── helpers.py
└── main.py
```

#### 3.2.2 Core Services

##### Authentication Service
- **Purpose**: Authentication and authorization dependency injection
- **Features**:
  - JWT token validation and user extraction
  - Role-based access control enforcement
  - Current user context management
  - Security middleware integration

##### Content Scraping Service
- **Library**: Trafilatura for content extraction
- **Features**: 
  - URL validation and sanitization
  - Content type detection
  - Image URL extraction
  - Error handling for failed requests
  - Content cleaning and formatting

##### Gemini Integration Service
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

## 5. Deployment Architecture

### 5.1 Infrastructure Setup

#### 5.1.1 AliCloud ECS Configuration
- **Instance Type**: ecs.g6.large (2 vCPU, 8GB RAM) or similar
- **Operating System**: Ubuntu 20.04 LTS
- **Storage**: 20GB SSD for system + additional data disk for media
- **Network**: VPC with security group configuration
- **Backup**: Automated snapshot backups


## 6. Performance Optimization

### 6.1 Frontend Optimization
- **Code Splitting**: Lazy loading for route components
- **Image Optimization**: WebP format, responsive images
- **Caching**: Browser caching for static assets
- **Bundle Optimization**: Tree shaking and minification

### 6.2 Backend Optimization
- **Database Indexing**: Optimized queries with proper indexes
- **Connection Pooling**: Efficient database connections
- **Image Processing**: Async processing for large images

## 7. Monitoring & Logging

### 7.1 Application Monitoring
- **Health Checks**: Basic health endpoint monitoring
- **Error Tracking**: Structured error logging
- **Performance Metrics**: Response time and throughput monitoring


## 8. Future Considerations

### 8.1 Scalability Path
- **Horizontal Scaling**: Load balancer + multiple app instances
- **Database Scaling**: Read replicas for improved performance
- **CDN Integration**: Content delivery network for media files
- **Microservices Migration**: Breaking down monolith as needed

### 8.2 Feature Enhancements
- **Caching Layer**: Redis for session and content caching
- **Queue System**: Background job processing for heavy operations
- **API Rate Limiting**: Advanced rate limiting and throttling
- **Advanced Monitoring**: APM tools like New Relic or DataDog

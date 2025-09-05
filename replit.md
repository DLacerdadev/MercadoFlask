# Overview

This is a comprehensive ERP (Enterprise Resource Planning) system designed specifically for small to medium-sized markets and retail businesses. The system provides complete management capabilities for products, inventory, purchases, sales, and reporting. Built with Flask and SQLite, it offers a lightweight yet robust solution for market operations with real-time inventory tracking, transaction management, and business analytics.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **Authentication**: Session-based authentication with password hashing using Werkzeug
- **Application Structure**: Separation of concerns with distinct modules for models, routes, and application configuration

## Database Design
- **Database**: SQLite for lightweight, file-based data storage
- **Models**: Four core entities - User, Product, Purchase, and Sale with appropriate relationships
- **Data Integrity**: Foreign key relationships between transactions and products, with automatic timestamp tracking
- **Stock Management**: Real-time inventory updates through purchase and sale transactions

## Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **Icons**: Font Awesome for consistent iconography
- **Templates**: Jinja2 templating with base template inheritance
- **User Experience**: Dashboard-driven interface with intuitive navigation and real-time status indicators

## Security Features
- **Password Security**: Werkzeug password hashing for user credentials
- **Session Management**: Flask sessions with configurable secret keys
- **Route Protection**: Before-request middleware for authentication enforcement
- **Admin Controls**: Role-based access with admin user capabilities

## Business Logic
- **Inventory Management**: Automatic stock level updates on purchase/sale transactions
- **Stock Alerts**: Low stock warning system with configurable minimum thresholds
- **Transaction Tracking**: Complete audit trail for all business transactions
- **Reporting Engine**: Real-time analytics for sales performance and inventory status

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: CSS framework via CDN for responsive UI components
- **Font Awesome 6**: Icon library via CDN for consistent visual elements
- **Custom CSS**: Application-specific styling to complement Bootstrap theme

## Python Packages
- **Flask**: Core web framework for application routing and request handling
- **Flask-SQLAlchemy**: Database ORM integration with Flask
- **Werkzeug**: Security utilities for password hashing and authentication

## Database
- **SQLite**: Embedded database engine requiring no external server setup
- **File Storage**: Database stored as `market_erp.db` file in application directory

## Development Tools
- **Logging**: Python logging module for application debugging and monitoring
- **Environment Variables**: Support for environment-based configuration (session secrets)

Note: The system is designed to be self-contained with minimal external dependencies, making it ideal for small business deployments where simplicity and reliability are paramount.
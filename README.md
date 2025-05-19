# Citizen Complaints and Engagement System

A web-based platform that enables citizens to submit complaints or feedback on public services, allowing government agencies to respond effectively and track resolution progress.

## Live Demo

You can access the live application at:
[https://citizen-engagement-system-ebg6.onrender.com](https://citizen-engagement-system-ebg6.onrender.com)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Citizen Complaints and Engagement System addresses the challenge of fragmented complaint handling in public services. By providing a centralized platform, it improves response times, streamlines communication between citizens and government agencies, and enhances public service accountability.

This platform was developed as part of the Tech Associates Program Hackathon in Rwanda, focused on identifying talented developers and data scientists who can contribute to digital public infrastructure projects.

## Features

### Citizen Interface

- **Complaint Submission**: User-friendly form to submit complaints with details and optional attachments
- **Category Selection**: Organized categorization of complaints for appropriate routing
- **Tracking System**: Unique tracking ID for monitoring complaint status
- **Response Viewing**: Access to official responses and status updates

### Government Official Interface

- **Dashboard**: Overview of all complaints with filtering options
- **Analytics**: Visual representation of complaint data, trends, and performance metrics
- **Case Management**: Tools to update statuses and respond to complaints
- **Agency Assignment**: Automatic and manual routing to appropriate departments

### Administrative Functions

- **User Management**: Admin controls for government officials
- **Category Management**: Configuration of complaint categories and agency mappings
- **System Configuration**: Basic system settings and performance monitoring

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap, HTML, CSS, JavaScript, Chart.js
- **Database**: PostgreSQL
- **Deployment**: Render (Cloud Platform)

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Git

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/citizen-engagement-system.git
   cd citizen-engagement-system
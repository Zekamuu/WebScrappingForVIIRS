# Technical Design Document: Agricultural Fire Data Scraper

## 1. Project Overview

### 1.1 Purpose
This project is a web scraping application designed to automatically collect agricultural fire location data from the Bhuvan NRSC (National Remote Sensing Centre) portal for multiple Indian states. The scraper extracts fire coordinates from KML files and converts them into CSV format for analysis and storage.

### 1.2 Scope
The application currently supports data collection for three states:
- Punjab (PB)
- Uttar Pradesh (UP) 
- Haryana (HR)

### 1.3 Data Source
- **Primary Source**: Bhuvan NRSC Portal (https://bhuvan-app1.nrsc.gov.in/)
- **Data Type**: S-NPP VIIRS Active Agricultural Fire locations
- **Format**: KML files containing geographic coordinates
- **Update Frequency**: Multiple times per day (based on satellite passes)

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Bhuvan NRSC   │    │   Web Scraper   │    │   Local Storage │
│     Portal      │───▶│   Application   │───▶│   (CSV Files)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Component Overview
- **Data Source Layer**: Bhuvan NRSC web portal
- **Scraping Layer**: Python-based web scraper using requests and BeautifulSoup
- **Processing Layer**: KML parsing and coordinate extraction
- **Storage Layer**: Local file system with organized directory structure

## 3. Technical Specifications

### 3.1 Technology Stack
- **Language**: Python 3.x
- **Web Scraping**: 
  - `requests` (HTTP client)
  - `BeautifulSoup4` (HTML/XML parsing)
  - `lxml` (XML parser)
- **File Operations**: Built-in `os` module
- **Data Format**: CSV (comma-separated values)

### 3.2 Dependencies
```
beautifulsoup4==4.12.3
certifi==2024.8.30
charset-normalizer==3.4.0
idna==3.10
lxml==5.3.0
requests==2.32.3
soupsieve==2.6
urllib3==2.2.3
PyDrive==1.3.1
```

## 4. Data Flow Architecture

### 4.1 Process Flow
1. **Initialization**: Define state codes, names, and HTML element IDs
2. **Data Discovery**: Scrape the main portal to extract available date timestamps
3. **URL Construction**: Build download URLs for each timestamp
4. **File Download**: Retrieve KML files from the portal
5. **Data Extraction**: Parse KML files to extract coordinate data
6. **Data Storage**: Save coordinates as CSV files in organized directories
7. **Duplicate Prevention**: Skip existing files to avoid re-downloading

### 4.2 Data Structure

#### Input Data (KML Format)
```xml
<kml>
  <Document>
    <Placemark>
      <Point>
        <coordinates>longitude,latitude</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
```

#### Output Data (CSV Format)
```csv
75.78309631347656,29.88534927368164
76.0208511352539,29.912599563598633
75.7853012084961,29.958900451660156
```

## 5. Implementation Details

### 5.1 Core Function: `Download()`

#### Parameters
- `stCode` (string): State code (e.g., "PB", "UP", "HR")
- `stName` (string): State name for URL construction
- `level` (string): HTML element ID containing date information

#### Functionality
1. **URL Construction**: Builds state-specific URL for data discovery
2. **HTML Parsing**: Extracts date timestamps from specific HTML elements
3. **File Processing**: Downloads and processes KML files for each timestamp
4. **Directory Management**: Creates state-specific directories for file organization
5. **Error Handling**: Manages HTTP errors and file system operations

### 5.2 State-Specific Configuration

| State | Code | Name | HTML Element ID |
|-------|------|------|----------------|
| Punjab | PB | PUNJAB | minuslevel901 |
| Uttar Pradesh | UP | UTTAR%20PRADES | minuslevel31 |
| Haryana | HR | HARYANA | minuslevel31 |

### 5.3 File Organization Structure
```
project_root/
├── PB/                    # Punjab data directory
│   ├── 2024-12-03 02_43_35.85.csv
│   └── ...
├── UP/                    # Uttar Pradesh data directory
│   ├── 2024-12-03 01_03_18.65.csv
│   └── ...
├── HR/                    # Haryana data directory
│   ├── 2024-12-02 14_12_31.05.csv
│   └── ...
└── Done/                  # Completed/processed files
    └── ...
```

## 6. Data Processing Pipeline

### 6.1 Data Extraction Process
1. **Timestamp Extraction**: Parse HTML to find available fire detection timestamps
2. **URL Encoding**: Convert spaces to `%20` for URL compatibility
3. **Filename Generation**: Convert colons to underscores for file system compatibility
4. **KML Download**: Retrieve fire location data for specific timestamps
5. **Coordinate Extraction**: Parse KML XML to extract longitude,latitude pairs
6. **CSV Generation**: Write coordinates to CSV files with one coordinate pair per line

### 6.2 Data Quality Assurance
- **Duplicate Prevention**: Check for existing files before download
- **Error Handling**: Graceful handling of HTTP errors and network issues
- **Status Reporting**: Console output for download progress and errors

## 7. Performance Considerations

### 7.1 Scalability
- **Sequential Processing**: Current implementation processes states sequentially
- **File-based Storage**: Simple file system storage suitable for moderate data volumes
- **Memory Efficiency**: Processes files individually to minimize memory usage

### 7.2 Optimization Opportunities
- **Parallel Processing**: Could implement concurrent downloads for multiple states
- **Database Integration**: Consider database storage for large-scale data management
- **Caching**: Implement intelligent caching to reduce redundant downloads

## 8. Error Handling and Resilience

### 8.1 Error Scenarios
- **Network Failures**: HTTP request failures
- **Data Format Changes**: Changes in HTML structure or KML format
- **File System Issues**: Directory creation or file writing failures
- **Invalid Responses**: Malformed or empty responses from the portal

### 8.2 Current Error Handling
- HTTP status code validation
- File existence checks
- Graceful error messages with context
- Continuation of processing despite individual failures

## 9. Security Considerations

### 9.1 Data Privacy
- **Public Data**: Agricultural fire data is publicly available
- **No Authentication**: Portal does not require authentication
- **Read-Only Operations**: Application only reads data, no modifications

### 9.2 Network Security
- **HTTPS Usage**: All communications use HTTPS
- **No Sensitive Data**: No personal or sensitive information is processed
- **Rate Limiting**: Consider implementing delays to avoid overwhelming the source

## 10. Deployment and Operations

### 10.1 System Requirements
- **Python Environment**: Python 3.x with required packages
- **Network Access**: Internet connectivity for data source access
- **Storage Space**: Sufficient disk space for CSV file storage
- **Operating System**: Cross-platform (Windows, Linux, macOS)

### 10.2 Deployment Options
- **Local Execution**: Direct Python script execution
- **Scheduled Execution**: Cron jobs or Windows Task Scheduler
- **Container Deployment**: Docker containerization for consistent environments

## 11. Monitoring and Maintenance

### 11.1 Monitoring Requirements
- **Download Success Rate**: Track successful vs failed downloads
- **Data Freshness**: Monitor timestamps of latest available data
- **Storage Usage**: Monitor disk space consumption
- **Error Logging**: Track and analyze error patterns

### 11.2 Maintenance Tasks
- **Dependency Updates**: Regular updates of Python packages
- **HTML Structure Monitoring**: Watch for changes in source website structure
- **Data Validation**: Periodic validation of downloaded coordinate data
- **Storage Cleanup**: Archive or remove old data files as needed

## 12. Future Enhancements

### 12.1 Functional Improvements
- **Additional States**: Expand support to more Indian states
- **Data Visualization**: Add mapping and visualization capabilities
- **Real-time Processing**: Implement real-time data processing and alerts
- **API Development**: Create REST API for data access

### 12.2 Technical Improvements
- **Database Integration**: Migrate from file-based to database storage
- **Cloud Deployment**: Deploy to cloud platforms for scalability
- **Automated Testing**: Implement comprehensive test suite
- **Configuration Management**: Externalize configuration parameters

## 13. Risk Assessment

### 13.1 Technical Risks
- **Source Changes**: Portal structure changes could break scraping
- **Rate Limiting**: Excessive requests could result in IP blocking
- **Data Quality**: Inconsistent data formats or missing data
- **Dependency Vulnerabilities**: Security vulnerabilities in third-party packages

### 13.2 Mitigation Strategies
- **Robust Parsing**: Implement flexible HTML parsing with fallback options
- **Request Throttling**: Add delays between requests
- **Data Validation**: Implement data quality checks
- **Security Updates**: Regular dependency updates and vulnerability scanning

## 14. Conclusion

This agricultural fire data scraper provides a reliable solution for collecting and processing fire location data from the Bhuvan NRSC portal. The current implementation focuses on simplicity and reliability, with clear opportunities for future enhancements in scalability, performance, and functionality.

The modular design allows for easy extension to additional states and data sources, while the file-based storage approach provides a simple foundation that can be enhanced with database integration as requirements grow.

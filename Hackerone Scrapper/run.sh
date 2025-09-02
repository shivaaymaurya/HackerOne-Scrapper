#!/bin/bash

# HackerOne Link Scraper Runner Script

# Display help message
show_help() {
    echo "HackerOne Link Scraper - Usage Guide"
    echo "===================================="
    echo ""
    echo "This script helps you run the HackerOne Link Scraper with different options."
    echo ""
    echo "Usage: ./run.sh [option]"
    echo ""
    echo "Options:"
    echo "  all         Run all scrapers (CVE, CWE, disclosed, undisclosed)"
    echo "  cve         Run only the CVE scraper"
    echo "  cwe         Run only the CWE scraper"
    echo "  disclosed   Run only the disclosed reports scraper"
    echo "  undisclosed Run only the undisclosed reports scraper"
    echo "  test        Run the test suite"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh all          # Run all scrapers"
    echo "  ./run.sh cve          # Run only the CVE scraper"
    echo "  ./run.sh test         # Run the test suite"
    echo ""
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not installed."
        echo "Please install Python 3 and try again."
        exit 1
    fi
}

# Check if dependencies are installed
check_dependencies() {
    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt not found."
        echo "Please make sure you're in the correct directory."
        exit 1
    fi
    
    # Check if pip is installed
    if ! command -v pip3 &> /dev/null; then
        echo "Error: pip3 is not installed."
        echo "Please install pip3 and try again."
        exit 1
    fi
    
    # Check if dependencies are installed
    if ! python3 -c "import selenium, requests, bs4, tqdm, webdriver_manager" &> /dev/null; then
        echo "Some dependencies are missing. Installing..."
        pip3 install -r requirements.txt
    fi
}

# Main function
main() {
    # Check Python installation
    check_python
    
    # Check dependencies
    check_dependencies
    
    # Process command line arguments
    case "$1" in
        all)
            echo "Running all scrapers..."
            python3 main.py --type all
            ;;
        cve)
            echo "Running CVE scraper..."
            python3 main.py --type cve
            ;;
        cwe)
            echo "Running CWE scraper..."
            python3 main.py --type cwe
            ;;
        disclosed)
            echo "Running disclosed reports scraper..."
            python3 main.py --type disclosed
            ;;
        undisclosed)
            echo "Running undisclosed reports scraper..."
            python3 main.py --type undisclosed
            ;;
        test)
            echo "Running test suite..."
            python3 test_scrapers.py
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use './run.sh help' to see available options."
            exit 1
            ;;
    esac
}

# Run the main function with all arguments
main "$@"
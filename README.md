# SAP PromoteSync

## Overview
SAP PromoteSync is an innovative application designed to automate and enhance the accuracy of trade promotion compliance verification. Using cutting-edge technologies like computer vision and machine learning, PromoteSync streamlines the process of analyzing retail proof of performance submissions, ensuring precise and efficient reimbursement processing for promotional activities.

## Table of Contents
- [Project Objective](#project-objective)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Project Objective
To automate and enhance the accuracy of trade promotion compliance verification using computer vision and machine learning to analyze retail proof of performance submissions.

## Key Features
- **Promotional Object Extraction:** Utilizes advanced computer vision and machine learning algorithms to extract key objects and details from promotion proofs, including brands, products, and promotional setups.
- **Contract Management Integration:** Seamless integration with contract management systems for real-time extraction of contract details, ensuring promotions are executed within agreed parameters.
- **Automated Verification:** Automatically verifies promotion details against contract terms, ensuring accuracy and compliance while minimizing manual effort and errors.
- **User-Friendly Dashboard:** An intuitive interface for retail managers, trade claim managers, and claim analysts to manage and validate promotions.
- **Secure Login System:** Ensures secure access to the platform with role-based permissions.

## System Requirements
- **Operating System:** Windows, macOS, or Linux
- **Programming Languages:** Python 3.8+
- **Frameworks and Libraries:** TensorFlow, OpenCV, Streamlit
- **Database:** MongoDB

## Installation
### Prerequisites
1. Python 3.8 or higher

### Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/SAP-PromoteSync.git
   cd SAP-PromoteSync
   ```

2. **Backend Setup**
   - Create a virtual environment and activate it
     ```sh
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
     ```
   - Install the required dependencies
     ```sh
     pip install -r requirements.txt
     ```

3. **Frontend Setup**
   - Start the frontend development server
     ```sh
     streamlit run ui/app.py
     ```

## Usage
1. **Login** to the system using your credentials.
2. **View Promotions** on the Promotions Page to see all active, upcoming, and past promotions.
3. **Validate Promotions** by uploading proof images on the Promotion Validation Page. The system will analyze the images, extract necessary details, and match them against contract terms.
4. **Process Reimbursements** once the promotion proofs are validated, ensuring accurate and timely payments.

## Contact
For any inquiries or support, please contact:
- **Om Naik** - naiko@uci.edu
- **Deap Daru** - ddaru@uci.edu
- **Puneet Nagar** - puneetn@uci.edu
- **Raj Sanghavi** - rtsangha@uci.edu
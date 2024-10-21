# :pushpin: Milestone 1 :pushpin:

## :book: NutriNube :book:  
Version 0.0.1

---

Project Description

Many people struggle to maintain a healthy lifestyle due to poor dietary choices and a lack of physical activity. This often leads to various health issues, such as obesity, heart disease, and diabetes. One major challenge is tracking nutritional intake and calories burned, which can hinder progress towards better health.

#Possible Solution

The proposed solution is to develop a health tracker application that helps individuals monitor their food intake and physical activities. Key features will include:

- Food Tracking: Users can log their nutritional intake, including calories, protein, fat, and carbohydrates.
- Activity Tracking: Users can track their physical activities and calories burned.

The application will feature a simple, user-friendly interface to ensure accessibility for users of all technological backgrounds.

---

Project Environment

## 1. Environment Setup for Ubuntu

1.1 Install Git
Ensure that Git is installed on your system (Ubuntu in my case) by running the following command in your terminal:

bash
sudo apt install git


1.2 Create SSH Key Pair
To securely communicate with GitHub, create an SSH key pair by executing the following commands:

bash
ssh-keygen -t ed25519 -C "pfeiferj@silbador.de"

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519


1.3 Upload SSH Key to GitHub
Copy the SSH public key to your clipboard with the following command:

bash
cat ~/.ssh/id_ed25519.pub


- Log into your GitHub account.
- Navigate to Settings > SSH and GPG keys.
- Click New SSH key, paste the copied key, and give it a title for easy identification.

- <p align="center">
  <img src="/images/ssh.jpg" alt="SSH Configuration">
</p>

1.4 Configure User Information
Set your Git configuration with your name and email by running the following commands:

bash
git config --global user.name "Jan Pfeifer"
git config --global user.email "pfeiferj@silbador.de"


1.5 Enable Two-Factor Authentication
To enhance the security of your GitHub account, enable Two-Factor Authentication (2FA) by following these steps:

- Log into your GitHub account.
- Go to Settings > Password and authentication > Two-factor authentication.
- Select a 2FA method of your choice. In my case i already have configured 2FA by Passkey.
- If not already configured, add a new passkey on a device of yours. 

- <p align="center">
  <img src="/images/2fa.jpg" alt="2-Factor-Authentification">
</p>

## 2. Repository Creation
- A new repository, `CC-24-25_NutriNube`, was created on GitHub and initialized with a README file.

## 3. README.md
- The README file includes the problem description and key documentation links.

## 4. License Selection
- The GNU General Public License was selected to ensure the software can be used, modified, and distributed freely.

## 5. .gitignore
- A Python-template .gitignore file was created to exclude unnecessary files from version control.

## 6. Documentation Progress
- Ongoing project documentation can be found here for Milestone 1. Future milestones will be documented in a similar manner.

## 7. Issues and Milestones
- Tasks have been organized into GitHub issues, with a milestone created for project submission.

---

Simple Architecture Prototype

Below is a graphic that describes the first prototype of the application:

<p align="center">
  <img src="/images/simple_architecture.png" alt="Simple Architecture">
</p>

# :pushpin: Milestone 5: Deployment on a PaaS :pushpin:

## :book: NutriNube :book:  
Version 3.0.0

---

## Description of the Milestone

The aim of this milestone is to deploy the NutriNube application to the cloud using a Platform as a Service (PaaS) to understand and utilize techniques for cloud deployment from a web repository. Render.com was selected as the PaaS due to its free tier and simplicity. This milestone focuses on connecting the project repository to Render.com for seamless deployments.

---

## 1. PaaS Selection and Justification (2 points)

Render.com was chosen for the deployment of NutriNube primarily because:

- Cost-Effective: Offers a free tier that fits the project requirements without incurring additional costs.
- Ease of Use: Simplifies the deployment process by directly connecting to GitHub repositories, automating many tasks that typically require manual configuration. 

The selection criteria emphasized ease of integration with GitHub and straightforward deployment capabilities, making Render.com an apt choice for this milestone.

---

## 2. Deployment Process (2 points)

2.1 GitHub Integration

Render.com allows seamless integration with GitHub, enabling automatic deployment of the application with every new commit to the specified branch. Here are the steps followed:

- Connect Render.com account to the NutriNube GitHub repository.
- Configure Render.com to automatically deploy the application upon changes to the repository, utilizing the automatic deployment feature. 

#Additional Configuration

The only configuration change required in `app.py` was adding:
python
port = int(os.getenv('PORT', 5000))

This change ensures that the application listens on the correct port as specified by Render during runtime.

2.2 Automatic Deployment

Render.com’s default setting includes:
- Automatic deployment of services from a Git-backed repository when changes are pushed or merged to the linked branch. This feature was utilized for deploying NutriNube.
- Reference documentation: Render.com Automatic Deploys.

No additional configurations were necessary beyond this setup.

---

## 3. Deployment Configuration (2 points)

Since Render.com manages deployment, the majority of configurations are handled via their platform dashboard. Yet, the key steps are summarized within the project's README to ensure reproducibility for authorized users.

The setup process allows for direct deployment from the GitHub repository, ensuring that any push or merge to the main branch triggers a new deployment cycle on Render.com.

---

## 4. Application Deployment and Functionality (3 points)

The application was successfully deployed on Render.com, and its functionality verified. The deployment process mirrors the local execution setup, ensuring consistent operation across environments.

A URL pointing to the deployed application on Render.com is included in the project's main README file.

---

## 5. Performance Testing (1 point)

Performance Testing

#todo
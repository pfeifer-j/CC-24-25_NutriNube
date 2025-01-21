# :pushpin: Milestone 5: Deployment on a PaaS :pushpin:

## :book: NutriNube :book:  
Version 3.0.0

---

## Description of the Milestone

The goal of this milestone is to deploy the NutriNube application to the cloud using a Platform as a Service (PaaS). Here, [Render](https://render.com) was selected as the PaaS due to its free tier and simplicity. This milestone focuses on connecting the project repository to [Render](https://render.com) for seamless deployments.

---

## 1. PaaS Selection and Justification

[Render](https://render.com) was chosen for the deployment of NutriNube primarily because:

- It is cost-effective and offers a free tier that fits the project requirements without incurring additional costs.
- It simplifies the deployment process by directly connecting to GitHub repositories, automating many tasks that typically require manual configuration.
- Allows for automatic deployment with commits on the linked GitHub repository.

---

## 2. Deployment Process

[Render](https://render.com) allows simple integration with GitHub, with automatic deployment of the application with every new commit to the specified branch. To get the application running, the following steps are necessary:

1. Create an account on [Render](https://render.com).
2. Add a new workspace with a project. In my case, I added the workspace `CloudComputing` and the project `NutriNube`.
3. Within the project, create a new environment. I called mine `nutri_nube_env`.
4. In the newly created environment, web services and databases can be added.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5aba4326-a46c-4814-9f28-cbe0113a399b">
</p>

5. Add a new database.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f657cba3-9a75-4394-aac6-fd72f98479ba">
</p>

6. Select the free tier and the region `Frankfurt`. I named my database `nutri_nube_db`. On the configuration page, all the necessary URIs, passwords, and usernames must be added as environment variables.
<p align="center">
  <img src="https://github.com/user-attachments/assets/eb99d5e7-ddaf-48a2-8a46-1fcab64a9752">
</p>

7. Add the necessary environment variables for the database and the `flask` application.
<p align="center">
  <img src="https://github.com/user-attachments/assets/648fe8fd-3deb-4c99-bcf4-63c6710d0f9c">
</p>

8. Now select a web service.
<p align="center">
  <img src="https://github.com/user-attachments/assets/381b0130-883a-4e22-a516-583424b817f5">
</p>

9. Add the repository.
<p align="center">
  <img src="https://github.com/user-attachments/assets/a3577f2e-7822-47ac-80c8-3ed8f30c587e">
</p>

10. Select `Frankfurt` as the region and the free tier.
<p align="center">
  <img src="https://github.com/user-attachments/assets/84cbcff7-8aec-49ff-a1d8-ec70c843b1b1">
</p>

11. Activate automatic deployment on changes to the repository (this setting is usually on by default).
<p align="center">
  <img src="https://github.com/user-attachments/assets/19028c99-8a13-41ba-adf6-cd020a814ca0">
</p>

12. Finally, deploy the application.

### Drawbacks
Sadly, I was not able to get my logging container to run in the [Render](https://render.com) environment, since it requires a persistent storage volume to store the logs. However, this is not a big deal since my logger now just outputs the logs to the [Render](https://render.com) logging system where they are stored instead. So I have logging, but not by the use of `fluent` but the [Render](https://render.com) system. Locally, my logger functions perfectly, but I am not willing to pay the monthly subscription price for Render to enable the logging system in the deployed version as well.

### Additional Configuration

The only configuration change required in `app.py` and `__init__.py` was changing the port and loading the database address from [Render](https://render.com) instead of hardcoding it.

```python
port = int(os.getenv('PORT', 8000))
...
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
```

---

Since I also implemented a frontend, which was not required, I added favicons and DNS records so that I can reach my webpage using my own domain. The application NutriNube is now available on:

  1. [https://nutri-nube-docker.onrender.com](https://nutri-nube-docker.onrender.com)
  2. [https://silbador.de](https://silbador.de)

Since the services idle when not in use, the first connection can take 1-2 minutes for the services to start.

---

## 5. Performance Testing
A small performance test was also a task of this milestone. I manually clicked around and opened multiple sessions without experiencing any kind of performance drop.

As a more scientific approach, I tested the page using `Google Lighthouse` and got good scores:

<p align="center">
  <img src="https://github.com/user-attachments/assets/7087728e-5ac2-47b5-9590-1b5faa881e4a">
</p>

So, the website is up and running and works quite nicely. 

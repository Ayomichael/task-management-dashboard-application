<p><a target="_blank" href="https://app.eraser.io/workspace/pqCx9JVttXYKuNk2ju6p" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

Task Management Dashboard App MVP

1. Introduction
1.1 Purpose
This document outlines the architectural plan for the Minimum Viable Product (MVP) of the Task Management Dashboard App. It's intended for the project's development and future architects. It will guide the initial development and future enhancements.

1.2 Scope
The architecture covers the MVP of the Curriculum App, focusing on user account management, curriculum creation, viewing, updating, and deletion.

1.3 Definitions, Acronyms, and Abbreviations 

- MVP: Minimum Viable Product 
- API: Application Programming Interface 
- DB: Database
- App: Application

1.4 References



1.5 Overview
The document proceeds to detail the architectural style, system stakeholders and concerns, a high-level system overview, architectural strategies, system architecture, key decisions, quality attributes, risks, and technical debt.



2. Architectural Representation
2.1 Architectural Style and Rationale
The system will use a Monolithic Architectural Style for the MVP to simplify deployment and development. The task requires to focus on time to delivery. Given the scope and scale at this stage, a monolithic approach is time-effective and straightforward to implement.





3. System Stakeholders and Concerns
3.1 Stakeholders

- Users: Individuals creating and managing their learning curriculum.
- Developer: The team developing and maintaining the app.
3.2 System Concerns

- Performance: Ensuring the app is responsive and efficient.
- Scalability: Ability to accommodate a growing number of users.
- Security: Protecting user data and privacy.


4. System Overview
4.1 High-Level Description
The Task Management App allows users to create, manage, and update their tasks. It includes user authentication, task management.



5. Architectural Strategies
5.1 Key Strategies
Given the requirements for this project, we will use the follow technologies: 

-  Utilize HTML and Tailwind CSS for a dynamic and responsive front-end. 
- Implement Django for a robust back-end(API endpoints and database management). - Use Django's built-in User model. 
-  Use JQuery AJAX for Dynamic task loading to make requests to the API endpoints.
Given the security considerations for our system, we will use the following strategy:

- Security credentials will be stored in an `auth`  table in the database and related to the user table through a foreign key. This will make our system flexible enough to easily swap out this table for a third party auth service as our needs change.
- Passwords will be hashed and salted using standard encryption libraries.
- Authentication tokens will be passed between the front-end and the API to check for authorization for objects and resources.


6. App Architecture

6.1 Overview of Layers/Modules

- Front-End Module: Handles the user interface and client-side logic.
- Back-End Module: Manages server-side logic, API requests, and database interactions.
-  Database Module: Stores and retrieves all application data.
6.2 Component Diagrams

![Task Mgt. Component](/.eraser/pqCx9JVttXYKuNk2ju6p___LGpJOnbYLnQnYB9rdGHkpn0yBjH3___---figure---6LuTDv3WRV-zb_cXuihdi---figure---lTVO0ZxvHsp_ElUJ-B-K1A.png "Task Mgt. Component")

6.3 Database Design

- Users table: Stores user information and hashed passwords.
- Auth table: Stores hashed passwords with a foreign key reference to the user table.
- AuthCodes: Verification codes to confirm email address. They will expire after 30 minutes.
- Task table : Stores details of each curriculum, including sections and resources.


7. Key Architectural Decisions

7.1 Decision Log

- Monolithic Architecture: Chosen for its simplicity and ease of deployment for the MVP.
- Tech Stack Selection: Chosen based on Task assigned, project requirements, speed of development.


8. Quality Attributes

8.1 Performance

- Optimize response times with efficient API design and database indexing.
8.2 Scalability

- Prepare for future scaling by designing a modular and maintainable codebase.
8.3 Security

- Implement secure authentication, data validation, and encryption practices.
8.4 Maintainability

- Follow best coding practices and comprehensive documentation for easy maintenance.


9. Risks and Technical Debt

9.1 Identified Risks

- User Adoption: Risks related to market competition and user acquisition.
- Technical Challenges: Potential issues with integrating different technologies.
9.2 Technical Debt 

- Rapid Development: Some best practices might be compromised for faster MVP rollout.




<!--- Eraser file: https://app.eraser.io/workspace/pqCx9JVttXYKuNk2ju6p --->
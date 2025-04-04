# holbertonschool-HBnb - Technical Documentation
Project HBnB

## 1. Introduction

### 1.1 Document Purpose

The HBnB Evolution project aims to develop a simplified application inspired by Airbnb, allowing users to manage properties, leave reviews, and manage associated amenities. The first phase of the project focuses on creating technical documentation that will serve as the foundation for the system's design. This documentation will detail the overall architecture, business processes, and interactions between system entities, ensuring a clear understanding of the project. The goal is to lay the groundwork for scalable and flexible development.

### 1.2 Document Scope

This document provides a detailed description of the technical architecture of the HBnB project. It is structured into several sections, each covering a key aspect of the system:

📍**High-Level Architecture**:  
Overview of the system's three-layer architecture, along with a package diagram explaining the distribution of responsibilities and interactions between components. 

📍**Business Logic Layer**:  
Details on the design of models and their relationships, illustrated by a class diagram.

📍**API Interaction Flow**:  
Analysis of interactions between layers through sequence diagrams, highlighting the processing of user requests.

📍**Explanations and Justifications**:  
Each section is accompanied by detailed descriptions to clarify design choices and ensure a comprehensive understanding of how the system works.

## 2. High-Level Architecture

### 2.1 Overview

**HBnB follows a three-layer architecture:**

📍**Presentation Layer (API Services):** Handles user interactions and requests.

📍**Business Logic Layer (Models & Facade):** Manages application logic and data processing.

📍**Persistence Layer (Database Access):** Responsible for storing and retrieving data.

### 2.2 High-Level Package Diagram

The diagram below illustrates the structure and interactions between these layers:  
![diagramme_package__720](https://github.com/user-attachments/assets/ae639521-ec0a-49d4-b84f-2c4e5bb07c0b)

### 2.3 High-Level Package Explanation

The primary goal of this diagram is to provide an overview of the project and clearly understand the relationships between the different layers.  
Our high-level diagram describes the relationships between the three layers of our application. The first, PresentationLayer, handles the interface and requests via an API. The business layer enforces business rules and centralizes data management through a Facade and data models (User, Place, Review, Amenity).  
Finally, the persistence layer ensures communication with the database through repositories and a data access interface. Each layer is independent to keep the system clear, easier to modify, and maintain.  
The design is pyramidal, starting with the PresentationLayer, the highest layer of the project. Each line shows relationships between elements and user interactions. The diagram presents the main features, with colors derived from Airbnb's graphic guidelines.

### 2.4 Facade Model Explanation

The Facade Model simplifies interactions between layers. It acts as an interface between the presentation layer and business logic. It hides the complexity of the system by centralizing calls to various entities, preventing direct interaction with the database, thus following the encapsulation logic. This facilitates modularity, keeps the layers well-separated, and makes the project easier to maintain and evolve. It also simplifies interactions because the presentation layer interacts only with one class (Facade) instead of multiple business classes.

## 3. Business Logic Layer

### 3.1 Overview

The Business Logic Layer includes the main models representing the various entities in HBnB, such as users, places, reviews, and amenities. These models encapsulate the necessary logic for validation, processing, and interacting with the database.

### 3.2 Business Logic Class Diagram

![diagramme_de_classe_720](https://github.com/user-attachments/assets/c2a4cae3-e2f7-4d4c-b7b4-16cbf3eba3c1)

### 3.3 Explanation

**Our Business Logic Layer consists of different models:**

**Parent Class:**

This class, **BaseModel**, provides common attributes (id, created_at, updated_at) to other entities. It ensures better data consistency and guarantees a common structure.

**Main Classes:**

📍**User**: Represents a registered user with authentication details.

📍**Place**: Represents a rental unit with details such as location and price. It also manages amenities for the places.

📍**Review**: Contains reviews written by users about places.

📍**Amenity**: Represents additional amenities available in a place.

#### Relationships:

- A user owns several places.
- A user writes multiple reviews.
- A place receives multiple reviews.
- A place has several amenities.

### 3.4 Class Diagram Explanation

This class diagram represents the structure and interactions of the main entities in the housing management system. Its hierarchical structure provides a clear view of the relationships between these classes. The parent class centralizes common attributes and ensures data consistency.  
Classes User, Place, Review, Amenity inherit from BaseModel and have their own specific properties and methods. A User can create multiple Places, write Reviews, and have multiple Amenities. The color coding makes the document clearer and follows Airbnb's graphic guidelines.

## 4. API Interaction Flow

### 4.1 Overview

The API layer provides an interface allowing users to interact with the system. The API plays a crucial role in handling user requests, such as registering a user, creating a place, submitting a review, or retrieving places.  
The diagrams below correspond to each API call:

### 4.2 Sequence Diagram: User Registration:

![diagramme_user_register_720](https://github.com/user-attachments/assets/2934cbc4-e0d4-4354-b296-2163310736c9)

#### 4.3 Diagram Description:

The user provides their information to the API via a POST /register request. The API validates the data, then forwards the request to the facade, which redirects the request to the business logic for insertion into the database. Once the user is successfully added, the API returns a user ID or an error message.

#### 4.4 Step-by-Step Explanation:

- **1. User Initiates the Request:**  
  The user sends an HTTP POST /register request to the server with the necessary registration details: email, password, and name. This step begins the user registration process. The data is sent in JSON format in the request body.

- **2. API Processing:**  
  Action: The API receives the user’s request. It is responsible for handling communication with the client (the user) and validating the data.  
  The API passes the data to the Facade for validation.

- **3. Data Validation by the Facade:**  
  The Facade takes responsibility for validating the input data provided by the user. It checks if the information is correct and complete.  
  The Facade acts as an intermediary, ensuring that the data is ready for processing in the Business Logic.

- **4. User Creation by Business Logic:**  
  If the data validation is successful, the Facade passes the information to the Business Logic. The business logic handles the creation of the user in the system. For example, it can check if the email is already used and create a new account for the user.

- **5. Data Insertion into the Database:**  
  The Business Logic sends an SQL query to the database to insert a new user record. This query could be an `INSERT INTO users` statement that adds data to the `users` table in the database. This step permanently stores the user in the database so they can log in and interact with the system.

- **6. Database Response to Business Logic:**  
  The database returns a response to the Business Logic, either a success (if the user was created successfully) or a failure (if an error occurred, e.g., an existing email). The Business Logic receives feedback from the persistence layer to determine whether the action was successful.

- **7. Result Returned to the Facade:**  
  After the user is successfully created, the Business Logic returns the user ID to the Facade. The Facade receives the user ID and sends it to the API, which allows the API to provide accurate feedback to the user.

- **8. Response to the API:**  
  The Facade transmits the user ID or an error message (if creation failed) to the API. This step allows the API to prepare the response for the user.

- **9. Final Response to the User:**  
  The API sends an HTTP response back to the client (the user). If user creation is successful, it returns an HTTP 201 status code with the user ID or a success message. If an error occurred, the API will send an appropriate error message (e.g., email already used, weak password). This response informs the user whether their registration was successful or if an issue occurred.

#### 4.5 Diagram Design:

The diagram shows interactions between the user, API, Business Logic class, and the Database. It demonstrates all steps for user registration. The arrow system clarifies the system’s interactions. With a modular design, interactions between layers are more transparent and logical. The readability and structure help users understand each step.

### 4.6 Sequence Diagram: Creating a Place:

![diagramme_review_place_720](https://github.com/user-attachments/assets/4f147019-079e-45f4-bd54-d292c19dd7d9)

#### 4.7 Diagram Description:

The user submits a request to create a place, the system validates and stores the information in the database, and then returns the place ID or an error message.

### 4.8 Step-by-Step Description:

- **1. User Initiates the Request:**  
  The user sends an HTTP POST /register request to the server with the required place details.

- **2. API Processing:**  
  The API validates the request and forwards it to the Facade.

- **3. Data Validation by the Facade:**  
  The Facade validates the input data.

- **4. Place Creation by the Business Logic:**  
  The Business Logic handles the creation of the place.

- **5. Data Insertion into the Database:**  
  The Business Logic stores the place in the database.

- **6. Database Response to the Business Logic:**  
  The database confirms whether the place was successfully created.

- **7. Response to the API:**  
  The Facade returns the place ID or error message to the API.

- **8. Final Response to the User:**  
  The API sends a success or error message to the user.

### 4.9 Sequence Diagram: Creating a Review:

![review_sub_720](https://github.com/user-attachments/assets/50bd4309-3bbf-436e-bcfc-a8f63a208937)

#### 4.10 Diagram Description:

The user submits a review for a specific place, which is validated, inserted into the database, and the review ID is returned to the user.

### 4.11 Step-by-Step Description:

- **1. User:**  
  Sends a request to submit a review for a place.

- **2. API:**  
  Receives the request and forwards it to the Facade for validation.

- **3. Facade:**  
  Validates the review data and forwards it to the Business Logic.

- **4. Business Logic:**  
  Manages the logic for creating the review and associates it with the user and the place.

- **5. Database:**  
  Inserts the review into the database.

- **6. Facade:**  
  If the review is validated, returns the review ID to the API.

- **7. API:**  
  Sends the response back to the user with a success or error message.

### 4.12 Sequence Diagram: Retrieving Places:

![diagramme_liste_place_720](https://github.com/user-attachments/assets/f5c07774-6b1c-41f0-ba03-46285ff6b00f)

#### 4.13 Diagram Description:

The user requests a list of places in a given city, the system retrieves and returns the places corresponding to the specified city.

#### 4.14 Step-by-Step Description:

- **1. User:**  
  Sends a request to retrieve the list of places in a specific city (e.g., Rennes).

- **2. API:**  
  Receives the request and forwards the city to the Facade.

- **3. Facade:**  
  Asks the Business Logic to retrieve the places for the specified city.

- **4. Business Logic:**  
  Queries the database to get the places matching the city.

- **5. Database:**  
  Returns the list of places to the Business Logic.

- **6. Business Logic:**  
  Returns the list of places to the Facade.

- **7. Facade:**  
  Sends the list of places or an error message to the API.

- **8. API:**  
  Returns the final response to the user, with the list of places or an error message.

## 5. Conclusion

This document serves as a blueprint for the HBnB project, ensuring architectural clarity and guiding implementation. By following this structured design, developers can ensure scalability, readability, and maintainability throughout the project lifecycle.

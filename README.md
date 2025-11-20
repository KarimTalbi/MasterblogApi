# Masterblog API

This project is a simple and robust RESTful API for a blog platform, developed as part of a Masterschool assignment. It is built with Python and Flask, providing full CRUD (Create, Read, Update, Delete) functionality for blog posts.

## Features

-   **Full CRUD Operations:** Create, read, update, and delete blog posts.
-   **Powerful Search:** Filter posts by title, content, author, or date.
-   **Flexible Sorting:** Sort the post list by any field in either ascending or descending order.
-   **API Documentation:** Comprehensive API documentation is available via Swagger UI.

## Technology Stack

-   **Backend:** Python, Flask
-   **Package Management:** `uv`
-   **Data Storage:** JSON
-   **API Specification:** OpenAPI (Swagger 2.0)

## Getting Started

### Prerequisites

-   Python 3.8+
-   `uv` for package and environment management. You can install it by following the [official instructions](https://astral.sh/docs/uv#installation).

### Setup and Installation

1.  **Clone the repository:**
    
    ```bash
    git clone <repository-url>
    cd MasterblogApi2
    ```
    
2.  **Create a virtual environment and install dependencies:** `uv` can create a virtual environment and install dependencies from `pyproject.toml` and `uv.lock` in one step.
    
    ```bash
    uv sync
    ```
    
3.  **Activate the virtual environment:** The virtual environment is created in a `.venv` directory in the project root.
    
    ```bash
    # For macOS/Linux
    source .venv/bin/activate
    
    # For Windows
    ..venvScriptsactivate
    ```
    

### Running the Application

To start the Flask development server, run the following command from the `src/backend` directory:

```bash
python backend_app.py
```

The API will be available at `http://localhost:5002`.

## API Endpoints

The API provides the following endpoints for managing blog posts. For interactive documentation, run the application and navigate to `/api/docs` in your browser.

### Posts Collection

-   `GET /api/posts`
    
    -   **Description:** Retrieves a list of all blog posts.
    -   **Query Parameters:**
        -   `sort` (string, optional): Field to sort by (e.g., `date`, `title`).
        -   `direction` (string, optional): Sort order (`asc` or `desc`).
    -   **Response:** `200 OK` with a JSON array of post objects.
-   `POST /api/posts`
    
    -   **Description:** Creates a new blog post.
    -   **Request Body:** A JSON object representing the new post.
        
        ```json
        {
          "title": "New Post Title",
          "content": "Content of the new post.",
          "author": "Author Name"
        }
        ```
        
    -   **Response:** `201` Created with the newly created post object.

### Single Post

-   `GET /api/posts/{id}`
    
    -   **Description:** Retrieves a single post by its ID.
    -   **Response:** `200 OK` with the post object or `404 Not Found`.
-   `PUT /api/posts/{id}`
    
    -   **Description:** Updates an existing post.
    -   **Request Body:** A JSON object with the fields to be updated.
    -   **Response:** `200 OK` with the updated post object or `404 Not Found`.
-   `DELETE /api/posts/{id}`
    
    -   **Description:** Deletes a post by its ID.
    -   **Response:** `200 OK` with a confirmation message or `404 Not Found`.

### Search

-   `GET /api/posts/search`
    -   **Description:** Searches for posts matching one or more criteria.
    -   **Query Parameters:**
        -   `title` (string, optional)
        -   `content` (string, optional)
        -   `author` (string, optional)
        -   `date` (string, optional, format: `YYYY-MM-DD`)
    -   **Response:** `200 OK` with a JSON array of matching post objects or `404 Not Found`.

## Project Structure

```
src/backend/
├── data/
│   ├── json_handler.py   # Handles all logic for interacting with the JSON data file.
│   └── posts.json        # The database file for storing posts.
├── static/
│   └── masterblog.json   # OpenAPI specification file.
└── backend_app.py        # Main Flask application file, defines routes and error handlers.
```

---

This project was completed as an assignment for the Masterschool curriculum.
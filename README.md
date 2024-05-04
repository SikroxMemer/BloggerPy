<section style="display:flex;flex-direction:column;justify-content:center;align-items:center;align-content:center;">
    <?xml version="1.0"?><svg fill="#FD7E14" xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 128 128" width="128px" height="128px">    <path d="M15,109.8l48,17c0,0,0,0,0,0c0.1,0,0.2,0.1,0.3,0.1c0.2,0.1,0.5,0.1,0.7,0.1c0.2,0,0.3,0,0.5,0c0,0,0,0,0,0c0,0,0,0,0.1,0 c0.1,0,0.3-0.1,0.4-0.1c0,0,0,0,0,0l48-17c1.2-0.4,2-1.6,2-2.8V73.4l10-3.5c0.8-0.3,1.5-1,1.8-1.8s0.2-1.8-0.3-2.6l-12-20 c0,0-0.1-0.1-0.1-0.1c0-0.1-0.1-0.1-0.1-0.2c0,0,0,0,0,0c0-0.1-0.1-0.1-0.1-0.2c0,0,0,0,0-0.1c-0.1-0.1-0.1-0.1-0.2-0.2 c0,0-0.1-0.1-0.1-0.1c0,0-0.1-0.1-0.1-0.1c0,0-0.1,0-0.1,0c0,0-0.1-0.1-0.1-0.1c-0.1-0.1-0.2-0.1-0.3-0.1c-0.1,0-0.1-0.1-0.2-0.1 c0,0,0,0,0,0c0,0,0,0,0,0l-48-17c0,0,0,0-0.1,0c0,0-0.1,0-0.1,0c0,0-0.1,0-0.1,0c-0.1,0-0.1,0-0.2,0c0,0,0,0,0,0c0,0,0,0,0,0 c-0.1,0-0.1,0-0.2,0c-0.1,0-0.1,0-0.2,0c-0.1,0-0.2,0-0.4,0c-0.1,0-0.1,0-0.2,0c-0.2,0-0.4,0.1-0.5,0.1l-48,17 c-0.2,0.1-0.3,0.1-0.5,0.2c0,0-0.1,0.1-0.1,0.1c-0.1,0.1-0.2,0.1-0.3,0.2c0,0-0.1,0.1-0.1,0.1c-0.1,0.1-0.2,0.1-0.2,0.2 c0,0-0.1,0.1-0.1,0.1c-0.1,0.1-0.1,0.2-0.2,0.2c0,0,0,0.1-0.1,0.1l-12,20c-0.7,1.1-0.6,2.5,0.2,3.4C2.3,69.6,3.1,70,4,70 c0.3,0,0.7-0.1,1-0.2l8-2.8v40C13,108.3,13.8,109.4,15,109.8z M119.5,65.4l-42.2,15l-8.9-14.8l42.2-15L119.5,65.4z M67,34.2L103,47 L67,59.8V34.2z M67,74.8l6.4,10.7C74,86.5,75,87,76,87c0.3,0,0.7-0.1,1-0.2l32-11.3v29.4l-42,14.9V74.8z M19,51.2l42,14.9v53.6 l-42-14.9V51.2z"/></svg>
    <h3>Stack : An open source article / blog site for the discussion of a variety of topics</h3>
</section>

## Introduction

Stack is a web application built using Flask, a Python web framework, designed for creating and managing blog posts and discussions. The app allows users to register, create posts, comment on posts, and manage their own content. Posts are organized by categories or topics, providing a structured way to navigate and explore different subjects within the app.

## **Features**

1. **User Authentication**
    - Users can register and log in to the Stack app to create and manage their posts.
    - User passwords are securely hashed and stored to ensure privacy and security.
2. **Post Management**
    - Users can create new blog posts, which can be categorized into specific topics or categories.
    - Each post can be edited or deleted by the user who created it.
3. **Commenting**
    - Users can comment on posts to engage in discussions related to the content.
    - Comments can also be edited or deleted by the user who posted them.
4. **Category/Topic Organization**
    - Posts are organized based on categories or topics, allowing users to browse and filter content based on their interests.
    - Each category/topic has its own page displaying relevant posts.

## **Installation**

To run the Stack app locally, follow these steps

```bash
git clone https://github.com/SikroxMemer/Stack.git
cd stack-app
```

**Create a Virtual Environment (Optional)**

```bash
# Linux & Mac

python -m venv venv
source venv/bin/activate 

# Windows

py -m venv venv
.\venv\bin\activate
```

**Install Dependencies**

```bash
pip install -r requirements.txt
```

**Run the Application**

```bash
py flask-project run

# or 

python3 flask-project run
```

## **Contributing**

Contributions to Stack are welcome! If you'd like to contribute:

## License

This project follows the MIT Open Source license [here](./LICENSE.md)

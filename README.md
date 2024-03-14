# Armada API

## Overview
This repository hosts the updated Armada API, showcasing advanced AI-powered automation through hierarchical, asynchronous tasks with callbacks and predefined expected outputs. It is designed to consume requests for automated tasks and execute those tasks.

## Features
- **Hierarchical Task Management:** Leverage the power of structured task execution to maintain a clean and scalable codebase.
- **Asynchronous Tasks:** Improve performance with non-blocking operations, allowing tasks to run concurrently.
- **Callbacks:** Ensure that each task can trigger subsequent actions upon completion, enabling a reactive task flow.
- **Expected Outputs:** Define the anticipated results for each task, streamlining debugging and ensuring quality control.

## Installation

### MacOS/Linux

To get started with the Armada API, clone the repository and install the necessary dependencies.

1. Install Homebrew

``` 
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

   Verify Homebrew installation

```bash
brew --version
```

2. Update Homebrew

```bash
brew update
```

3. Install Python 3

```bash
brew install python
```

   Verify Python installation

 ```bash
python3 --version
```

4. Install Poetry

```bash
brew install poetry
```

   Verify Poetry installation

```bash
poetry --version
```

5. Open your terminal and navigate to the existing project directory (the one containing the pyproject.toml file).

If this is your first time working with this project, or if new dependencies have been added since the last time you worked on it, run

```bash
poetry install
```

This command reads the pyproject.toml file and installs all the dependencies listed there, creating a virtual environment if one does not already exist.

6. Activate the Poetry environment

```bash
poetry shell
```

This command activates the project's virtual environment, allowing you to run Python and other commands within the context of your project's dependencies.
To activate an existing virtual environment you must first go to the root of the project that uses it.

```bash
cd /path/to/other/project
```

Then you must run the following:

```bash
poetry env info -p
```

Lastly, you must copy the path that you see appending '/bin/activate' to it and execute the following:

```bash
cd /path/to/your/project
source /path/to/virtualenv/bin/activate
```

7. In the shell, to build and install the project run the following:

```bash
poetry build && poetry install
cd dist
pip install armada_api-0.1.0.tar.gz
cd ..
```

## Usage

### Starting Celery

To start the Celery worker for asynchronous task processing, run the following command from the root directory of your project:

```bash
poetry run celery -A armada.main.celery worker --loglevel=info
````

### Stopping Celery

To gracefully stop your Celery worker, you can use the following command:

```shell
celery -A armada.main.celery control shutdown
````

To run the Armada API, execute the main script after setting up your environment variables and configuration.

### Development

``` 
poetry run python -m armada.main
```

### Production

``` 
poetry run gunicorn 'armada.main:app' -b :11000
```

## Structure
main.py: The entry point script that listens to incoming requests, and forms the AI crew.

concierge.py: The script that configures and initiates a concierge by mapping specific tools and callbacks to assistants.

agents.py: Defines various agents like the editor, news fetcher, news analyzer, and newsletter compiler.

tasks.py: Contains the task definitions that are used by the agents to perform specific operations.

file_io.py: Manages file input/output operations, crucial for handling the async flow of data.

### JSON Request Example

Armada is composed of a concierge with tasks orchestrated to perform complex A.I. automation.

```
{
  "agents": [
    {
      "role": "Editor",
      "goal": "Oversee the creation of the AI Newsletter",
      "backstory": "With a keen eye for detail and a passion for storytelling, you ensure that the newsletter not only informs but also engages and inspires the readers.",
      "allow_delegation": true,
      "verbose": true,
      "max_iter": 15,
      "tasks": []
    },
    {
      "role": "NewsFetcher",
      "goal": "Fetch the top AI news stories for the day",
      "backstory": "As a digital sleuth, you scour the internet for the latest and most impactful developments in the world of AI, ensuring that our readers are always in the know.",
      "tools": ["search_internet"],
      "verbose": true,
      "allow_delegation": true,
      "tasks": [
        {
          "id": "fetch_news",
          "description": "Fetch top AI news stories from the past 24 hours.",
          "async_execution": true,
          "context": [],
          "expected_output": "A list of top AI news story titles, URLs, and a brief summary for each story from the past 24 hours. Example Output: [ { 'title': 'AI takes spotlight in Super Bowl commercials', 'url': 'https://example.com/story1', 'summary': 'AI made a splash in this year's Super Bowl commercials...' }, { ... } ]"
        }
      ]
    },
    {
      "role": "NewsAnalyzer",
      "goal": "Analyze each news story and generate a detailed markdown summary",
      "backstory": "With a critical eye and a knack for distilling complex information, you provide insightful analyses of AI news stories, making them accessible and engaging for our audience.",
      "tools": ["search_internet"],
      "verbose": true,
      "allow_delegation": true,
      "tasks": [
        {
          "id": "analyze_news",
          "description": "Analyze each news story and ensure there are at least 5 well-formatted articles.",
          "async_execution": true,
          "context": ["fetch_news"], // This should be the identifier of the 'fetch news' task
          "expected_output": "A markdown-formatted analysis for each news story, including a rundown, detailed bullet points, and a \"Why it matters\" section. There should be at least 5 articles, each following the proper format. Example Output: '## AI takes spotlight in Super Bowl commercials\n\n**The Rundown:** AI made a splash in this year's Super Bowl commercials...\n\n**The details:**\n\n- Microsoft's Copilot spot showcased its AI assistant...\n\n**Why it matters:** While AI-related ads have been rampant over the last year, its Super Bowl presence is a big mainstream moment.\n\n'"
        }
      ]
    },
    {
      "role": "NewsletterCompiler",
      "goal": "Compile the analyzed news stories into a final newsletter format",
      "backstory": "As the final architect of the newsletter, you meticulously arrange and format the content, ensuring a coherent and visually appealing presentation that captivates our readers.",
      "verbose": true,
      "tasks": [
        {
          "id": "compile_newsletter",
          "description": "Compile the newsletter.",
          "async_execution": false,
          "context": ["analyze_news"], // This should be the identifier of the 'analyze news' task
          "expected_output": "A complete newsletter in markdown format, with a consistent style and layout. Example Output: '# Top stories in AI today:\\n\\n- AI takes spotlight in Super Bowl commercials\\n- Altman seeks TRILLIONS for global AI chip initiative\\n\\n## AI takes spotlight in Super Bowl commercials\\n\\n**The Rundown:** AI made a splash in this year's Super Bowl commercials...\\n\\n**The details:**...\\n\\n**Why it matters::**...\\n\\n## Altman seeks TRILLIONS for global AI chip initiative\\n\\n**The Rundown:** OpenAI CEO Sam Altman is reportedly angling to raise TRILLIONS of dollars...\\n\\n**The details:**...\\n\\n**Why it matters::**...\\n\\n'",
          "callback": "save_markdown"
        }
      ]
    }
  ],
  "process": "hierarchical",
  "manager_llm": {
    "model": "gpt-3.5-turbo-0613"
  },
  "verbose": 2
}
```

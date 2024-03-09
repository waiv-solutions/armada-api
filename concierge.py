from tools.search_tools import SearchTools
from file_io import save_markdown
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

# Define a mapping from string identifiers to actual functions
tool_mapping = {
    "search_internet": SearchTools.search_internet
}

callback_mapping = {
    'save_markdown': save_markdown
}

# Initialize Agents from request data
def initialize_concierge(request_data):
    tasks_dict = {}
    agents = []
    tasks = []

    for agent_info in request_data["agents"]:
        agent = Agent(
            role=agent_info["role"],
            goal=agent_info["goal"],
            backstory=agent_info.get("backstory", ""),
            allow_delegation=agent_info.get("allow_delegation", False),
            verbose=agent_info.get("verbose", False),
            max_iter=agent_info.get("max_iter", 10)
        )
        if "tools" in agent_info:
            agent_tools = [tool_mapping[tool] for tool in agent_info["tools"]]
            agent.tools = agent_tools

        agent_tasks = []
        for task_info in agent_info.get("tasks", []):
            context_tasks = [tasks_dict[ct] for ct in task_info.get("context", []) if ct in tasks_dict]
            task = Task(
                description=task_info["description"],
                agent=agent,
                async_execution=task_info.get("async_execution", False),
                context=context_tasks,
                expected_output=task_info.get("expected_output", "")
            )
            if 'callback_function' in task_info and task_info['callback_function'] in callback_mapping:
                task.callback = callback_mapping[task_info['callback_function']]

            agent_tasks.append(task)
            tasks_dict[task_info["id"]] = task  # Assuming each task has a unique ID

        tasks.extend(agent_tasks)
        agents.append(agent)

    # Prepare manager LLM
    manager_llm_params = request_data.get('manager_llm', {})
    manager_llm = ChatOpenAI(
        model=manager_llm_params.get('model', 'gpt-3')
    )

    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process[request_data.get('process', 'hierarchical')],
        manager_llm=manager_llm,
        verbose=request_data.get('verbose', 2)
    )

def execute_concierge(crew):
    return crew.kickoff()
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI
from .file_io import save_markdown
from ..tools.search_tools import SearchTools

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
    temp_tasks_with_context = []

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
            agent.tools = [tool_mapping[tool] for tool in agent_info["tools"]]

        for task_info in agent_info.get("tasks", []):
            task = Task(
                description=task_info["description"],
                agent=agent,
                async_execution=task_info.get("async_execution", False),
                context=[],  # Context to be set later
                expected_output=task_info.get("expected_output", "")
                
            )
            if 'callback' in task_info:
                task.callback = callback_mapping.get(task_info['callback'])
            tasks_dict[task_info["id"]] = task
            temp_tasks_with_context.append((task, task_info.get("context", [])))

        agents.append(agent)

    # Now, update each task's context based on IDs after all tasks have been created
    for task, context_ids in temp_tasks_with_context:
        task.context = [tasks_dict[ct_id] for ct_id in context_ids if ct_id in tasks_dict]
        tasks.append(task)  # Now append the correctly contextualized task to the tasks list

    # Prepare manager LLM
    manager_llm = ChatOpenAI(
        model=request_data['manager_llm'].get('model', 'gpt-3')
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
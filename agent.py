# For Maa Pipeline VSCode Extension & Maa Debugger to run custom
import sys

print(sys.prefix)
print(sys.executable)


def main():
    from maa.agent.agent_server import AgentServer
    from maa.toolkit import Toolkit
    
    Toolkit.init_option("./assets/cache/agent/")

    from app.utils.maafw.custom import custom_registry
    for name, recognition in custom_registry.custom_recognition_holder.items():
        if AgentServer.register_custom_recognition(name, recognition):
            print("Successfully registered ", name, recognition)
        else:
            print("[Warning] Failed to register ", name, recognition)
    for name, action in custom_registry.custom_action_holder.items():
        if AgentServer.register_custom_action(name, action):
            print("Successfully registered ", name, action)
        else:
            print("[Warning] Failed to register ", name, action)

    socket_id = sys.argv[-1]

    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()

if __name__ == "__main__":
    main()

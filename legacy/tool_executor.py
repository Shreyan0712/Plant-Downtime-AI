from app.llm.api_tools import (

    #Machines

    get_machines,
    create_machine,
    update_machine,
    delete_machine,

    #Maintenance Logs

    get_maintenance_logs,
    create_maintenance_log,
    update_maintenance_log,
    delete_maintenance_log,

    #Downtime Events

    get_downtime_events,
    create_downtime_event,
    update_downtime_event,
    delete_downtime_events,

    #Downtime causes
    get_downtime_causes,
    create_downtime_cause,
    update_downtime_cause,
    delete_downtime_causes

)

def execute_action(parsed_action):

    operation = parsed_action.get(
        "operation"
    )

    entity = parsed_action.get(
        "entity"
    )

    action_id = parsed_action.get(
        "id"
    )

    data = parsed_action.get(
        "data"
    )

    
    #-------------------MACHINES-------------------#

    if entity == "machines":

        if operation == "get":

            return get_machines()

        elif operation == "create":

            return create_machine(data)
        
        elif operation == "update":

            return update_machine(
                action_id,
                data
            )

        elif operation == "delete":

            return delete_machine(
                action_id
            )

    #-------------------MAINTENANCE LOGS-------------------#

    elif entity == "maintenance_logs":

        if operation == "get":

            return get_maintenance_logs()


        elif operation == "create":

            return create_maintenance_log(
                data
            )


        elif operation == "update":

            return update_maintenance_log(
                action_id,
                data
            )


        elif operation == "delete":

            return delete_maintenance_log(
                action_id
            )
    
    
     #-------------------DOWNTIME EVENTS-------------------#

    elif entity == "downtime_events":

        if operation == "get":

            return get_downtime_events()


        elif operation == "create":

            return create_downtime_event(
                data
            )


        elif operation == "update":

            return update_downtime_event(
                action_id,
                data
            )


        elif operation == "delete":

            return delete_downtime_events(
                action_id
            )

    #-------------------DOWNTIME CAUSES-------------------#

    elif entity == "downtime_causes":

        if operation == "get":

            return get_downtime_causes()


        elif operation == "create":

            return create_downtime_cause(
                data
            )


        elif operation == "update":

            return update_downtime_cause(
                action_id,
                data
            )


        elif operation == "delete":

            return delete_downtime_causes(
                action_id
            )


    return {
        "error": "Unsupported operation"
    }
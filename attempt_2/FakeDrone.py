from pioneer_sdk import Pioneer
import time

def get_heartbeat(pioneer_drone):
    '''
    check a state of autopilot and connection with drone
    :param drone: class Pioneer()
    :return:None
    '''
    print(f"State of autopilot {pioneer_drone.get_autopilot_state()}")
    print(f'Check link to drone {pioneer_drone.connected()}')


def get_telemetry(pioneer_drone):
    '''
    show a current telemetry of drone
    :param drone: class Pioneer()
    :return:None
    '''
    print(f"Battery status {pioneer_drone.get_battery_status()}")


if __name__ == "__main__":
    drone = Pioneer()
    drone.arm()
    time.sleep(0.1)
    drone.takeoff(2)
    time.sleep(0.2)
    get_heartbeat(drone)
    get_telemetry(drone)
    drone.land()
    time.sleep(0.2)
    drone.close_connection()
    del drone


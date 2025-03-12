from microbit import sleep, pin14, pin15


# Inicializace proměnných pro pravý enkodér
last_state_right = pin15.read_digital()
total_ticks_right = 0

# Inicializace proměnných pro levý enkodér
last_state_left = pin14.read_digital()
total_ticks_left = 0

def left_sum_ticks():
    global last_state_left, total_ticks_left
    raw_data_left = pin14.read_digital()
    # Počítání celkových tiků pro levý enkodér
    if last_state_left != raw_data_left:
        total_ticks_left += 1
    
    last_state_left = raw_data_left
    return total_ticks_left
def right_sum_ticks():
    global last_state_right, total_ticks_right
    raw_data_right = pin15.read_digital()
    # Počítání celkových tiků pro pravý enkodér
    if last_state_right != raw_data_right:
        total_ticks_right += 1
    
    last_state_right = raw_data_right
    return total_ticks_right

if __name__ == "__main__":

    while True:
        print(left_sum_ticks(), right_sum_ticks())
        sleep(5)

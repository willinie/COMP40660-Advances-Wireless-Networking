import math


# Standards' attributes
std_g = {
    "frame_size": 1542, #bytes
    "SIFS": 10, #μs
    "DIFS": 28, #μs
    "SDur": 4, #μs
    "min_data_rate": 6, #Mbps
    "max_data_rate": 54, #Mbps
    "min_NBits": 1,
    "min_CRate": 1/2,
    "min_NChan": 48,
    "max_NBits": 6,
    "max_CRate": 3/4,
    "max_NChan": 48,
    "Nss": 1,
    "min_preamble": 20,  # μs
    "max_preamble": 20, #μs
    "TCP_ACK_frame_size": 82 #bytes
}

std_ac_w2_normal = {
    "frame_size": 1548, #bytes
    "SIFS": 16, #μs
    "DIFS": 34, #μs
    "SDur": 3.6, #μs
    "min_data_rate": 7.2, #Mbps
    "max_data_rate": 6933.6, #Mbps
    "min_NBits": 1,
    "min_CRate": 1/2,
    "min_NChan": 52,
    "max_NBits": 8,
    "max_CRate": 5/6,
    "max_NChan": 52,
    "Nss": 1,
    "min_preamble": 20,  # μs
    "max_preamble": 92.8, #μs
    "TCP_ACK_frame_size": 88 #bytes
}

std_ac_w2_best = {
    "frame_size": 1548, #bytes
    "SIFS": 16, #μs
    "DIFS": 34, #μs
    "SDur": 3.6, #μs
    "min_data_rate": 7.2, #Mbps
    "max_data_rate": 6933.6, #Mbps
    "min_NBits": 1,
    "min_CRate": 1/2,
    "min_NChan": 52,
    "max_NBits": 8,
    "max_CRate": 5/6,
    "max_NChan": 468,
    "Nss": 8,
    "min_preamble": 20,  # μs
    "max_preamble": 92.8, #μs
    "TCP_ACK_frame_size": 88 #bytes
}

std_ax_normal = {
    "frame_size": 1548, #bytes
    "SIFS": 16, #μs
    "DIFS": 34, #μs
    "SDur": 13.6, #μs
    "min_data_rate": 8.6, #Mbps
    "max_data_rate": 9607.8, #Mbps
    "min_NBits": 1,
    "min_CRate": 1/2,
    "min_NChan": 234,
    "max_NBits": 10,
    "max_CRate": 5/6,
    "max_NChan": 234,
    "Nss": 1,
    "min_preamble": 20,  # μs
    "max_preamble": 92.8,  # μs
    "TCP_ACK_frame_size": 88 #bytes

}

std_ax_best = {
    "frame_size": 1548, #bytes
    "SIFS": 16, #μs
    "DIFS": 34, #μs
    "SDur": 13.6, #μs
    "min_data_rate": 8.6, #Mbps
    "max_data_rate": 9607.8, #Mbps
    "min_NBits": 1,
    "min_CRate": 1/2,
    "min_NChan": 1960,
    "max_NBits": 10,
    "max_CRate": 5/6,
    "max_NChan": 1960,
    "Nss": 8,
    "min_preamble": 20,  # μs
    "max_preamble": 92.8,  # μs
    "TCP_ACK_frame_size": 88 #bytes

}


def calculate(standard, data_rate, protocol, case):
    # data bits per OFDM symbol
    bits_per_symbol = math.floor(standard["min_NBits"] * standard["min_CRate"] * standard["min_NChan"] * standard["Nss"] if data_rate == "min" else standard["max_NBits"] * standard["max_CRate"] * standard["max_NChan"] * standard["Nss"])
    # Time to transfer a data frame
    time_data = math.ceil((standard["frame_size"] * 8 + 6) / bits_per_symbol) * standard["SDur"]
    # Time to transfer RTS
    time_rts = math.ceil((20*8+6) / bits_per_symbol) * standard["SDur"]
    # Time to transfer CTS
    time_cts = math.ceil((14*8+6) / bits_per_symbol) * standard["SDur"]
    # Time to transfer MAC ACK
    time_mac_ack = math.ceil((14*8+6) / bits_per_symbol) * standard["SDur"]
    # Time to transfer TCP ACK
    time_tcp_ack = math.ceil((standard["TCP_ACK_frame_size"] * 8 + 6) / bits_per_symbol) * standard["SDur"]
    # Time for a round-trip data frame communication: DIFS + Preamble + RTS + SIFS + Preamble + CTS + SIFS + Preamble + Data + SIFS + Preamble + MAC ACK
    time_data_round = standard["DIFS"] + time_rts + time_cts + 3 * standard["SIFS"] + time_data + time_mac_ack + 4 * (standard["min_preamble"] if case == "normal" else standard["max_preamble"])
    # Time for a round-trip TCP ACK: DIFS + Preamble + RTS + SIFS + Preamble + CTS + SIFS + Preamble + TCP ACK + SIFS + Preamble + MAC ACK
    time_tcp_ack_round = standard["DIFS"] + time_rts + time_cts + 3 * standard["SIFS"] + time_tcp_ack + time_mac_ack + 4 * (standard["min_preamble"] if case == "normal" else standard["max_preamble"])
    # 802.11g has a signal extension of 6 μs after every frame
    if standard == std_g:
        time_data_round += 6
        time_tcp_ack_round += 6
    # Actual throughput (Mbps)
    throughput = round((1500*8) / time_data_round, 2) if protocol == "UDP" else round((1500 * 8) / (time_data_round + time_tcp_ack_round), 2)
    # Time to transfer 15 * 10^9 bytes of data (seconds)
    time_to_transfer = round((15*(10**9) * 8) / (throughput*(10**6)), 2)
    print("Throughput: " + str(throughput) + " Mbps\nTime: " + str(time_to_transfer) + " seconds")
    return


if __name__ == '__main__':
    # Display menu
    print("-----802.11 Throughput calculator-----")
    print("1. 802.11g")
    print("2. 802.11ac_w2")
    print("3. 802.11ax")
    first_input = int(input("Select standard (type the number before each option): "))
    if first_input == 1:
        standard_normal = std_g
        standard_best = std_g
    elif first_input == 2:
        standard_normal = std_ac_w2_normal
        standard_best = std_ac_w2_best
    elif first_input == 3:
        standard_normal = std_ax_normal
        standard_best = std_ax_best
    else:
        print("Input Error!")
        exit(1)

    print("1. max")
    print("2. min")
    second_input = int(input("Select data rete (type the number before each option): "))
    if second_input == 1:
        data_rate = "max"
    elif second_input == 2:
        data_rate = "min"
    else:
        print("Input Error!")
        exit(1)

    print("1. UDP")
    print("2. TCP")
    third_input = int(input("Select protocol (type the number before each option): "))
    if third_input == 1:
        protocol = "UDP"
    elif third_input == 2:
        protocol = "TCP"
    else:
        print("Input Error!")
        exit(1)

    # Calculate throughput by chosen options
    print("-----Normal Result------")
    calculate(standard_normal, data_rate, protocol, "normal")
    print("-----Best Result------")
    calculate(standard_best, data_rate, protocol, "best")




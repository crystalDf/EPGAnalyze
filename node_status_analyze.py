import sys


class BoardInfo:
    def __init__(self, board, cpu, memory, board_info_function_list):
        self.board = board
        self.cpu = cpu
        self.memory = memory
        self.functions = board_info_function_list


class Function:
    def __init__(self, board_info, role, status, bearers, conns,
                 ul_pks, dl_pks):
        self.board_info = board_info
        self.role = role
        self.status = status
        self.bearers = bearers
        self.conns = conns
        self.ul_pks = ul_pks
        self.dl_pks = dl_pks


def abridge_str_with_num(original_str):
    original_str_list = original_str.split(', ')
    new_str_list = []
    for str_obj in original_str_list:
        new_str_list.append(str_obj[0:1] + str_obj[str_obj.index(' '):])
    return ', '.join(new_str_list)


def abridge_str_without_num(original_str):
    original_str_list = original_str.split(' ')
    new_str_list = []
    for str_obj in original_str_list:
        new_str_list.append(str_obj[0:1])
    return ''.join(new_str_list)


def format_function_list(function_list):
    for function in function_list:
        print(function.board_info.board + '\t' + function.role + '\t' +
              function.bearers + '\t' + function.conns + '\t' +
              function.board_info.cpu + '\t' + function.board_info.memory +
              '\t' + function.ul_pks + '\t' + function.dl_pks + '\t' +
              function.status)


def analyze_node_status(filename):
    with open(filename) as file_object:

        function_list = []

        while True:
            line = file_object.readline()
            if line.find('board-information') != -1:
                break

        while line.find('board-information') != -1:
            while line.find('board: ') == -1:
                line = file_object.readline()
            board = line.split('board: ')[1][:-1]

            while line.find('cpu-utilization: ') == -1:
                line = file_object.readline()
            cpu = line.split('cpu-utilization: ')[1][:-1]
            cpu = abridge_str_with_num(cpu)

            while line.find('memory: ') == -1:
                line = file_object.readline()
            memory = line.split('memory: ')[1][:-1]
            memory = abridge_str_with_num(memory)

            board_info_function_list = []

            board_info = BoardInfo(board=board, cpu=cpu, memory=memory,
                                   board_info_function_list=
                                   board_info_function_list)

            while line.find('function:') == -1:
                line = file_object.readline()

            while line.find('function:') != -1:
                while line.find('function-name: ') == -1:
                    line = file_object.readline()
                role = line.split('function-name: ')[1][:-1]
                role = abridge_str_without_num(role)

                while line.find('status: ') == -1:
                    line = file_object.readline()
                status = line.split('status: ')[1][:-1]

                line = file_object.readline()

                if line.find('external-gn-address: ') != -1:
                    line = file_object.readline()

                bearers = ''
                if line.find('number-of-bearers: ') != -1:
                    bearers = line.split('number-of-bearers: ')[1][:-1]
                    line = file_object.readline()

                conns = ''
                if line.find('number-of-pdn-connections: ') != -1:
                    conns = line.split('number-of-pdn-connections: ')[1][
                            :-1]
                    line = file_object.readline()

                if line.find('number-of-l2tp-sessions: ') != -1:
                    line = file_object.readline()

                ul_pks = ''
                if line.find('uplink-packets: ') != -1:
                    ul_pks = line.split('uplink-packets: ')[1][:-1]
                    line = file_object.readline()

                dl_pks = ''
                if line.find('downlink-packets: ') != -1:
                    dl_pks = line.split('downlink-packets: ')[1][:-1]
                    line = file_object.readline()

                if line.find('estimated-free-memory: ') != -1:
                    line = file_object.readline()

                function = Function(board_info=board_info, role=role,
                                    status=status, bearers=bearers,
                                    conns=conns, ul_pks=ul_pks, dl_pks=dl_pks)
                board_info_function_list.append(function)
                function_list.append(function)

                while line and line.find('function:') == -1 and \
                                line.find('board-information') == -1:
                    line = file_object.readline()

            board_info.board_info_function_list = board_info_function_list

        format_function_list(function_list)


if len(sys.argv) > 1:
    node_status_filename = sys.argv[1]
    analyze_node_status(node_status_filename)

import sys

from prettytable import PrettyTable


class NodeLim:
    def __init__(self, node_lim_entry):
        self.index = node_lim_entry[0]
        self.active = node_lim_entry[1].split(':')[2]
        self.standby = node_lim_entry[2].split(':')[2]
        self.primary = node_lim_entry[3].split(':')[2]
        self.secondary = node_lim_entry[4].split(':')[2]
        self.state = node_lim_entry[9]


class TsmTsft:
    def __init__(self, tsm_tsft_entry):
        self.tsid = tsm_tsft_entry[0]
        self.valid_prim = tsm_tsft_entry[1]
        self.valid_sec = tsm_tsft_entry[2]
        self.papid_prim = tsm_tsft_entry[3]
        self.papid_sec = tsm_tsft_entry[4]
        self.board_prim = (int(self.papid_prim.split('/')[0]) + 1) if (
            self.valid_prim == '1') else 0
        self.board_sec = (int(self.papid_sec.split('/')[0]) + 1) if (
            self.valid_sec == '1') else 0


class MergeNodeLim:
    def __init__(self, active, standby, primary, secondary, state,
                 index_range=''):
        self.active = active
        self.standby = standby
        self.primary = primary
        self.secondary = secondary
        self.state = state
        self.index_range = index_range


class MergeTsmTsft:
    def __init__(self, valid_prim, valid_sec, board_prim, board_sec,
                 tsid_range=''):
        self.valid_prim = valid_prim
        self.valid_sec = valid_sec
        self.board_prim = board_prim
        self.board_sec = board_sec
        self.tsid_range = tsid_range


def build_node_lim_list(filename):
    with open(filename) as file_object:

        node_lim_list = []

        while True:
            line = file_object.readline()
            if line.find('UP Index') != -1:
                break

        while True:
            line = file_object.readline()
            node_lim_entry = line.split()
            if len(node_lim_entry) > 0:
                node_lim = NodeLim(node_lim_entry)
                node_lim_list.append(node_lim)
                if int(node_lim_entry[0]) == 2047:
                    break

        return node_lim_list


def build_tsm_tsft_list(filename):
    with open(filename) as file_object:

        tsm_tsft_list = []

        while True:
            line = file_object.readline()
            if line.find('TSID Valid Primary') != -1:
                break

        while True:
            line = file_object.readline()
            tsm_tsft_entry_prim = line.split()
            if len(tsm_tsft_entry_prim) > 0:
                line = file_object.readline()
                tsm_tsft_entry_sec = line.split()
                tsm_tsft_entry = [tsm_tsft_entry_prim[0],
                                  tsm_tsft_entry_prim[1],
                                  tsm_tsft_entry_sec[1],
                                  tsm_tsft_entry_prim[5],
                                  tsm_tsft_entry_sec[5]]
                tsm_tsft = TsmTsft(tsm_tsft_entry)
                tsm_tsft_list.append(tsm_tsft)
                if int(tsm_tsft_entry_prim[0]) == 2047:
                    break

        return tsm_tsft_list


def analyze_node_lim_list(node_lim_list):
    merge_node_lim_list = []

    active = ''
    standby = ''
    primary = ''
    secondary = ''
    state = ''
    index = ''

    for node_lim_entry in node_lim_list:
        if (node_lim_entry.active != active) or (
                    node_lim_entry.standby != standby) or (
                    node_lim_entry.primary != primary) or (
                    node_lim_entry.secondary != secondary) or (
                    node_lim_entry.state != state):
            active = node_lim_entry.active
            standby = node_lim_entry.standby
            primary = node_lim_entry.primary
            secondary = node_lim_entry.secondary
            state = node_lim_entry.state
            index = node_lim_entry.index
            merge_node_lim = MergeNodeLim(active, standby, primary,
                                          secondary, state)

            merge_node_lim_list.append(merge_node_lim)
        else:
            merge_node_lim_list[-1].index_range = index + ' - ' + \
                                                  node_lim_entry.index

    format_node_lim_list(merge_node_lim_list)


def analyze_tsm_tsft_list(tsm_tsft_list):
    merge_tsm_tsft_list = []

    valid_prim = ''
    valid_sec = ''
    board_prim = ''
    board_sec = ''
    tsid = ''

    for tsm_tsft_entry in tsm_tsft_list:
        if (tsm_tsft_entry.valid_prim != valid_prim) or (
                    tsm_tsft_entry.valid_sec != valid_sec) or (
                    tsm_tsft_entry.board_prim != board_prim) or (
                    tsm_tsft_entry.board_sec != board_sec):
            valid_prim = tsm_tsft_entry.valid_prim
            valid_sec = tsm_tsft_entry.valid_sec
            board_prim = tsm_tsft_entry.board_prim
            board_sec = tsm_tsft_entry.board_sec
            tsid = tsm_tsft_entry.tsid
            merge_tsm_tsft = MergeTsmTsft(valid_prim, valid_sec, board_prim,
                                          board_sec)

            merge_tsm_tsft_list.append(merge_tsm_tsft)
        else:
            merge_tsm_tsft_list[-1].tsid_range = tsid + ' - ' + \
                                                 tsm_tsft_entry.tsid

    format_tsm_tsft__list(merge_tsm_tsft_list)


def format_node_lim_list(merge_node_lim_list):
    with open('node_lim_and_tsm_tsft_analyze_result.txt', 'a') as file_object:

        headers = ['Index Range', 'Primary', 'Secondary', 'Active', 'Standby',
                   'State']
        table = PrettyTable(headers)
        for merge_node_lim in merge_node_lim_list:
            row = [merge_node_lim.index_range, merge_node_lim.primary,
                   merge_node_lim.secondary, merge_node_lim.active,
                   merge_node_lim.standby, merge_node_lim.state]
            table.add_row(row)

        file_object.write(str(table) + '\n')


def format_tsm_tsft__list(merge_tsm_tsft_list):
    with open('node_lim_and_tsm_tsft_analyze_result.txt', 'a') as file_object:

        headers = ['Tsid Range', 'Primary', 'Secondary', 'Primary Valid',
                   'Secondary Valid']
        table = PrettyTable(headers)
        for merge_tsm_tsft in merge_tsm_tsft_list:
            row = [merge_tsm_tsft.tsid_range, merge_tsm_tsft.board_prim,
                   merge_tsm_tsft.board_sec, merge_tsm_tsft.valid_prim,
                   merge_tsm_tsft.valid_sec]
            table.add_row(row)

        file_object.write(str(table) + '\n')


if len(sys.argv) > 2:
    node_lim_master_table_filename = sys.argv[1]
    card_fabl_tsm_tsft_table_filename = sys.argv[2]

    node_lim_list_built = build_node_lim_list(node_lim_master_table_filename)
    tsm_tsft_list_built = build_tsm_tsft_list(
        card_fabl_tsm_tsft_table_filename)

    analyze_node_lim_list(node_lim_list_built)
    analyze_tsm_tsft_list(tsm_tsft_list_built)

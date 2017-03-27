''' Module of sushi crypt class and'''

from string import ascii_letters, digits
from binascii import hexlify, unhexlify
import os
import random
import codecs


class func_sushi:
    def rand_string(self, size, key):
        random.seed(key)
        return "".join(random.choice(ascii_letters + digits) for _ in range(size))

    def gen_noise(self, msg, base_key):
        sushi_obj = func_sushi()

        noise = str(os.urandom(1000)).split('\\')

        coor = random.randint(8, len(noise) - 1)

        random.seed(base_key)

        splitter = sushi_obj.rand_string(random.randint(3, 19), base_key)
        # print(splitter)

        noise[coor + 1] = splitter
        noise[coor - 1] = splitter
        noise[coor] = msg

        random.seed()

        noise[0] = sushi_obj.rand_string(random.randint(2, 4), base_key)

        return ''.join(noise)

    def gen_segment(self, seg_key, strt_seg, msg, ind):
        if ind == 'end':
            stp_seg = len(msg)
        else:
            random.seed(seg_key)

            stp_seg = random.randint(strt_seg + 30, strt_seg + 100)

            if len(msg) < strt_seg + stp_seg:
                stp_seg += len(msg) - (stp_seg + strt_seg)

            #print(stp_seg)
        return stp_seg

    def gen_comm_panel(self, alp, msg, seg, key):

        #print(alp, seg, key)

        random.seed(key)

        comm = list()

        for i in range(0, len(msg[seg[0]: seg[1]]), 1):
            comm.append(random.randint(0, len(alp) - 1))

        #print(seg)
        #print(len(msg[seg[0]: seg[1]]))
        #print(len(comm))

        #print(comm)

        return comm

    def inp_param(self):
        '''Function for input keys for rot, gamma key and other'''

        param = dict()

        amnt_rot = int(input('Amount of rotors( >= 4 and <= 32): '))

        while amnt_rot < 4 or amnt_rot > 32:
            print("Error amount of rotors < 4 or > 32, reinput this")
            amnt_rot = int(input('Amount of rotors( >= 4 and <= 32): '))

        param.update({'amnt_rots': amnt_rot})

        for i in range(0, param['amnt_rots'], 1):
            alp_key = input("Alphabet key for rotor №" + str(i + 1) +
                            " ( >= 4 symbols and <= 32): ")

            while len(alp_key) < 4 or len(alp_key) > 32:
                print("Error Alphabet key < 4 or > 32 symbols, reinput this")
                alp_key = input("Alphabet key for rotor №" + str(i + 1) +
                                " ( >= 4 symbols and <= 32): ")

            seg_key = input("Segment key for rotor №" + str(i + 1) + " ( >= 4 symbols and <= 32): ")

            while len(seg_key) < 4 or len(seg_key) > 32:
                print("Error Segment key < 4 or > 32 symbols, reinput this")
                seg_key = input("Segment key for rotor №" + str(i + 1) +
                                " ( >= 4 symbols and <= 32): ")

            param.update({'rot' + str(i + 1): [alp_key, seg_key]})

        base_key = input("Base key( >= 4 symbols and <= 32): ")

        while len(base_key) < 4 or len(base_key) > 32:
            print("Error base key < 4 or > 32 symbols, reinput this")
            base_key = input("Base key( >= 4 symbols and <= 32): ")

        param.update({"base_key": base_key})

        return param

    def gen_alp(self, alp_key):

        sushi_obj = func_sushi()

        random.seed(alp_key)

        alp = list()

        alp_len = random.randint(30, 60)

        for i in range(0, alp_len, 1):
            len_sym = random.randint(3, 6)
            alp.append(sushi_obj.rand_string(len_sym, alp_key + str(i)))

        return alp

    def repl_msg(self, seg, comm, alp, msg):
        sr_msg = list(msg[seg[0]: seg[1]])

        for i in range(0, len(sr_msg), 1):
            sr_msg[i] = alp[comm[i]]

        return ''.join(sr_msg)


    def encrypt(self):
        sushi_obj = func_sushi()

        segments = dict()

        os.system('clear')

        param = sushi_obj.inp_param()

        os.system('clear')

        msg = input('Message: ')

        if len(msg) < 10:
            print("!!!WARNING!!!\n\nYour message lenth < 10 sysmbols.\nIf you want encrypt this message, then computer generate noise for encrypt your message.")

        msg = sushi_obj.gen_noise(msg, param['base_key'])
        print(msg)

        random.seed(param['base_key'])
        splitter = sushi_obj.rand_string(random.randint(3, 19), param['base_key'])
        # print(splitter)

        # random.seed()

        alps = dict()

        for i in range(0, param['amnt_rots'], 1):
            alps.update({'rot_alp' + str(i + 1): sushi_obj.gen_alp(param['rot' + str(i + 1)][0])})

        strt_seg = 0
        for i in range(0, param['amnt_rots'], 1):
            if i == param['amnt_rots'] - 1:
                segments.update(
                    {'rot' + str(i + 1): [strt_seg, sushi_obj.gen_segment(param['rot' + str(i + 1)][1], strt_seg, msg, 'end')]})
                strt_seg = segments['rot' + str(i + 1)][1]
            else:
                segments.update(
                    {'rot' + str(i + 1): [strt_seg, sushi_obj.gen_segment(param['rot' + str(i + 1)][1], strt_seg, msg, ' ')]})
                strt_seg = segments['rot' + str(i + 1)][1]

        #print(msg.split(splitter))
        #print(hexlify(bytes(msg.encode('utf-8'))))

        comm_panel = dict()

        for i in range(0, param['amnt_rots'], 1):
            tmp_list = sushi_obj.gen_comm_panel(alps['rot_alp' + str(i + 1)], msg, segments['rot' + str(i + 1)], param['base_key'])
            comm_panel.update({'rot_seg' + str(i + 1): tmp_list})

        #print(comm_panel)

        enc_msg = str()

        for i in range(0, param['amnt_rots'], 1):
            #print(i)
            #print(comm_panel['rot_seg' + str(i + 1)])
            enc_msg += sushi_obj.repl_msg(segments['rot' + str(i + 1)], comm_panel['rot_seg' + str(i + 1)], alps['rot_alp' + str(i + 1)], msg)

        print('\n\n', enc_msg)
        print('\n\n', hexlify(bytes(enc_msg.encode('utf-8'))))


class sushi():
    def __init__(self, func):
        if func == 0:
            sushi_obj = func_sushi()
            sushi_obj.encrypt()

        else:
            encrypt()

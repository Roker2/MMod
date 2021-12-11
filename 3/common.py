import simpy
import numpy as np
import matplotlib.pyplot as plt

class QueuingSystem(object):
    def __init__(self, n, lambd, mu, env, p_bad, r_bad):
        ##queuing system params
        self.n = n
        self.lambd = lambd
        self.mu = mu
        ##custom params
        self.p_bad = p_bad
        self.r_bad = r_bad
        self.r_count = 0
        self.all_count = 0
        ##making requests simulation
        self.env = env
        self.loader = simpy.Resource(env, n)
        ##observable values
        self.L_queuing_system_lst = []
        self.L_queue_lst = []
        self.t_queuing_system_lst = []
        self.t_queue_lst = []
        # max queque length
        self.queque_len = 0
    
    def request_processing(self):
        yield self.env.timeout(np.random.exponential(1/self.mu))


def make_request(qs, env):
    queque_len_before = len(qs.loader.queue)
    n_occuped = qs.loader.count
    
    with qs.loader.request() as request:
        queque_len_after = len(qs.loader.queue)
        if queque_len_after > qs.queque_len:
            qs.queque_len = queque_len_after
        qs.L_queue_lst.append(queque_len_before)
        qs.L_queuing_system_lst.append(queque_len_before + n_occuped)
        arrival_time = env.now

        yield request

        qs.t_queue_lst.append(env.now - arrival_time)
        yield env.process(qs.request_processing())
        qs.t_queuing_system_lst.append(env.now - arrival_time)
        qs.all_count += 1
        # print(qs.all_count)

        if np.random.sample() < qs.p_bad:
            make_request(qs, env)
            if np.random.sample() < qs.r_bad:
                qs.r_count += 1


def run_queuing_system(qs, env):
    while True:
        yield env.timeout(np.random.exponential(1/qs.lambd))
        env.process(make_request(qs, env))


def display(characteristic, label):
    p, A, L_queuing_system, L_queue, t_queuing_system, t_queue, n_occuped, RQ = characteristic
    for i in range(len(p)):
        print( f'{label} p{(i)}: ', p[i] )
    print(f'{label} A (абсолютная пропускная способность): ', A)
    print(f'{label} L СМО (среднее число заявок в СМО): ', L_queuing_system)
    print(f'{label} L очереди (среднее число заявок в очереди): ', L_queue)
    print(f'{label} t СМО (среднее время пребывания заявки в СМО): ', t_queuing_system)
    print(f'{label} t очереди (среднее время пребывания заявки в очереди): ', t_queue)
    print(f'{label} n занятости (среднее число занятых каналов): ', n_occuped)
    print(f'{label} RQ рекламаций (среднее число рекламаций за единицу времени): ', RQ)
    print()
    
def get_p_from_characteristic(characteristic):
    p, A, L_queuing_system, L_queue, t_queuing_system, t_queue, n_occuped, RQ = characteristic
    return p
   
def get_queque_len_from_results(results):
    t_queuing_system_lst, L_queue_lst, t_queue_lst , L_queuing_system_lst, queque_len, r_count, all_count = results
    return queque_len

'''
def get_RQ_from_results(results):
    t_queuing_system_lst, L_queue_lst, t_queue_lst , L_queuing_system_lst, queque_len, r_count, all_count = results
    return RQ
'''
   
def p_graph(theoretical_characteristic, empirical_characteristic):
    plt.plot(get_p_from_characteristic(theoretical_characteristic))
    plt.plot(get_p_from_characteristic(empirical_characteristic))
    plt.legend(['Теоритические вероятности', 'Эмпирические вероятности'])
    plt.xlabel('p_i', color='gray')
    plt.show()
   
def get_xi_2(o, e):
    return sum(((o[i] - e[i]) ** 2) / e[i] for i in range(len(o)))
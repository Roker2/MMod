import simpy
import numpy as np
import matplotlib.pyplot as plt

class QueuingSystem(object):
    def __init__(self, n, m, lambd, mu, v, env):
        ##queuing system params
        self.n = n
        self.m = m
        self.lambd = lambd
        self.mu = mu
        self.v = v
        ##making requests simulation
        self.env = env
        self.loader = simpy.Resource(env, n)
        ##observable values
        self.L_queuing_system_lst = []
        self.L_queue_lst = []
        self.t_queuing_system_lst = []
        self.t_queue_lst = []
    
    def request_processing(self):
        yield self.env.timeout(np.random.exponential(1/self.mu))
    
    def waiting_in_queue(self):
        yield self.env.timeout(np.random.exponential(1/self.v))



def make_request(qs, env):
    queque_len_before = len(qs.loader.queue)
    n_occuped = qs.loader.count
    
    with qs.loader.request() as request:
        queque_len_after = len(qs.loader.queue)
        qs.L_queue_lst.append(queque_len_before)
        qs.L_queuing_system_lst.append(queque_len_before + n_occuped)
        if queque_len_after <= qs.m:
            arrival_time = env.now
            
            waiting_process = env.process(qs.waiting_in_queue())
            result = yield request | waiting_process    
            
            qs.t_queue_lst.append(env.now - arrival_time)
            if request in result:
                yield env.process(qs.request_processing())
                qs.t_queuing_system_lst.append(env.now - arrival_time)
            else:
                qs.t_queuing_system_lst.append(env.now - arrival_time)
        else:
            qs.t_queue_lst.append(0)
            qs.t_queuing_system_lst.append(0)



def run_queuing_system(qs, env):
    while True:
        yield env.timeout(np.random.exponential(1/qs.lambd))
        env.process(make_request(qs, env))


def display(characteristic, label):
    p, A, p_reject, L_queuing_system, L_queue, t_queuing_system, t_queue, n_occuped = characteristic
    for i in range(len(p)):
        print( f'{label} p{(i)}: ', p[i] )
    print(f'{label} A (абсолютная пропускная способность): ', A)
    print(f'{label} p отказа: ', p_reject)
    print(f'{label} L СМО (среднее число заявок в СМО): ', L_queuing_system)
    print(f'{label} L очереди (среднее число заявок в очереди): ', L_queue)
    print(f'{label} t СМО (среднее время пребывания заявки в СМО): ', t_queuing_system)
    print(f'{label} t очереди (среднее время пребывания заявки в очереди): ', t_queue)
    print(f'{label} n занятости (среднее число занятых каналов): ', n_occuped)
    print()
    
def get_p_from_characteristic(characteristic):
    p, A, p_reject, L_queuing_system, L_queue, t_queuing_system, t_queue, n_occuped = characteristic
    return p
   
def p_graph(theoretical_characteristic, empirical_characteristic):
    plt.plot(get_p_from_characteristic(theoretical_characteristic))
    plt.plot(get_p_from_characteristic(empirical_characteristic))
    plt.legend(['Теоритические вероятности', 'Эмпирические вероятности'])
    plt.xlabel('p_i', color='gray')
    plt.show()
   
def get_xi_2(o, e):
    return sum(((o[i] - e[i]) ** 2) / e[i] for i in range(len(o)))
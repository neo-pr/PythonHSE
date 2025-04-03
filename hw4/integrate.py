def integrate(f, a, b, job_nb=1, n_jobs=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    ini = n_iter // n_jobs * (job_nb - 1)
    fin = n_iter // n_jobs * job_nb if n_jobs != job_nb else n_iter

    for i in range(ini, fin):
        acc += f(a + i * step) * step
    return acc

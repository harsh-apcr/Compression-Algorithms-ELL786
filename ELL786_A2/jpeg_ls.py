import numpy as np

from golomb_code import modified_GPO2, modified_GPO2_decode
import math


# return the grayscale value of pixel at i,j
# 0 if pixel doesn't exist
def get(grayscale_img, i, j, m, n):
    return grayscale_img[i][j] if 0 <= i < m and 0 <= j < n else 0


# quantize local gradient bases on user defined parameter t1 ,t2 ,t3
def def_component(d, t1, t2, t3):
    if d <= -t3:
        return -4
    elif -t3 < d <= -t2:
        return -3
    elif -t2 < d <= -t1:
        return -2
    elif -t1 < d <= 0:
        return -1
    elif d == 0:
        return 0
    elif 0 < d <= t1:
        return 1
    elif t1 < d <= t2:
        return 2
    elif t1 < d <= t3:
        return 3
    else:
        # t3 < d
        return 4


# map context vector to integers in {1, ..., 365}
# (c1 ,c2 ,c3) -> {1, ..., 365}
def context_map(c1, c2, c3):
    # assuming (c1, c2, c3) is normalized (i.e. first non-zero entry is positive)
    if c1 != 0:
        return 41 + (c1 - 1) * 81 + (c2 + 4) * 9 + (c3 + 5)
    elif c2 != 0:
        # c1 == 0
        return 5 + (c2 - 1) * 9 + (c3 + 5)
    else:
        # c1 == 0 and c2 == 0
        return c3 + 1


# define context vector given local gradient (d1, d2, d3) and user defined parameter values (for quantization)
def def_context(d1, d2, d3, t1=3, t2=7, t3=21):
    return [def_component(d1, t1, t2, t3), def_component(d2, t1, t2, t3), def_component(d3, t1, t2, t3)]


# maps the residue res for golomb coding
def map_residue(res, k, B, N):
    if k == 0 and 2 * B <= -N:
        if res >= 0:
            return 2 * res + 1
        else:
            return -2 * (res + 1)
    else:
        if res >= 0:
            return 2 * res
        else:
            return -2 * res - 1


def invmap_residue(mapped_res, k, B, N):
    if k == 0 and 2 * B <= -N:
        if mapped_res % 2 == 0:
            return (-mapped_res // 2) - 1
        else:
            return (mapped_res - 1) // 2
    else:
        if mapped_res % 2 == 0:
            return mapped_res // 2
        else:
            return - (mapped_res + 1) // 2


# de-correlation + refinement step
# returns residual sequence of refined prediction
def jpegls_encode(grayscale_img, M, N0=64):
    # height
    m = len(grayscale_img)

    # width
    n = len(grayscale_img[0])

    # define cum_count, cum_bias,cum_ares for a given context {0, ..., 364}
    cum_count = [1] * 365
    cum_bias = [0] * 365
    correction = [0] * 365
    cum_ares = [max(2, (M + 32) // 64)] * 365

    beta = math.ceil(math.log2(M))
    bbeta = max(2, math.ceil(math.log2(M)))
    # any positive integer > bbeta+1 works
    L_max = 2 * (bbeta + max(8, bbeta))

    residual_seq = np.zeros((m, n), dtype=object)
    for i in range(m):
        for j in range(n):
            # de-correlation via prediction
            a = get(grayscale_img, i, j - 1, m, n)
            b = get(grayscale_img, i - 1, j, m, n)
            c = get(grayscale_img, i - 1, j - 1, m, n)
            d = get(grayscale_img, i - 1, j + 1, m, n)

            # context modeling (refining prediction error)

            # local gradient
            g1 = int(d) - int(b)
            g2 = int(b) - int(c)
            g3 = int(c) - int(a)

            # using default values of quantization boundaries to define context
            c_vec = def_context(g1, g2, g3)

            # 'normalize' c such that first non-zero entry of c is positive
            SIGN = 1
            if c_vec[0] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1
            elif c_vec[0] == 0 and c_vec[1] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1
            elif c_vec[0] == 0 and c_vec[1] == 0 and c_vec[2] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1

            # value-given the context vector c
            context = context_map(*c_vec) - 1

            # fixed prediction
            predicted_val = int(min(a, b)) if c >= max(a, b) else int(max(a, b)) if c <= min(a, b) else int(a) + int(
                b) - int(c)

            # refined/corrected prediction
            predicted_val = predicted_val + SIGN * correction[context]

            if predicted_val >= M:
                predicted_val = M - 1
            elif predicted_val < 0:
                predicted_val = 0

            residue = SIGN * (int(grayscale_img[i][j]) - predicted_val)

            # "modulo" the residue so that it belongs to -M/2 to M/2
            if residue < -M // 2:
                residue = residue + M
            elif residue > M // 2:
                residue = residue - M

            # encode residual_seq[i, j] using Golomb-Codes
            # compute the context dependent golomb-parameter k
            k = 0
            while (cum_count[context] << k) < cum_ares[context]:
                k += 1

            # perform mapped error encoding
            mapped_res = map_residue(residue, k, cum_bias[context], cum_count[context])
            residual_seq[i, j] = modified_GPO2(mapped_res, k, beta, L_max)

            # update cum_count , cum_bias given context c
            cum_bias[context] += residue
            cum_ares[context] += abs(residue)

            # if reset threshold limit is reached
            if cum_count[context] == N0:
                cum_count[context] = cum_count[context] >> 1
                cum_bias[context] = cum_bias[context] >> 1 if cum_bias[context] >= 0 else -(
                        (1 - cum_bias[context]) >> 1)
                cum_ares[context] = cum_ares[context] >> 1
            cum_count[context] += 1

            # division-free bias computation
            if cum_bias[context] <= -cum_count[context]:
                correction[context] = correction[context] - 1
                cum_bias[context] += cum_count[context]
                if cum_bias[context] <= -cum_count[context]:
                    cum_bias[context] = -cum_count[context] + 1

            elif cum_bias[context] > 0:
                correction[context] = correction[context] + 1
                cum_bias[context] -= cum_count[context]
                if cum_bias[context] > 0:
                    cum_bias[context] = 0
    return residual_seq


def jpegls_decode(residual_seq, M, N0=64):
    # height
    m = len(residual_seq)

    # width
    n = len(residual_seq[0])

    # define cum_count, cum_bias,cum_ares for a given context {0, ..., 364}
    cum_count = [1] * 365
    cum_bias = [0] * 365
    correction = [0] * 365
    cum_ares = [max(2, (M + 32) // 64)] * 365

    beta = math.ceil(math.log2(M))
    bbeta = max(2, math.ceil(math.log2(M)))
    # any positive integer > bbeta+1 works
    L_max = 2 * (bbeta + max(8, bbeta))

    grayscale_img = np.zeros((m, n), dtype=int)
    for i in range(m):
        for j in range(n):
            # de-correlation via prediction
            a = get(grayscale_img, i, j - 1, m, n)
            b = get(grayscale_img, i - 1, j, m, n)
            c = get(grayscale_img, i - 1, j - 1, m, n)
            d = get(grayscale_img, i - 1, j + 1, m, n)

            # context modeling (refining prediction)

            # local gradient
            g1 = int(d) - int(b)
            g2 = int(b) - int(c)
            g3 = int(c) - int(a)

            # using default values of quantization boundaries to define context
            c_vec = def_context(g1, g2, g3)

            # 'normalize' c such that first non-zero entry of c is positive
            SIGN = 1
            if c_vec[0] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1
            elif c_vec[0] == 0 and c_vec[1] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1
            elif c_vec[0] == 0 and c_vec[1] == 0 and c_vec[2] < 0:
                c_vec = [-x for x in c_vec]
                SIGN = -1

            # value-given the context vector c
            context = context_map(*c_vec) - 1

            # fixed-prediction
            predicted_val = int(min(a, b)) if c >= max(a, b) else int(max(a, b)) if c <= min(a, b) else int(a) + int(
                b) - int(c)

            # refined/corrected prediction
            predicted_val = predicted_val + SIGN * correction[context]

            if predicted_val >= M:
                predicted_val = M - 1
            elif predicted_val < 0:
                predicted_val = 0

            # compute context dependent golomb-parameter k , to decode residue
            k = 0
            while (cum_count[context] << k) < cum_ares[context]:
                k += 1

            # decode residue (mapped error value)
            mapped_residue = modified_GPO2_decode(residual_seq[i][j], beta, L_max)

            # apply inverse map to residue to get the actual signed modulo residue
            residue = invmap_residue(mapped_residue, k, cum_bias[context], cum_count[context])

            # update cum_count , cum_bias , cum_ares given context c
            # low complexity division-free bias computation
            cum_bias[context] += residue
            cum_ares[context] += abs(residue)

            # if reset thresh-hold limit is reached
            if cum_count[context] == N0:
                cum_count[context] = cum_count[context] >> 1
                cum_bias[context] = cum_bias[context] >> 1 if cum_bias[context] >= 0 else -(
                        (1 - cum_bias[context]) >> 1)
                cum_ares[context] = cum_ares[context] >> 1
            cum_count[context] += 1

            # above residue is "modulo-'ed" in [-M/2,M/2]
            # re-map to get actual "corrected" residue
            if -predicted_val <= residue < M - predicted_val:
                residue = residue
            elif residue >= M - predicted_val:
                residue = residue - M
            elif residue < -predicted_val:
                residue = residue + M
            residue = SIGN * residue

            grayscale_img[i, j] = (residue + predicted_val) % M

            # Implement the 15th - pt


            # division-free bias computation
            if cum_bias[context] <= -cum_count[context]:
                correction[context] = correction[context] - 1
                cum_bias[context] += cum_count[context]
                if cum_bias[context] <= -cum_count[context]:
                    cum_bias[context] = -cum_count[context] + 1

            elif cum_bias[context] > 0:
                correction[context] = correction[context] + 1
                cum_bias[context] -= cum_count[context]
                if cum_bias[context] > 0:
                    cum_bias[context] = 0

    return grayscale_img

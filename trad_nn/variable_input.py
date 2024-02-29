
def default(tp, input, j, i):
    tp.append(input[j][2*i])
    tp.append(input[j][2*i + 1])

def phi(tp,input,j,i):
    tp.append(abs(input[j][2*i+1] - input[j][2*i] - 3.1415))

def masym(tp,input,j,i):
    tp.append(input[j][2*i])

def input_dict():
    d = {
            "jtrip_masym": masym,
            "jtrip_phi": phi,
            "jtrip_delta": default,
            "jtrip_qgl": default,
            "jtrip_dlow": default,
            "jtrip_dmid": default,
            "jtrip_dhigh": default
            
    }
    return d
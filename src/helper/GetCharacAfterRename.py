def get_antibiotics(_imgname):
    return _imgname.split('_')[0]

def get_conc(_imgname):
    return _imgname.split('_')[1]

def get_position(_imgname):
    return _imgname.split('_')[2]

def get_time(_imgname):
    return _imgname.split('_')[3].split('.')[0]

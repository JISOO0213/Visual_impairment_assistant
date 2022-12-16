import yaml
 
with open('../data/mot16.yaml', 'r', encoding = 'utf-8') as f:
	data = yaml.full_load(f)
    
#print(data)
 
data['train'] = './train.txt'
data['val'] = './valid.txt'
 
with open('../data/mot16.yaml', 'w') as f:
	yaml.dump(data, f)
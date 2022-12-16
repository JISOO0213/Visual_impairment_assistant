from glob import glob
 
# 이미지들의 주소 리스트로 만들어줌
train_img_list = glob('./train/*.jpg')
valid_img_list = glob('./val/*.jpg')
 
# 리스트를 txt파일로 생성
with open('./train.txt', 'w') as f:
	f.write('\n'.join(train_img_list) + '\n')
    
with open('./val.txt', 'w') as f:
	f.write('\n'.join(valid_img_list) + '\n')